================================================================================
Monetary Incentive Delay Task
================================================================================

This is a reimplementation of the Monetary Incentive Delay task :cite:p:`knutsonFMRIVisualizationBrain2000`,
that is also used in the ABCD study :cite:p:`caseyAdolescentBrainCognitive2018`.

For this project the graph structure is the following:

.. literalinclude:: ../../rewardgym/tasks/mid.py
    :language: python
    :lines: 14-25

Or in graph form:

.. plot::

    from rewardgym import get_env
    from rewardgym.environments.visualizations import plot_env_graph
    env = get_env("mid")
    plot_env_graph(env)

Task description
********************************************************************************

In this task, participants are asked to hit a target in time.

First they are presented with a cue, that indicates the potential win,
or the loss to be avoided.

After a short while, the participant needs to press *space* in time, in response
to a target stimulus.

If the participant's response is in time, they either win or avoid the loss indicated
by the stimulus.

There are 5 cues, two win conditions of different magnitude, a neutral condition with
no outcome and two loss conditions.

As can be seen in the graph, the task is controlled by the ``agent_location``
or ``starting_position`` in that each cueing condition, has a separate graph
structure.

.. bibliography::
   :filter: docname in docnames
