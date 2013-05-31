subDrush
=============

subDrush is plugin for Sublime Text 3 (ST3) that exposes a subset of [Drush](https://drupal.org/project/drush) functionality. This is not an attempt to bring the entirety of Drush into Sublime Text, which doesn't work well conceptually or on a practical level.

Instead the idea is that there are some commands that can be executed easily from within ST, such as clearing caches, getting values of variables, enabling or disabling modules and themes, etc. These commands don't rely on options and don't produce much output, and do not require additional user input to run.

For other Drush commands, use your terminal.

### Requirements

- [Drush 6](https://drupal.org/project/drush)
- Sublime Text 3
- Possibly, Mac OS. Hasn't been tested in Windows. Linux should be fine but please report back if it doesn't work
 
### Installation

Clone this repository into `~/Library/Application Support/Sublime Text 3/Packages/`

### Supported Commands

- Cache Clear (select a specific cache bin)
- Cache Clear All

#### In progress

- Variable Get

#### Planned

- Module/Theme enable/disable
- Watchdog Show
