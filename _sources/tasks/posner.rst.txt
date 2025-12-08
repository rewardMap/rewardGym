================================================================================
Spatial-Cueing / Posner Task
================================================================================

This is not a typical reward related learning task, but rather a task from visual attention :cite:p:`posnerOrientingAttention1980`.

In this task, rather than learning reward contingencies the participant learns the validity of a pre-cue.

.. literalinclude:: ../../rewardgym/tasks/posner.py
    :language: python
    :lines: 16-23

Or in graph form:

.. plot::

    from rewardgym import get_env
    from rewardgym.environments.visualizations import plot_env_graph
    env = get_env("posner")
    plot_env_graph(env)

Task description
********************************************************************************

In this task, participants are asked to attend a central fixation cross,
after a while a central pre-cue appears, indicating the likely location of the
next target stimulus. Participants are then asked to indicate the side the
target stimulus appeared, pressing either *left* or *right*.

If they are correct, they get a reward.

As can be seen in the graph, the task is controlled by the ``agent_location``
or ``starting_position`` in that each cueing condition, has a separate graph
structure.

.. bibliography::
   :filter: docname in docnames
