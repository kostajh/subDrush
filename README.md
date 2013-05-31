subDrush
=============

subDrush is plugin for Sublime Text 3 (ST3) that exposes a subset of [Drush](http://drush.ws) functionality. The idea is that there are some commands that can and should be executed from within ST, such as clearing caches, getting values of variables, downloading modules, and enabling or disabling modules. For other Drush commands, use your terminal.

### Requirements

- [Drush 6](http://drush.ws).
- Possibly, Mac OS. Hasn't been tested in Windows. Linux should be fine but please report back if it doesn't work.
 
### Installation

Clone this repository into ~/Library/Application Support/Sublime Text 3/Packages.

### Supported Commands

- Cache Clear (select a specific cache bin)
- Cache Clear All

#### In progress

- Variable Get
- Download

#### Planned

- Module/Theme enable/disable
- Watchdog Show
