"""Small-strain continuum checks and independent cohesive-fracture toy law.

NOT a full finite-strain FE, phase-field, gradient-plasticity or crack solver.
Units: energy epsilon, length sigma_LJ, stress epsilon/sigma_LJ^3.
"""
from dataclasses import dataclass
from math import isclose

@dataclass
class Cohesive:
    tmax: float = 0.4
    delta0: float = 0.2
    deltaf: float = 2.0

    def __post_init__(self):
        if not (self.tmax > 0 and 0 < self.delta0 < self.deltaf):
            raise ValueError("Invalid cohesive law")

    def traction(self, delta):
        if delta < 0:
            raise ValueError("Opening must be nonnegative")
        if delta <= self.delta0:
            return self.tmax*delta/self.delta0
        if delta < self.deltaf:
            return self.tmax*(self.deltaf-delta)/(self.deltaf-self.delta0)
        return 0.0

    def damage_envelope(self, delta):
        if delta <= self.delta0:
            return 0.0
        if delta >= self.deltaf:
            return 1.0
        return self.deltaf*(delta-self.delta0)/(delta*(self.deltaf-self.delta0))

    @property
    def fracture_energy(self):
        return 0.5*self.tmax*self.deltaf

    def work_to(self, delta):
        if delta <= 0:
            return 0.0
        if delta <= self.delta0:
            return .5*self.tmax*delta**2/self.delta0
        d = min(delta, self.deltaf)
        return .5*self.tmax*self.delta0 + .5*(self.tmax+self.traction(d))*(d-self.delta0)

def voigt_shear(stresses, fractions, delta_gamma):
    """Uniform-strain check; does NOT prove finite-strain Hill-Mandel consistency."""
    if not stresses or len(stresses) != len(fractions) or min(fractions)<0:
        raise ValueError("Invalid RVE values")
    if not isclose(sum(fractions),1,abs_tol=1e-12):
        raise ValueError("Fractions must sum to 1")
    macro = sum(s*v for s,v in zip(stresses,fractions))
    micro_work = sum(s*v*delta_gamma for s,v in zip(stresses,fractions))
    assert isclose(macro*delta_gamma,micro_work,rel_tol=1e-12)
    return macro,micro_work

def series_bar_curve(openings, young_modulus=20., length=10., cohesive=None):
    """Equilibrium parameterization U=delta+L*T/E, NOT postpeak path following."""
    law=cohesive or Cohesive()
    return [(d+length*law.traction(d)/young_modulus,law.traction(d)) for d in openings]

if __name__ == "__main__":
    tau,work=voigt_shear([.30,.34,.36,.32],[.25]*4,.005)
    law=Cohesive()
    assert isclose(tau,.33)
    assert isclose(work,.00165)
    assert isclose(law.fracture_energy,.4)
    assert isclose(law.work_to(1.),.2888888888888889)
    print("RVE stress:",tau,"work:",work)
    print("Gc:",law.fracture_energy,"work(delta=1):",law.work_to(1.))
    print("Bar points:",series_bar_curve([0,.2,1,2]))
