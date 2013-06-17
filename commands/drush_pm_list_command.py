import threading
from ..lib.drush import DrushAPI
from ..lib.thread_progress import ThreadProgress
from ..lib.output import Output

import sublime
import sublime_plugin


class DrushPmListCommand(sublime_plugin.WindowCommand):
    """
    Implements `drush pm-list` command.
    """
    def run(self):
        thread = DrushPmListThread(self.window)
        thread.start()
        ThreadProgress(thread,
                       'Loading project information',
                       'Loaded project information')


class DrushPmListThread(threading.Thread):
    """
    A thread to return info from `drush pm-list` and output it.
    """

    def __init__(self, window):
        self.window = window
        threading.Thread.__init__(self)

    def run(self):
        drush_api = DrushAPI(self.window.active_view())
        options = list()
        options.append('--format=yaml')
        pm_list = drush_api.run_command('pm-list', list(), options)
        if not pm_list:
            sublime.status_message('Could not find a Drupal directory!')
            return
        Output(self.window, 'pm-list', 'YAML', pm_list).renderWindow()
