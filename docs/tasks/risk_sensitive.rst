================================================================================
Risk-Sensitive Decision Making Task
================================================================================

This task is greatly inspired by :cite:t:`nivNeuralPredictionErrors2012` and slightly
adapted towards the second task done in mice described in :cite:t:`dabneyDistributionalCodeValue2020`.

See description below.

For this project the graph structure is the following:

.. literalinclude:: ../../rewardgym/tasks/risk_sensitive.py
    :language: python
    :lines: 18-23

Or in graph form:

.. plot::

    from rewardgym import get_env
    from rewardgym.environments.visualizations import plot_env_graph
    env, conditions = get_env("risk-sensitive")
    plot_env_graph(env)

Task description
********************************************************************************

In this task, participants are asked to either select one of two gambles or
to just select a single forced choice stimulus.

There are currently three gambles in total, with different probabilistic outcomes.

Participants are presented with either a choice, where they select one of two
gambles using *left* or *right* or a single gamble, that they select with *left*.

The graph is controlled by the ``condition`` parameter, that indicates either the
two gambles on display (or a single gamble for that matter).

As can be seen by the graph, the setting here is slightly different than in the
other tasks, in that separate actions are associated with each individual gamble.
In practice the actions (*left* or *right*) are remapped to indicate the selection.

.. bibliography::
   :filter: docname in docnames
