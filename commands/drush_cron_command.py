import threading
from ..lib.drush import DrushAPI

import sublime
import sublime_plugin


class DrushCronCommand(sublime_plugin.WindowCommand):
    """
    A command to invoke cron.
    """

    def run(self):
        self.drush_api = DrushAPI()
        self.view = self.window.active_view()
        working_dir = self.view.window().folders()
        self.drush_api.set_working_dir(working_dir[0])
        self.drupal_root = self.drush_api.get_drupal_root()
        if self.drupal_root is "drush":
            sublime.status_message('Could not invoke cron as you are not '
                                   'working in a Drupal directory')
            return
        sublime.status_message('Invoking cron...')
        thread = DrushCronThread(self.window)
        thread.start()


class DrushCronThread(threading.Thread):
    """
    A thread to clear all caches
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
        drush_api.run_command('cron', '')
        sublime.status_message("Cron was invokved for '%s'" % drupal_root)
