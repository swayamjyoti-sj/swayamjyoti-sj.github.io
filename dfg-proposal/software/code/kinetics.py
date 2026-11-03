"""Conditional activated-event hazards and Gillespie clock; illustrative inputs."""
from math import exp, log, log1p
from random import Random

def stats(barriers, kbt, attempts):
    if not barriers or len(barriers) != len(attempts) or kbt <= 0:
        raise ValueError("Invalid arguments")
    if any(b < 0 for b in barriers) or any(a <= 0 for a in attempts):
        raise ValueError("Barriers nonnegative and attempts positive")
    logits = [log(a) - b / kbt for b, a in zip(barriers, attempts)]
    center = max(logits)
    weight = [exp(v-center) for v in logits]
    total = exp(center) * sum(weight)
    return total, [v / sum(weight) for v in weight]

def next_event(barriers, kbt, attempts, rng=None):
    rng = rng or Random()
    total, probabilities = stats(barriers, kbt, attempts)
    dt = -log1p(-rng.random()) / total
    u, acc = rng.random(), 0
    for i, p in enumerate(probabilities):
        acc += p
        if u <= acc:
            return dt, i
    return dt, len(probabilities)-1

if __name__ == "__main__":
    k, probabilities = stats([5,8,12], 2, [1e6]*3)
    print("Rate (1/tau):", k, "Probabilities:", probabilities, "Mean wait:", 1/k)
