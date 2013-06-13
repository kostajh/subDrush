import threading
from ..lib.drush import DrushAPI
from ..lib.thread_progress import ThreadProgress

import sublime
import sublime_plugin


class DrushWatchdogShowCommand(sublime_plugin.WindowCommand):
    """
    A command to display Drupal's watchdog log.
    """
    def run(self):
        thread = DrushWatchdogShowThread(self.window)
        thread.start()
        ThreadProgress(thread,
                       'Loading watchdog entries',
                       'Loaded watchdog entries')


class DrushWatchdogShowThread(threading.Thread):
    """
    A thread to return watchdog entries.
    """
    def __init__(self, window):
        self.window = window
        threading.Thread.__init__(self)

    def run(self):
        drush_api = DrushAPI(self.window.active_view())
        watchdog = drush_api.run_command('watchdog-show', list(), list())
        if not watchdog:
            sublime.status_message('Could not find a Drupal directory')
            return
        sublime.status_message('Loaded 10 most recent watchdog entries')
        if watchdog:
            output = self.window.create_output_panel("watchdog")
            output.set_syntax_file("Packages/Text/Plain Text.tmLanguage")
            output.run_command('erase_view')
            output.run_command('append', {'characters': watchdog})
            self.window.run_command("show_panel", {"panel": "output.watchdog"})
