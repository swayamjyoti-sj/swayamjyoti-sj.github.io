"""ARTn/NEB catalogue data contract, NOT an ARTn or NEB solver.
LJ energy in epsilon; event moment in sigma_LJ**3.
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class Event:
    source: str
    target: str
    saddle_id: str
    energy_source: float
    energy_target: float
    energy_saddle: float
    moment_xy: float
    region: int

    @property
    def forward_barrier(self):
        return self.energy_saddle - self.energy_source

    @property
    def reverse_barrier(self):
        return self.energy_saddle - self.energy_target

    def validate(self):
        if self.forward_barrier < 0 or self.reverse_barrier < 0:
            raise ValueError("Saddle must lie above both minima")
        if self.region < 0:
            raise ValueError("Negative region")
        return True

def deduplicate(events):
    """IDs only for this demo; real searches require geometry/path matching."""
    seen, result = set(), []
    for e in events:
        e.validate()
        key = (e.source, e.target, e.saddle_id)
        if key not in seen:
            result.append(e)
            seen.add(key)
    return result

if __name__ == "__main__":
    event = Event("A", "B", "S01", -100, -102, -90, .16, 0)
    print("Forward, reverse barriers:", event.forward_barrier, event.reverse_barrier)
