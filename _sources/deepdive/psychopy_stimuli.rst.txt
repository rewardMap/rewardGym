================================================================================
PsychoPy Stimuli
================================================================================

Stimuli based on PsychoPy play a special role in rewardGym, as they allow for both
stimulation, fine control over timing, logging and simulation of experiments.

See some examples :doc:`../api/psychopy_stimuli`,
which can be accessed via the :py:mod:`rewardgym.psychopy_render.stimuli` module.

These stimuli are added to the environment as a list, so that at each state a number
of stimuli are displayed after another. Typically ending in an :py:class:`rewardgym.psychopy_render.stimuli.ActionStimulus`.


The Stimulus Class
================================================================================

The stimulus class has three main methods: ``setup``, ``display``, and ``simulate``.


Setup
********************************************************************************

The role of the ``setup`` method is to instantiate the different PsychoPy objects,
that are used for displaying stimuli on the screen. In principle, this
method should only take the current ``window`` object as an argument.

All properties of the PsychoPy objects to be displayed (filenames, images, text, etc.)
should be added to the class during ``__init__``.


Display
********************************************************************************

The ``display`` method is used by the :py:class:`rewardgym.environments.psychopy_env`,
to render the stimuli onto the display.

The display method inside the environment has access to:

* the current window object
* the current logger object
* the current condition
* the total reward
* the current reward
* the current location of the agent
* and the action issued previously


Simulate
********************************************************************************

Finally, there's the ``simulate`` method, which mirrors the ``display`` method.
This is used to simulate full log files. In many cases you can use ``simulate``
method inherited from the :py:class:`rewardgym.psychopy_render.stimuli.BaseStimulus`,
class.
