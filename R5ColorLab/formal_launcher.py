"""Launch the portable formal Mac/AMD console with isolated job directories."""
from pathlib import Path
import argparse
import json
import os
import subprocess
import sys

ROOT=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--backend',choices=('mac','amd'),default='amd' if sys.platform=='win32' else 'mac')
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--test',action='store_true')
    parser.add_argument('--port',type=int,default=4180)
    args,extra=parser.parse_known_args()
    runtime=ROOT/('amd' if args.backend=='amd' else 'web')
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1',
         'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','VECLIB_MAXIMUM_THREADS':'1'}
    if args.test:
        return subprocess.call([sys.executable,'-X','utf8',str(ROOT/'self_check.py'),'--test'],cwd=ROOT,env=env)
    if args.check:
        env['R5_GPU_TRAINING']='1'
        code='''import json,sys
from pathlib import Path
root=Path(sys.argv[1]);runtime=Path(sys.argv[2]);sys.path[:0]=[str(runtime),str(root/'scripts')]
import core,baseline,gpu_runtime,numpy as np
from edit_color_pipeline import RuntimeColor
from edit_parameter_context import ParameterContext
from measured_response import default_response,get
m=RuntimeColor.from_capture(*baseline.resolve(baseline.V45_ID));ParameterContext(m)
p=np.tile(np.array([4208,1574,6937],np.uint16),(1,9,1))
assert m.sectors(p)[0,4]==59 and m.color_only(p)[0,4].tolist()==[16383,9795,16383]
assert len(core.presets()[0])==12
get(default_response())
if hasattr(gpu_runtime,'configure'):gpu_runtime.configure()
assert gpu_runtime.available(),'Requested GPU unavailable'
print(json.dumps(dict(backend=gpu_runtime.policy(),hue_boundary_verified=True)))
'''
        return subprocess.call([sys.executable,'-X','utf8','-c',code,str(ROOT),str(runtime)],cwd=ROOT,env=env)
    return subprocess.call([sys.executable,'-X','utf8',str(runtime/'formal_server.py'),
        '--port',str(args.port),*extra],cwd=ROOT,env=env)

if __name__=='__main__':sys.exit(main())
