import json
import threading
from ..lib.drush import DrushAPI
from ..lib.thread_progress import ThreadProgress

import sublime
import sublime_plugin


class DrushVariableGetCommand(sublime_plugin.WindowCommand):
    """
    A command to return the value of a Drupal variable.
    """
    quick_panel_command_selected_index = None

    def run(self):
        self.drush_api = DrushAPI(self.window.active_view())
        thread = DrushVariableGetAllThread(self.window,
                                           self.drush_api)
        thread.start()
        ThreadProgress(thread,
                       'Loading defined variables',
                       'Loaded variables. Select one to display its'
                       ' value in the output panel.')


class DrushVariableGetAllThread(threading.Thread):
    """
    A thread to return a list of all variables.
    """
    def __init__(self, window, drush_api):
        self.window = window
        self.drush_api = drush_api
        threading.Thread.__init__(self)

    def run(self):
        args = list()
        options = list()
        options.append('--format=json')
        variables = self.drush_api.run_command('variable-get', args, options)
        if not variables:
            sublime.status_message('No variables were found. Make sure you'
                                   ' are working in a Drupal directory.')
            return
        variable_data = json.loads(variables)
        self.variables = []
        for key, value in variable_data.items():
            desc = "Array"
            if (type(value) is str) and (type(key) is str):
                desc = value
            self.variables.append([key, desc])

        self.window.show_quick_panel(self.variables,
                                     self.command_execution,
                                     sublime.MONOSPACE_FONT)

    def command_execution(self, idx):
        thread = DrushVariableGetThread(self.window,
                                        self.variables,
                                        idx,
                                        self.drush_api)
        thread.start()
        ThreadProgress(thread,
                       'Retrieving value of variable "%s"' %
                       self.variables[idx][0],
                       'Retrieved value of variable "%s"' %
                       self.variables[idx][0])


class DrushVariableGetThread(threading.Thread):
    """
    A thread to return the value of a variable.
    """
    def __init__(self, window, args, idx, drush_api):
        self.window = window
        self.args = args
        self.idx = idx
        self.drush_api = drush_api
        threading.Thread.__init__(self)

    def run(self):
        args = list()
        args.append(self.args[self.idx][0])
        options = list()
        options.append('--pipe')
        variable = self.drush_api.run_command('variable-get', args, options)
        window = self.window
        if window:
            output = window.create_output_panel("variable_get")
            output.set_syntax_file("Packages/PHP/PHP.tmLanguage")
            output.run_command('erase_view')
            output.run_command('append', {'characters': "<?php\n"})
            output.run_command('append', {'characters': variable})
            window.run_command("show_panel", {"panel": "output.variable_get"})
