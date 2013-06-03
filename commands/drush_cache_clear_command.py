class DrushCacheClearCommand (sublime_plugin.WindowCommand):
    """
    A command to clear a specific cache bin.
    """
    quick_panel_command_selected_index = None

    def run(self):
        self.drush_api = DrushAPI()
        self.view = self.window.active_view()
        working_dir = self.view.window().folders()
        self.drush_api.set_working_dir(working_dir[0])
        self.args = self.drush_api.load_command_args('cache-clear')
        self.window.show_quick_panel(
            self.args, self.command_execution, sublime.MONOSPACE_FONT)

    def command_execution(self, idx):
        if drupal_root == self.args[idx]:
            sublime.status_message("Clearing '%s' cache" % self.args[idx])
        else:
            sublime.status_message("Clearing '%s' cache for '%s'" % (
                self.args[idx], self.drush_api.get_drupal_root()))
        thread = DrushCacheClearThread(self.window, self.args, idx)
        thread.start()


class DrushCacheClearThread (threading.Thread):
    """
    A thread to clear a specific cache bin.
    """
    def __init__ (self, window, args, idx):
        self.window = window
        self.args = args
        self.idx = idx
        threading.Thread.__init__(self)

    def run (self) :
        drush_api = DrushAPI()
        drush_api.run_command('cache-clear', self.args[self.idx])
        drupal_root = drush_api.get_drupal_root()
        if drupal_root == self.args[self.idx]:
            sublime.status_message("Cleared '%s' cache" % self.args[self.idx])
        else:
            sublime.status_message("Cleared '%s' cache for '%s'" % (
                self.args[self.idx], drush_api.get_drupal_root()))
