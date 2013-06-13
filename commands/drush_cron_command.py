import threading
from ..lib.drush import DrushAPI
from ..lib.thread_progress import ThreadProgress

import sublime
import sublime_plugin


class DrushCronCommand(sublime_plugin.WindowCommand):
    """
    A command to invoke cron.
    """

    def run(self):
        self.drush_api = DrushAPI(self.window.active_view())
        self.drupal_root = self.drush_api.get_drupal_root()
        if self.drupal_root is "drush":
            sublime.status_message('Could not invoke cron as you are not '
                                   'working in a Drupal directory!')
            return
        thread = DrushCronThread(self.window, self.drush_api)
        thread.start()
        ThreadProgress(thread,
                       'Invoking cron for %s' % self.drupal_root,
                       "Cron was successfully run on '%s'" % self.drupal_root)


class DrushCronThread(threading.Thread):
    """
    A thread to clear all caches
    """
    def __init__(self, window, drush_api):
        self.window = window
        self.drush_api = drush_api
        threading.Thread.__init__(self)

    def run(self):
        self.drush_api.run_command('cron', list(), list())
