import threading
from ..lib.drush import DrushAPI

import sublime
import sublime_plugin


class DrushCacheClearAllCommand(sublime_plugin.WindowCommand):
    """
    A command that clears all caches.
    """
    def run(self):
        sublime.status_message('Clearing all caches')
        thread = DrushCacheClearAllThread(self.window)
        thread.start()


class DrushCacheClearAllThread(threading.Thread):
    """
    A thread to clear all caches.
    """
    def __init__(self, window):
        self.window = window
        threading.Thread.__init__(self)

    def run(self):
        drush_api = DrushAPI()
        self.view = self.window.active_view()
        working_dir = self.view.window().folders()
        drush_api.set_working_dir(working_dir[0])
        drupal_root = drush_api.get_drupal_root()
        drush_api.run_command('cache-clear', 'all')
        sublime.status_message("Cleared all caches for '%s'" % drupal_root)
