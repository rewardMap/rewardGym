================================================================================
Graph structure
================================================================================

At its core rewardGym uses a graph structure to represent environments and tasks.
There are multiple possible representations at different complexities.

The core representation is the same across experiments:

* Nodes represent states of the environment.
* Edges represent different actions.
* There is usually one or more starting nodes, which represent the condition.
* There is usually an end node, which is associated with a reward.


The basic graph
================================================================================

A basic graph could be the following:

.. code-block:: python
  graph = {0 : [1, 2], 1 : [], 2 : []}

Here we have the starting node ``0`` which presupposes two actions. Each of these
actions lead to a terminal state (indicated by the empty lists).

An important consideration for this graph structure is, that the actions are simply numbered.
I.e. action ``0`` would lead to node ``1`` and action ``1`` would lead to node ``2``.

This representation is already powerful enough to create experiments, such as the :doc:`tasks/hcp` task
or a two-arm bandit task :doc:`tutorials/tutorial`.


Adding probabilistic transitions
================================================================================

If we want to add some randomness to the action selection, we can introduce and
indicator for probabilistic choosing, using a tuple:

.. code-block:: python
  graph = {0: ([1, 2], 0.7), 1 : [], 2 :[]}

In this case the tuple for state ``0: ([1, 2], 0.7)`` indicates that action ``0``
selects state ``1`` in 70% of the cases and any other state (here that is only ``2``)
in 30 % of the cases. Similarly, action ``1`` selects state ``2`` in 70 % of the cases
and any other state with 30 % probability.

One could use this functionality to uniformly draw form a series of possible outcome states.

.. code-block:: python
  graph = {0: ([1, 2, 3, 4, 5], 0.2), 1: [], 2: [], 3: [], 4: [], 5: []}

In this example, any of the 5 possible actions (0 - 4) will lead to a random new state.
An action (e.g. ``0``) leads to the selected outcome (``1``) in only 20 % of the case, in the remaining 80 % of cases
a random state of the remaining list (``[2, 3, 4, 5]``) will be drawn with uniform probability.


Using the complete graph structure
================================================================================

RewardGym uses a more detailed graph structure under the hood, which allows for
greater controllability (e.g. in experiments).

Instead of associating a node only with a list of possible outcomes or a tuple of outcomes
and probabilities, a node is can be associated with a dictionary.

.. code-block:: python
  graph = {0: {0: 1, 1 : 2}, 1 : {}, 2 : {}}

Here we are reiterating the first example, but how it would look like in the internal
representation.
The first node is associated with a dictionary, that explicitly states which action leads to which
terminal state.

For even more complex examples, this would be the full graph representation of the
two-step task.

.. code-block:: python

  graph = {0: {0: ([1, 2], 0.7), 1: ([2, 1], 0.7)},
          1: {0: 3, 1: 4},
          2: {0: 5, 1: 6},
          3: {},
          4: {},
          5: {},
          6: {}}

As you can see each of the probabilistic nodes explicitly states, which action
leads with 70 % probability to which state (see the order of the possible endpoints).

In practice, you will not often use the full structure or only use it for very
specific nodes. If necessary, you can call the static method of the ``BaseEnv``
class ``_unpack_graph`` to create the full graph structure for you graph.


Utilizing skip connections
================================================================================

You can also decide to skip certain connections, for example to use a primary node
only for selecting the tasks current condition.

This is done by using the ``skip`` argument.

.. code-block:: python
  graph = {0: {0: ([1, 2], 0.5), 'skip': True}, 1 : {}, 2 : {}}

Adding ``skip`` to the graph tells the environment class to automatically jump to
the next state, pretending to have pressed the indicated key (here ``0``).
Essentially, this example would let you start in states ``1`` or ``2``, with even
probability.
