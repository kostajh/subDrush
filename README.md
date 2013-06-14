subDrush (Sublime Drush plugin)
===============================

This is plugin for Sublime Text 3 (ST3) that exposes a subset of [Drush](https://drupal.org/project/drush) functionality to facilitate Drupal development.

This is not an attempt to bring the entirety of Drush into Sublime Text. Instead the idea is that there are some commands that can be executed easily from within ST, such as clearing caches, getting values of variables, enabling or disabling modules and themes, etc. Such commands typically don't require numerous options and usually do not require additional user input to run. These kinds of commands will be added to subDrush - for other Drush commands, use your terminal.

### Supported Commands

| Command                     | Description                                               | Type   |
|-----------------------------|-----------------------------------------------------------|--------|
| `cache-clear`               | Clear a specific cache bin                                | core   |
| `cache-clear all`           | Clear all caches                                          | core   |
| `core-status`               | Provides a birds-eye view of the Drupal installation      | core   |
| `watchdog-show`             | Displays the 10 most recent watchdog entries              | core   |
| `variable-get`              | Displays the value of a Drupal variable                   | core   |
| `cron`                      | Invokes cron for open Drupal directory                    | core   |
| `php-eval`                  | Evaluates selected text in the bootstrapped Drupal site   | core   |
| `php-script`                | Executes open buffer as PHP script after Drupal bootstrap | core   |
| `alias-edit`                | Edit the Drush aliases (current site or choose from list) | custom |
| `Clear Sublime Drush cache` | Clears Sublime Drush internal cache                       | custom |

See the [issue queue](https://github.com/kostajh/subDrush/issues) for commands that are in progress.

### Usage

This plugin works best when you have a Drupal directory open in ST3, or a directory immediately below your Drupal root. This allows subDrush to know about the local Drupal environment, and lets you interact with the local Drupal site's database.

For example, suppose your site directory structure looks like this:

    /path/to/repo/docroot   <-- Where Drupal core is
    /path/to/repo/resources <-- Miscellaneous scripts
    /path/to/repo/tests     <-- Any tests you've written, etc

In Sublime Text 3, if you go to File -> Open and open up `/path/to/repo` or `/path/to/repo/docroot` this plugin will work fine, and will be able to accurately identify the Drupal root to pass to Drush.

If you want, you can also open a single file in ST3 (for example, `/path/to/repo/docroot/modules/color/color.module`), and subDrush will identify the Drupal root by using the `drush dd` command.

Open up the command palette (Ctrl + Shift + P), type `drush` to see the commands.

Feel free to create your own [key bindings](http://docs.sublimetext.info/en/latest/reference/key_bindings.html) as none are provided by this plugin.

### Requirements

- [Drush 6](https://drupal.org/project/drush). Drush 5 may work but this plugin is developed against Drush 6.
- Sublime Text 3 (Build 3033 or later)
- Only Mac OS 10.8 has been tested so far. Linux and Windows should work fine though.

### Installation

Clone this repository into `~/Library/Application Support/Sublime Text 3/Packages/`

### Credits

This plugin was written and is maintained by [Kosta Harlan](http://kostaharlan.net) with support from [DesignHammer Media Group](http://www.designhammer.com).

The ThreadProgress class is borrowed from [wbond's](https://github.com/wbond) [Sublime Package Control](https://github.com/wbond/sublime_package_control) plugin.

### License

A Sublime Text 3 Plugin that integrates with Drush
Copyright (C) 2013 Kosta Harlan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
