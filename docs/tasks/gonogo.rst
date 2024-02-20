================================================================================
Monetary Incentive Delay Task
================================================================================

This is a reimplementation of the Go / No-Go task described in :cite:p:`guitart-masipGoNogoLearning2012`.


For this project the graph structure is the following:

.. literalinclude:: ../../rewardgym/tasks/gonogo.py
    :language: python
    :lines: 16-25

Or in graph form:

.. plot::

    from rewardgym import get_env
    from rewardgym.environments.visualizations import plot_env_graph
    env, conditions = get_env("gonogo")
    plot_env_graph(env)

Task description
********************************************************************************

In this task, participants are asked to respond to a target in time, or to
withhold their response.


First they are presented with a cue, the condition and response-type. There are
two conditions: punishment or reward and two response-types go or no-go.

After the cue the participant needs to press *space* in response
to a target stimulus, or to withhold their response.

Depending on their action, the participant receives a probabilistic reward, or
probabilistic punishment.

As can be seen in the graph, the task is controlled by the ``agent_location``
or ``starting_position`` in that each cueing condition, has a separate graph
structure.

References
********************************************************************************

.. bibliography::
