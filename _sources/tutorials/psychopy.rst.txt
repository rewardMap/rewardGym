================================================================================
rewardGym + PsychoPy
================================================================================

The toolbox is build in such a way, that it can also be used from a standalone
installation of PsychoPy (tested only at v2023.2.3 and higher).

Showing stimuli with PsychoPy is recommended for data collection for multiple
reasons.

1. The installation of PsychoPy is often times easier than setting up a new Python environment, especially on different stimulus computers.
2. PsychoPy has been shown to provide a reasonable and accurate report of stimulus and response timings.
3. PsychoPy is probably better known in the cognitive and psychology communities.


Adding stimulus representations
********************************************************************************

The main purpose of providing support for PsychoPy is that rewardGym should also be used for data collection.

Before writing your own loop and functions, I recommend checking out the ``rewardgym_psychopy.py`` file in the root directory.

Adding stimuli works in principle in the same way as in the pygame rendering example by creating an ``info_dict``, which has
entries for every node in the graph. However, this time using "psychopy" as the key. Same as before, we are also using a
list to collate different stimulus representations.


.. code-block:: python

    info_dict = {0: {"pychopy": []}}

rewardGym has some of pre-specified stimulus classes (see the API documentation for more details).

We are going to use four classes for our example from before:

1. :py:meth:`~rewardgym.psychopy_render.stimuli.BaseStimulus`
2. :py:meth:`~rewardgym.psychopy_render.stimuli.TextStimulus`
3. :py:meth:`~rewardgym.psychopy_render.stimuli.ActionStimulus`
4. :py:meth:`~rewardgym.psychopy_render.stimuli.FeedBackStimulus`

The :py:meth:`~rewardgym.psychopy_render.stimuli.BaseStimulus` is simply a flip / update of the window, which could
for example be used to clear the screen again.  :py:meth:`~rewardgym.psychopy_render.stimuli.TextStimulus` and
:py:meth:`~rewardgym.psychopy_render.stimuli.FeedBackStimulus` are text stimuli, where the latter is specially designed
to be used for reward feedback. :py:meth:`~rewardgym.psychopy_render.stimuli.ActionStimulus`, finally indicates that the
program should wait for a user action.


Full example
********************************************************************************

You can find the full worked example under ``notebooks/psychopy_example.py``.

To run it in PsychoPy copy the file to the root directory (it won't work otherwise!).

.. literalinclude :: ../../notebooks/psychopy_example.py
  :language: python
  :linenos:
