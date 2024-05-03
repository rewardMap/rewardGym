.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.10942784.svg
  :target: https://doi.org/10.5281/zenodo.10942784

.. image:: https://codecov.io/gh/rewardMap/rewardGym/graph/badge.svg?token=NVVNHNP38M
 :target: https://codecov.io/gh/rewardMap/rewardGym

.. image:: https://github.com/rewardMap/rewardGym/actions/workflows/build-sphinx.yaml/badge.svg
.. image:: https://github.com/rewardMap/rewardGym/actions/workflows/pip-push.yaml/badge.svg

==================================
rewardGym
==================================

Ambitiously called ``rewardGym``, this is a part of the ``rewardMap`` project.

The project's goal is to provide two things:

1. A common language for reward tasks used in research.
2. A common interface to display and collect data for these tasks.

Under the hood this module uses the `gymnasium <https://github.com/Farama-Foundation/Gymnasium>`_ [cit1]_. The general package has
been greatly inspired by `neuro-nav <https://github.com/awjuliani/neuro-nav>`_ [cit2]_, especially the use of a graph structure to represent the tasks.


Installation
-------------------------------------------------------------------------------

I recommend creating a new python enviroment (using e.g. ``venv`` or ``conda``).

Then install the package and all necessary dependencies using::

    pip install git+https://github.com/rewardMap/rewardGym


Alternatively, download / clone the repository and install from there::

    git clone https://github.com/rewardMap/rewardGym
    cd rewardGym
    pip install -e .

Usage
-------------------------------------------------------------------------------

The package should be importable as usually.


Play a task
********************************************************************************

To play one of the tasks using a simplified pygame implementation, you can e.g.
run::

    rg_play hcp --window 700 --n 5

To play the gambling task from the human connectome project, in a window of 700 x 700 pixels for 5 trials.

The available tasks are:

hcp
    Gambling task from the human connectome project. Response buttons are: left + right.
mid
    Monetary incentive delay task. Response button is: space
two-step
    The classic two-step task. Response buttons are: left + right
risk-sensitive
    Risk sensitive decision making task, contains both decision tasks between to outcome and singular event. Response buttons are: Left + right
posner
    Posner task. Response buttons are left + right.
gonogo
    Go / No-Go task, different stimuli indicate go to win, go to punish etc. Response button is: space.


Use PsychoPy for data collection
********************************************************************************

There might be cases, where you want to use this package purely for data collection.

In the current release, basic logging is supported.

This is also possible using `PsychoPy <https://psychopy.org/>`_ Standalone [cit3]_ (only tested version v2023.2.3).

For this clone or download the repository.

E.g.::

    git clone https://github.com/rewardMap/rewardGym

**IMPORTANT:**

In it's current form, the stimuli files are not shipped with the package, please ask SRSteinkamp to get the files.


Afterwards, you can use the PsychoPy coder to run ``rewardGym.py``, which is located in the root directory.

Outputs of this program will be saved by default in the ``data`` directory.


Run the environment and train an agent
********************************************************************************

Running a task could look like the following

.. code-block:: python

    from rewardgym import get_env, unpack_conditions
    from rewardgym.agents.base_agent import QAgent

    env, conditions = get_env('hcp')
    agent = QAgent(env, 0.1, 0.2)

    n_episodes = 1000

    for t in range(n_episodes):

        condition, starting_position = unpack_conditions(conditions, t)

        obs, info = env.reset(agent_location=starting_position, condition=condition)

        done = False

        while not done:

            action = agent.get_action(obs)

            next_obs, reward, terminated, truncated, info = env.step(action)

            agent.update(obs, action, reward, terminated, next_obs)
            done = terminated or truncated
            obs = next_obs


References
--------------------------------------------------------------------------------
.. [cit1] Towers, M., Terry, J. K., Kwiatkowski, A., Balis, J. U., Cola, G. de, Deleu, T., Goulão, M., Kallinteris, A., KG, A., Krimmel, M., Perez-Vicente, R., Pierré, A., Schulhoff, S., Tai, J. J., Shen, A. T. J., & Younis, O. G. (2023). Gymnasium. Zenodo. https://doi.org/10.5281/zenodo.8127026
.. [cit2] Juliani, A., Barnett, S., Davis, B., Sereno, M., & Momennejad, I. (2022). Neuro-Nav: A Library for Neurally-Plausible Reinforcement Learning (arXiv:2206.03312). arXiv. https://doi.org/10.48550/arXiv.2206.03312
.. [cit3] Peirce, J., Gray, J. R., Simpson, S., MacAskill, M., Höchenberger, R., Sogo, H., Kastman, E., & Lindeløv, J. K. (2019). PsychoPy2: Experiments in behavior made easy. Behavior Research Methods, 51(1), 195–203. https://doi.org/10.3758/s13428-018-01193-y
