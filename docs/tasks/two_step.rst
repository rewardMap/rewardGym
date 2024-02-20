================================================================================
Two-Step task
================================================================================

This is an implementation of the well known two-step task :cite:p:`dawModelBasedInfluencesHumans2011`.

The task has often been used to investigate the relationship between model-based and model free reinforcement learning
processes in humans.

In the experiment, we use the starting points of probabilities described in :cite:p:`nussenbaumMovingDevelopmentalResearch2020`,
but with a separate drift. Furthermore, the drift in this implementation is only applied when the choice is selected.
For their implementation of the task, see their GitHub `repo <https://github.com/hartleylabnyu/online_two_step_replication>`_

For this project the graph structure is the following:

.. literalinclude:: ../../rewardgym/tasks/two_step.py
    :language: python
    :lines: 14-22

Or in graph form:

.. plot::

    from rewardgym import get_env
    from rewardgym.environments.visualizations import plot_env_graph
    env, conditions = get_env("two-step")
    plot_env_graph(env)

Task description
********************************************************************************

In this task, participants are asked to make two subsequent decisions.

In the first decision the participant selects between one of two environments,
by pressing either *left* or *right*.

After the selection the participant enters the second environment, where they
make again a *left* or *right* choice between a gamble. The gamble has a
set reward probability at the beginning, but drifts slowly over time.

Because the task has no set conditions, there is only a single starting position
and no further conditions that can be controlled from the outside.



References
********************************************************************************

.. bibliography::
