import threading
from ..lib.drush import DrushAPI

import sublime
import sublime_plugin


class DrushWatchdogShowCommand(sublime_plugin.WindowCommand):
    """
    A command to display Drupal's watchdog log.
    """
    def run(self):
        self.view = self.window.active_view()
        window = self.view.window()
        if window:
            self.drush_api = DrushAPI()
            working_dir = self.view.window().folders()
            self.drush_api.set_working_dir(working_dir[0])
            watchdog = self.drush_api.run_command('watchdog-show',
                                                  '')
            if watchdog:
                output = window.create_output_panel("watchdog")
                output.run_command('erase_view')
                output.run_command('insert_view', {'string': watchdog})
                window.run_command("show_panel", {"panel": "output.watchdog"})
