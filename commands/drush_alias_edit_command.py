from ..lib.drush import DrushAPI
from os.path import expanduser

import sublime
import sublime_plugin


class DrushAliasEditCommand(sublime_plugin.WindowCommand):
    """
    A command to edit the alias associated with the current
    working directory.
    """
    quick_panel_command_selected_index = None

    def run(self):
        self.drush_api = DrushAPI()
        self.view = self.window.active_view()
        working_dir = self.view.window().folders()
        self.drush_api.set_working_dir(working_dir[0])
        self.drupal_root = self.drush_api.get_drupal_root()
        alias_id = self.drush_api.get_site_alias_from_drupal_root(
            self.drupal_root)
        if not alias_id:
            # Load all local aliases
            self.aliases = self.drush_api.get_local_site_aliases()
            self.window.show_quick_panel(
                self.aliases, self.command_execution, sublime.MONOSPACE_FONT)
        else:
            filename = expanduser("~") + '/.drush/' + alias_id \
                + ".aliases.drushrc.php"
            self.window.open_file(filename)
            sublime.status_message('Loaded %', filename)

    def command_execution(self, idx):
        filename = expanduser("~") + '/.drush/' + self.aliases[idx].replace(
            '@', '') + ".aliases.drushrc.php"
        self.window.open_file(filename)
        sublime.status_message('Loaded %', filename)
