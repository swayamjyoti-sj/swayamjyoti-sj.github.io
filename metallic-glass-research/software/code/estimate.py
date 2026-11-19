"""Reproduce a candidate breakdown of the 1,000,000 core-hour envelope.

These are planning assumptions, NOT measured node performance or allocated HPC.
The 100,000-core-hour mesoscale line is provisionally subdivided to include
continuum and conditional cohesive-fracture work. Revise proposal if adopted.
"""
workloads = [
  ("Preparation and equilibration",300,16,31.25),
  ("ARTn/NEB searches",2500,32,7.5),
  ("AQS and replica validation",750,16,12.5),
  ("Mesoscale kinetics and coupling",400,16,9.375),
  ("Continuum RVE and closure tests",125,16,12.5),
  ("Conditional cohesive fracture",75,16,12.5),
]
if __name__ == "__main__":
    total=0
    for name,jobs,cores,hours in workloads:
        budget=jobs*cores*hours
        total+=budget
        print(f"{name}: {jobs} jobs × {cores} cores × {hours} h = {budget:,.0f} core-h")
    assert total == 1_000_000
    print("TOTAL:",f"{total:,.0f} core-h")
