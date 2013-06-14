import threading
from ..lib.drush import DrushAPI
from ..lib.thread_progress import ThreadProgress

import sublime_plugin


class DrushStatusCommand(sublime_plugin.WindowCommand):
    """
    Implements the `drush core-status` command.
    """

    def run(self):
        self.drush_api = DrushAPI(self.window.active_view())
        thread = DrushStatusThread(self.window, self.drush_api)
        thread.start()
        drupal_root = self.drush_api.get_drupal_root()
        ThreadProgress(thread,
                       "Returning status information for '%s'" % drupal_root,
                       "Returned status information for '%s'" % drupal_root
                       )


class DrushStatusThread(threading.Thread):
    """
    A thread to run `drush core-status`.
    """
    def __init__(self, window, drush_api):
        self.drush_api = drush_api
        self.window = window
        threading.Thread.__init__(self)

    def run(self):
        options = list()
        options.append('--format=yaml')
        status = self.drush_api.run_command('core-status', list(), options)
        print(status)
        if status:
            output = self.window.create_output_panel("core-status")
            output.set_syntax_file("Packages/YAML/YAML.tmLanguage")
            output.run_command('erase_view')
            output.run_command('append', {'characters': status})
            self.window.run_command("show_panel",
                                    {"panel": "output.core-status"})
