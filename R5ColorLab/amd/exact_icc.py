"""Float64 LittleCMS transforms on Windows; no RGB16 intermediate lookup."""
import hashlib
import io
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from PIL import ImageCms


class ExactRGBTransform:
    def __init__(self, source_icc, destination_icc):
        import imagecodecs
        if not imagecodecs.CMS.available:
            raise RuntimeError('imagecodecs lacks LittleCMS support')
        self.source, self.destination = source_icc, destination_icc
        for raw in (source_icc, destination_icc):
            if ImageCms.ImageCmsProfile(io.BytesIO(raw)).profile.xcolor_space.strip() != 'RGB':
                raise ValueError('Only RGB ICC profiles are supported')

    def convert_float(self, rgb):
        import imagecodecs
        source = np.ascontiguousarray(rgb, dtype=np.float64)
        if source.shape[-1] != 3 or not np.isfinite(source).all():
            raise ValueError('Expected finite normalized RGB')
        result = imagecodecs.cms_transform(source.reshape(-1, 1, 3), self.source, self.destination,
            colorspace='RGB', outcolorspace='RGB', outdtype=np.float64, intent=1, flags=0x0100).reshape(source.shape)
        if result.dtype != np.float64 or result.shape != source.shape or not np.isfinite(result).all():
            raise ValueError('LittleCMS did not return a finite float64 RGB result')
        return np.clip(result, 0, 1)

    def convert(self, rgb16):
        source = np.asarray(rgb16)
        if source.dtype != np.uint16:
            raise ValueError('Expected uint16 RGB')
        return np.rint(self.convert_float(source/65535)*65535).astype(np.uint16)

    def close(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()


def to_srgb(probes, icc):
    values = np.asarray(probes, dtype=np.float64)
    if not icc:
        return values, dict(policy='untagged-assumed-sRGB', converted=False)
    profile = ImageCms.ImageCmsProfile(io.BytesIO(bytes(icc)))
    description = ImageCms.getProfileDescription(profile).strip()
    if profile.profile.xcolor_space.strip() != 'RGB':
        raise ValueError('需要 RGB ICC 配置文件')
    info = dict(source_profile=description, source_icc_sha256=hashlib.sha256(icc).hexdigest())
    if 'srgb' in description.lower().replace(' ', ''):
        return values, dict(info, policy='embedded-sRGB', converted=False)
    destination = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
    shape = values.shape
    flat = values.reshape(-1, 3)
    def convert(part):
        with ExactRGBTransform(icc, destination) as transform:
            return transform.convert_float(part)
    with ThreadPoolExecutor(max_workers=10, thread_name_prefix='r5-icc') as pool:
        result = np.concatenate(list(pool.map(convert, np.array_split(flat, min(8, len(flat)))))).reshape(shape)
    import imagecodecs
    return result, dict(info, policy='float64-NOOPTIMIZE-relative-noBPC-before-mean', converted=True,
        workers=10, working_bits=64, intermediate_quantization=False, backend=imagecodecs.cms_version(),
        destination_icc_sha256=hashlib.sha256(destination).hexdigest())
