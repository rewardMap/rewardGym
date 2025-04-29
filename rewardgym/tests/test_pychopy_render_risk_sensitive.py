import numpy as np

from rewardgym.psychopy_render.risk_sensitive import risksensitive_stimuli
from rewardgym.stimuli import STIMULUS_DEFAULTS


def test_smoke_risksensitive_stimuli():
    for _ in range(10):
        i = np.random.default_rng(np.random.randint(1000))
        risksensitive_stimuli(random_state=i, stim_defaults=STIMULUS_DEFAULTS)
        risksensitive_stimuli(random_state=i, stim_defaults=STIMULUS_DEFAULTS)
