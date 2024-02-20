================================================================================
Human Connectome Project Gambling Task
================================================================================

This is a reimplementation of the HCP's gambling task :cite:p:`delgadoTrackingHemodynamicResponses2000`.

For this project the graph structure is the following:

.. literalinclude:: ../rewardgym/tasks/hcp.py
    :language: python
    :lines: 14-18

Or in graph form:

.. plot::

    from rewardgym import get_env
    from rewardgym.environments.visualizations import plot_env_graph
    env, conditions = get_env("hcp")
    plot_env_graph(env)

Task description
********************************************************************************

In this task, participants are asked to make a gamble: Is the next card larger
or less than five?

The participant indicates their choice by pressing either *left* (lower) or *right*
(larger than five).

After the selection a card is drawn and the participant is presented with the outcome.
They gain a reward of 1, if they were correct, 0 if the card is 5 or -0.5 if their choice
was incorrect.

Unbeknownst to the participant, the outcome is rigged. The experimenter is able to manipulate
the number of wins or losses over time.

In this environment, this is controlled via the condition variable.

The value can be 0 = loss, 1 = neutral, and 2 = win.

In the original experiment and the Human Connectome Project, there are two blocks
of the experiment, where participant either win more or lose more. By contrasting
the neural activity in the blocks, one can localize brain regions related to punishment
or reward.



References
********************************************************************************

.. bibliography::
