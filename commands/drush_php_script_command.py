import threading
from ..lib.drush import DrushAPI
from ..lib.thread_progress import ThreadProgress
from ..lib.output import Output

import sublime
import sublime_plugin


class DrushPhpScriptCommand (sublime_plugin.WindowCommand):
    """
    A command to execute the active view as a Drush script.
    """

    def run(self):
        self.view = self.window.active_view()
        syntax = self.view.settings().get('syntax')
        if 'HTML' in syntax or 'PHP' in syntax:
            thread = DrushPhpScriptThread(self.window)
            thread.start()
            ThreadProgress(thread,
                           'Executing Drush script',
                           'Done executing Drush script')
        else:
            sublime.status_message('Make sure the syntax for your files is set'
                                   ' to PHP or HTML.')


class DrushPhpScriptThread(threading.Thread):
    """
    A thread to execute the active view as a Drush script.
    """
    def __init__(self, window):
        self.window = window
        threading.Thread.__init__(self)

    def run(self):
        self.view = self.window.active_view()
        drush_api = DrushAPI(self.view)
        file_name = self.view.file_name()
        args = list()
        args.append(file_name)
        result = drush_api.run_command('php-script', args, list())
        if not result:
            sublime.status_message('An error occurred when attempting to '
                                   'execute this script.')
            return
        Output(self.window, 'script', 'Text', result).render()
