import threading
from ..lib.drush import DrushAPI

import sublime
import sublime_plugin


class DrushCacheClearCommand(sublime_plugin.WindowCommand):
    """
    A command to clear a specific cache bin.
    """
    quick_panel_command_selected_index = None

    def run(self):
        self.drush_api = DrushAPI()
        self.view = self.window.active_view()
        working_dir = self.view.window().folders()
        self.drush_api.set_working_dir(working_dir[0])
        self.drupal_root = self.drush_api.get_drupal_root()
        self.args = self.drush_api.load_command_args('cache-clear')
        self.window.show_quick_panel(
            self.args, self.command_execution, sublime.MONOSPACE_FONT)

    def command_execution(self, idx):
        if self.drupal_root == self.args[idx]:
            sublime.status_message("Clearing '%s' cache" % self.args[idx])
        else:
            sublime.status_message("Clearing '%s' cache for '%s'" % (
                self.args[idx], self.drupal_root))
        thread = DrushCacheClearThread(self.window,
                                       self.args,
                                       idx,
                                       self.drush_api,
                                       self.drupal_root)
        thread.start()


class DrushCacheClearThread(threading.Thread):
    """
    A thread to clear a specific cache bin.
    """
    def __init__(self, window, args, idx, drush_api, drupal_root):
        self.window = window
        self.args = args
        self.idx = idx
        self.drush_api = drush_api
        self.drupal_root = drupal_root
        threading.Thread.__init__(self)

    def run(self):
        args = list()
        args.append(self.args[self.idx])
        self.drush_api.run_command('cache-clear', args, list())
        if self.drupal_root == self.args[self.idx]:
            sublime.status_message("Cleared '%s' cache" % self.args[self.idx])
        else:
            sublime.status_message("Cleared '%s' cache for '%s'" % (
                self.args[self.idx], self.drupal_root))
