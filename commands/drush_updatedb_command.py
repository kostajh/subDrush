import threading
from ..lib.drush import DrushAPI
from ..lib.thread_progress import ThreadProgress

import sublime
import sublime_plugin


class DrushUpdateDbCommand(sublime_plugin.WindowCommand):
    """
    A command to invoke update-db.
    """

    def run(self):
        self.drush_api = DrushAPI(self.window.active_view())
        self.drupal_root = self.drush_api.get_drupal_root()
        if self.drupal_root is "drush":
            sublime.status_message('Could not invoke update-db as you are not '
                                   'working in a Drupal directory!')
            return
        thread = DrushUpdateDbThread(self.window, self.drush_api)
        thread.start()
        ThreadProgress(thread,
                       'Invoking update-db for %s' % self.drupal_root,
                       "Update.php was successfully run on '%s'" % self.drupal_root)


class DrushUpdateDbThread(threading.Thread):
    """
    A thread to run update-db.
    """
    def __init__(self, window, drush_api):
        self.window = window
        self.drush_api = drush_api
        threading.Thread.__init__(self)

    def run(self):
        updb = self.drush_api.run_command('updatedb', list(), list())

