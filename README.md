subDrush (Sublime Drush plugin)
===============================

This is plugin for Sublime Text 3 (ST3) that exposes a subset of [Drush](https://drupal.org/project/drush) functionality to facilitate Drupal development.

This is not an attempt to bring the entirety of Drush into Sublime Text, which doesn't work very well on a practical level. Instead the idea is that there are some commands that can be executed easily from within ST, such as clearing caches, getting values of variables, enabling or disabling modules and themes, etc. Such commands typically don't require numerous options, don't produce much output for review, and usually do not require additional user input to run. These kinds of commands will be added to subDrush - for other Drush commands, use your terminal.

### Requirements

- [Drush 6](https://drupal.org/project/drush). Drush 5 may work but this plugin is developed against Drush 6.
- Sublime Text 3
- Only Mac OS 10.8 has been tested so far. Linux should be okay, not sure about Windows.

### Installation

Clone this repository into `~/Library/Application Support/Sublime Text 3/Packages/`

### Usage

Open up the command palette (Ctrl + Shift + P), type `drush` to see the commands.

Feel free to create your own [key bindings](http://docs.sublimetext.info/en/latest/reference/key_bindings.html) as none are provided by this plugin.

### Supported Commands

#### Drush

- `cache-clear` (Select a specific cache bin)
- `cache-clear all`
- `watchdog-show` (Displays the 10 most recent watchdog entries)
- `variable-get` (Displays the value associated with a Drupal variable)
- `cron` (Invokes cron for open Drupal directory)
- `php-eval` (Evaluates selected text in the bootstrapped Drupal site)

#### Custom

- `alias-edit` (Edit the Drush alias associated with the open Drupal directory, or choose from a list of all available local Drush aliases)
- `Clear Sublime Drush cache` (Clears Sublime Drush internal cache)

See the [issue queue](https://github.com/kostajh/subDrush/issues) for commands that are in progress.
