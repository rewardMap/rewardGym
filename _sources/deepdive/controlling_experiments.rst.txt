================================================================================
Controlling the experiment
================================================================================

There are multiple ways to control the experiments when you are using the main
function for stimulus displays ``rewardgym_psychopy.py`` in the root directory
or when you want to use :py:func:`rewardgym.psychopy_core.run_task`.

All controls are added to a settings dictionary.

Controlling timing
================================================================================

To controlling timings is relatively straight forward. In the settings dictionary
you will need to add a ``update`` entry, which is a list, and could include the
names of the stimulus objects you want to update. Furthermore, there should be an
entry of with the same name, again a list, which is the same length as the number
of trials in the experiment.

For example, if you want to update a stimulus with the name of ``isi`` you would
add "iti" to the ``settings["update"] = ["iti"]`` and a list of timings. For example,
if it would be only 5 trials, it could look like this ``settings["isi"] = [0.6, 0.4, 0.6, 0.4, .05]``.

Controlling Conditions
================================================================================

Controlling conditions is a bit more complicated, as it requires overwriting
some parts of the graph structure.

Let's use the MID task as an example, you would create the 5 different conditions.
As this graph uses a ``skip`` step in the first condition, we are simply going
to overwrite what each action leads to. E.g. here in the first state (0), the
issued actions (0) leads to state 1, 2, etc.

.. code-block:: python

    condition_dict = {
        "loss-large": {0: {0: 1}},
        "loss-small": {0: {0: 2}},
        "neutral": {0: {0: 3}},
        "win-small": {0: {0: 4}},
        "win-large": {0: {0: 5}},
    }

You would then add this ``condition_dict`` to the ``settings`` dictionary:
``settings["condition_dict"] = condition_dict`` and you can now add a list of
strings (i.e. the keys to the dictionary - "neutral", etc.) to the dictionary
``settings["condition"] = ["neutral", "win-small"]``. The condition will then
be used in the main loops and applied to the given trial, the name of the
condition will also be logged as "trial_type".
