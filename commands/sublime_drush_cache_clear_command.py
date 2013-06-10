import threading
import os
import shutil
from ..lib.thread_progress import ThreadProgress

import sublime
import sublime_plugin


class SublimeDrushCacheClearCommand (sublime_plugin.WindowCommand):
    """
    A command that clears this plugin's cache.
    """

    def run(self):
        thread = SublimeDrushCacheClearThread()
        thread.start()
        ThreadProgress(thread,
                       'Clearing Sublime Drush plugin cache',
                       'Cleared Sublime Drush plugin cache')


class SublimeDrushCacheClearThread (threading.Thread):
    """
    A thread to clear the Sublime Drush plugin cache.
    """

    def run(self):
        sublime_cache_path = sublime.cache_path()
        bin = sublime_cache_path + "/" + "sublime-drush"
        shutil.rmtree(bin)
        os.makedirs(bin)
