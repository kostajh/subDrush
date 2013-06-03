subDrush (Sublime Drush plugin)
===============================

subDrush is plugin for Sublime Text 3 (ST3) that exposes a subset of [Drush](https://drupal.org/project/drush) functionality.

This is not an attempt to bring the entirety of Drush into Sublime Text, which doesn't work very well on a practical level. Instead the idea is that there are some commands that can be executed easily from within ST, such as clearing caches, getting values of variables, enabling or disabling modules and themes, etc. Such commands typically don't require numerous options, don't produce much output for review, and do not require additional user input to run. These kinds of commands will be added to subDrush - for other Drush commands, use your terminal.

### Requirements

- [Drush 6](https://drupal.org/project/drush). Drush 5 may work but this plugin is developed against Drush 6.
- Sublime Text 3
- Only Mac OS 10.8 has been tested so far. Linux should be okay, not sure about Windows.

### Installation

Clone this repository into `~/Library/Application Support/Sublime Text 3/Packages/`

### Supported Commands

- `cache-clear` (Select a specific cache bin)
- `cache-clear all`
- `watchdog-show` (Displays the 10 most recent watchdog entries)
- `variable-get` (Displays the value associated with a Drupal variable)

#### Planned

- `cron`
- `test-run`
- `pm-enable` and `pm-disable`
- `reinstall` (`pm-disable && pm-uninstall && pm-enable`)
- `php-script` and `eval`
