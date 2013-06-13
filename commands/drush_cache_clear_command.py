import threading
from ..lib.drush import DrushAPI
from ..lib.thread_progress import ThreadProgress

import sublime
import sublime_plugin


class DrushCacheClearCommand(sublime_plugin.WindowCommand):
    """
    A command to clear a specific cache bin.
    """
    quick_panel_command_selected_index = None

    def run(self):
        self.drush_api = DrushAPI(self.window.active_view())
        sublime.status_message('Loading cache bins...')
        self.args = self.drush_api.load_command_args('cache-clear')
        self.window.show_quick_panel(
            self.args, self.command_execution, sublime.MONOSPACE_FONT)

    def command_execution(self, idx):
        thread = DrushCacheClearThread(self.window,
                                       self.args,
                                       idx,
                                       self.drush_api)
        thread.start()
        self.drupal_root = self.drush_api.get_drupal_root()
        if self.drupal_root == self.args[idx]:
            progress_message = "Clearing '%s' cache" % self.args[idx]
            finished_message = "Cleared '%s' cache" % self.args[idx]
        else:
            progress_message = "Clearing '%s' cache for '%s'" % (
                self.args[idx], self.drupal_root)
            finished_message = "Cleared '%s' cache for '%s'" % (
                self.args[idx], self.drupal_root)
        ThreadProgress(thread, progress_message, finished_message)


class DrushCacheClearThread(threading.Thread):
    """
    A thread to clear a specific cache bin.
    """
    def __init__(self, window, args, idx, drush_api):
        self.window = window
        self.args = args
        self.idx = idx
        self.drush_api = drush_api
        threading.Thread.__init__(self)

    def run(self):
        args = list()
        args.append(self.args[self.idx])
        self.drush_api.run_command('cache-clear', args, list())
