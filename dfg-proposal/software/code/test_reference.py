"""Run: python -m unittest discover -s code -p 'test_*.py' (from software/)."""
import unittest
from math import isclose
from catalogue import Event
from kinetics import stats
from mesoscale import Mesostate
from continuum import Cohesive,voigt_shear

class TestReference(unittest.TestCase):
    def test_barriers(self):
        e=Event("A","B","S",-100,-102,-90,.16,0)
        self.assertEqual((e.forward_barrier,e.reverse_barrier),(10,12))
    def test_rates(self):
        k,p=stats([5,8,12],2,[1e6]*3)
        self.assertTrue(isclose(sum(p),1.0))
        self.assertGreater(p[0],p[1])
    def test_plastic_moment(self):
        m=Mesostate(1000)
        self.assertTrue(isclose(m.apply_moments([.16]*20),.0032))
        self.assertTrue(isclose(m.stress(.02,20),.336))
    def test_rve_work(self):
        stress,work=voigt_shear([.30,.34,.36,.32],[.25]*4,.005)
        self.assertTrue(isclose(stress,.33))
        self.assertTrue(isclose(work,.00165))
    def test_fracture(self):
        c=Cohesive()
        self.assertTrue(isclose(c.fracture_energy,.4))
        self.assertTrue(isclose(c.work_to(1),.2888888888888889))

if __name__=="__main__":
    unittest.main()
