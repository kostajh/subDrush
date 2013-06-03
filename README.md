subDrush
=============

subDrush is plugin for Sublime Text 3 (ST3) that exposes a subset of [Drush](https://drupal.org/project/drush) functionality.

This is not an attempt to bring the entirety of Drush into Sublime Text, which doesn't work well conceptually or on a practical level. Instead the idea is that there are some commands that can be executed easily from within ST, such as clearing caches, getting values of variables, enabling or disabling modules and themes, etc. These commands typically don't require numerous options, don't produce much output for review, and do not require additional user input to run. These kinds of commands will be added to subDrush - for other Drush commands, use your terminal.

### Requirements

- [Drush 6](https://drupal.org/project/drush)
- Sublime Text 3
- Only Mac OS 10.8 has been tested so far. Linux should be okay, not sure about Windows.
 
### Installation

Clone this repository into `~/Library/Application Support/Sublime Text 3/Packages/`

### Supported Commands

- `cache-clear` (select a specific cache bin)
- `cache-clear all`

#### In Progress

- `variable-get`

#### Planned

- `cron`
- `test-run`
- `pm-enable` and `pm-disable`
- `reinstall` (`pm-disable && pm-uninstall && pm-enable`)
- `php-script` and `eval`
- `watchdog-show`
