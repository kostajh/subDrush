import threading
from ..lib.drush import DrushAPI

import sublime
import sublime_plugin


class DrushWatchdogShowCommand(sublime_plugin.WindowCommand):
    """
    A command to display Drupal's watchdog log.
    """
    def run(self):
        sublime.status_message('Loading watchdog entries...')
        thread = DrushWatchdogShowThread(self.window)
        thread.start()


class DrushWatchdogShowThread(threading.Thread):
    """
    A thread to return watchdog entries.
    """
    def __init__(self, window):
        self.window = window
        threading.Thread.__init__(self)

    def run(self):
        drush_api = DrushAPI()
        self.view = self.window.active_view()
        working_dir = self.view.window().folders()
        drush_api.set_working_dir(working_dir[0])
        watchdog = drush_api.run_command('watchdog-show', list(), list())
        if not watchdog:
            sublime.status_message('Could not find a Drupal directory')
            return
        sublime.status_message('Loaded 10 most recent watchdog entries')
        if watchdog:
            output = self.window.create_output_panel("watchdog")
            output.run_command('erase_view')
            output.run_command('append', {'characters': watchdog})
            self.window.run_command("show_panel", {"panel": "output.watchdog"})
