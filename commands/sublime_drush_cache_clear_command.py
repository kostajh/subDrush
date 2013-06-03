class SublimeDrushCacheClearCommand (sublime_plugin.WindowCommand):
    """
    A command that clears this plugin's cache.
    """

    def run(self):
        sublime.status_message('Clearing Sublime Drush plugin cache')
        thread = SublimeDrushCacheClearThread()
        thread.start()
        sublime.status_message('Cleared Sublime Drush plugin cache')


class SublimeDrushCacheClearThread (threading.Thread):
    """
    A thread to clear the Sublime Drush plugin cache.
    """

    def run(self):
        sublime_cache_path = sublime.cache_path()
        bin = sublime_cache_path + "/" + "sublime-drush"
        shutil.rmtree(bin)
        os.makedirs(bin)
