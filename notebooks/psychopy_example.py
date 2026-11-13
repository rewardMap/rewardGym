"""
Example code for using psychopy + rewardGym.
As a set up create a copy of this code and move it into the root directory of
the rewardGym folder.
Then open the file in PsychoPy coder. Note, that it requires a recent
PsychoPy version (tested on at least v2026.1.3).
"""

from psychopy import core, event, visual
from rewardgym.psychopy_render.psychopy_display import (
    ActionStimulus,
    BaseStimulus,
    FeedBackStimulus,
    TextStimulus,
)

from rewardgym.environments import RenderEnv
from rewardgym.logging import ExperimentLogger
from rewardgym.reward_classes import BaseReward

# As in the pygame example, we create the graph, rewards and their locations:
env_graph = {0: [1, 2], 1: [], 2: []}

reward1 = BaseReward(reward=[0, 1], p=[0.2, 0.8], random_state=2222)
reward2 = BaseReward(reward=[0, 1], p=[0.5, 0.5], random_state=3333)

# This creates the reward dictionary necessary for the environment.
reward_locs = {1: reward1, 2: reward2}

# We then create the environment. Note that we use a RenderEnv.
env = RenderEnv(environment_graph=env_graph, reward_locations=reward_locs)

# We then creat the stimuli we want to display. Here we use a very minimal example
# as in the pygame example:

# This is just a flip of the screen (clear everything that is on there)
flip_screen = BaseStimulus(duration=0)
# Then we put a fixatoin cross on the screen for 0.2 s (note the different time units for pygame (ms) and psychopy (s))
fixation = TextStimulus(duration=0.2, text="+", position=(0, 0), name="text1")
# Another TextStimulus to show the choic
selection = TextStimulus(duration=0.001, text="A or B", position=(0, 0), name="text2")
# Finally, we require an action, which is done using the ActionStimulus.
action = ActionStimulus(duration=10, key_dict={"left": 0, "right": 1})

# In the end we create some reward feedback.
reward = FeedBackStimulus(
    duration=1.0,
    text="You gain: {0}",
    position=(0, 0),
    target="reward",
    name="feedback1",
)
earnings = FeedBackStimulus(
    duration=0.5,
    text="You have gained: {0}",
    position=(0, 0),
    target="total_reward",
    name="feeback2",
)

# We then augment the nodes in the info dict with the stimuli.
info_dict = {
    0: {"render": [flip_screen, fixation, selection, action]},
    1: {"render": [flip_screen, reward, earnings]},
    2: {"render": [flip_screen, reward, earnings]},
}

env.info_dict.update(info_dict)


# For psychopy we need to create a window to render the stimuli onto.
win = visual.Window(
    size=[1680, 1050],
    fullscr=False,
    color=[-0.5, -0.5, -0.5],
    units="pix",
)

# As the stimuli require a logger object, we create one here. If we create an ExperimentLogger
# with file_name=None, it is properly writing everything to a dictionary.
# Here it is just used for compatibility with the stimulus classes (see the main psychopy
# code in the root dir for advanced logging).
Logger = ExperimentLogger(file_name=None, clock=core.Clock())
Logger.create()

# Finally, the stimuli need to be setup (associating and creating the psychopy
# objects that need a window object). The pyschopy environment has a method for that:
env.setup(window=win, logger=Logger)

# We also show some instructions here:
instruction = visual.TextStim(
    win=win, text="Hi\nWellcome to the example", color=[1, 1, 1]
)

instruction.draw()
win.flip()
event.waitKeys()
win.flip()

# The main loop to display the experiment.
n_episodes = 5  # Change to a higher number, disabled here for rendering.

for episode in range(n_episodes):
    Logger.set_trial_time()
    obs, info = env.reset(agent_location=0)
    done = False

    while not done:
        # The environment stores the action (and the previous action)
        next_obs, reward, terminated, truncated, info = env.step(env.action)

        done = terminated or truncated
        obs = next_obs

# And finally closing everything.
env.close()
win.close()
core.quit()
