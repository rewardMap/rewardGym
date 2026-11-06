.. rewardGym documentation master file, created by
   sphinx-quickstart on Wed Feb  7 15:25:01 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root ``toctree`` directive.

Welcome to rewardGym's documentation!
=====================================

.. relativeinclude:: ../README.rst

docs/

.. toctree::
   :maxdepth: 2
   :caption: Walkthrough

   tutorials/tutorial
   tutorials/psychopy.rst

.. toctree::
   :maxdepth: 2
   :caption: Deep Dive

   deepdive/graph_structure.rst
   deepdive/psychopy_stimuli.rst
   deepdive/controlling_experiments.rst
   deepdive/what_is_run_task.rst
   deepdive/writing_agents.rst

.. toctree::
   :maxdepth: 2
   :caption: Tasks
   :glob:

   tasks/*

.. toctree::
   :maxdepth: 3
   :caption: (limited) API reference

   api/environments.rst
   api/psychopy_stimuli.rst


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
