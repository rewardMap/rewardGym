import numpy as np

from rewardgym.psychopy_render.risk_sensitive import risksensitive_stimuli


def test_smoke_risksensitive_stimuli():
    for _ in range(10):
        i = np.random.randint(0, 10000)
        risksensitive_stimuli(random_state=i)
