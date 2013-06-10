import threading
from ..lib.drush import DrushAPI

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
            sublime.status_message('Executing Drush script...')
            thread = DrushPhpScriptThread(self.window)
            thread.start()
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
        drush_api = DrushAPI()
        self.view = self.window.active_view()
        working_dir = self.view.window().folders()
        drush_api.set_working_dir(working_dir[0])
        file_name = self.view.file_name()
        args = list()
        args.append(file_name)
        result = drush_api.run_command('php-script', args, list())
        if not result:
            sublime.status_message('An error occurred when attempting to '
                                   'execute this script.')
            return
        output = self.window.create_output_panel("script")
        output.set_syntax_file("Packages/Text/Plain Text.tmLanguage")
        output.run_command('erase_view')
        output.run_command('append', {'characters': result})
        self.window.run_command("show_panel", {"panel": "output.script"})
