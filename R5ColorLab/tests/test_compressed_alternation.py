"""Fixed-grid forward, full native loss, and block derivatives match float64."""
import unittest
import numpy as np
from test_gpu_alternation import GPUAlternationTests
from compressed_alternation import CompressedGridObjective, residual
from measured_response import default_response,get

class CompressedAlternationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        GPUAlternationTests.setUpClass()
        src=GPUAlternationTests
        cls.smooth,cls.start,cls.vector=src.smooth,src.start,src.vector
        cls.target,cls.weights=src.target,src.weights
        cls.grid=np.random.default_rng(42).integers(-8,9,(405,3),dtype=np.int8)
        cls.response=default_response()
        cls.objective=CompressedGridObjective(cls.smooth,cls.target*16383,cls.weights,
            cls.start,cls.grid,cls.response,device='cpu',dtype=src.torch.float64)

    @classmethod
    def rows(cls,v):
        return residual(cls.smooth,cls.target*16383,cls.weights,cls.start,cls.grid,cls.response,v)

    def test_forward_and_loss_match_packed_grid_cpu(self):
        t=self.objective.gpu.tensor(self.vector)
        result=self.objective.corrected(self.objective.gpu.render(t)/16383).detach().numpy()
        expected=get(self.response).predict_cpu(self.smooth.render(self.vector)/16383,self.grid)
        np.testing.assert_allclose(result,expected,atol=2e-10,rtol=0)
        rows=self.rows(self.vector)
        self.assertAlmostEqual(float(self.objective.loss(t)),float(rows@rows)/len(self.weights),places=11)

    def test_both_native_blocks_differentiate_through_grid_coordinates(self):
        _,gradient=self.objective.value_gradient(self.vector,slice(None))
        rng=np.random.default_rng(5)
        for block in (slice(0,104),slice(104,None)):
            direction=np.zeros_like(self.vector);direction[block]=rng.normal(size=len(direction[block]));direction/=np.linalg.norm(direction)
            eps=1e-6;lo=self.rows(self.vector-eps*direction);hi=self.rows(self.vector+eps*direction)
            expected=(hi@hi-lo@lo)/(2*eps*len(self.weights))
            self.assertAlmostEqual(float(gradient@direction),expected,delta=max(1e-8,abs(expected)*.02))

if __name__=='__main__':unittest.main()
