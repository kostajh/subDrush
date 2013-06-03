import threading
import json
from ..lib.drush import DrushAPI
import pprint

import sublime
import sublime_plugin


class DrushVariableGetCommand (sublime_plugin.WindowCommand):
    """
    A command to return the value of a Drupal variable.
    """
    quick_panel_command_selected_index = None

    def run(self):
        sublime.status_message('Loading variables')
        self.drush_api = DrushAPI()
        self.view = self.window.active_view()
        working_dir = self.view.window().folders()
        self.drush_api.set_working_dir(working_dir[0])
        variables = self.drush_api.run_command('variable-get', '--format=json')
        if not variables:
            sublime.status_message('No variables were found. Make sure you \
            " are working in a Drupal directory.')
            return
        sublime.status_message('Loaded variables. Select one to display its \
            " value in the output panel.')
        variable_data = json.loads(variables)
        variables = []
        for key, value in variable_data.items():
            desc = "Array"
            if (type(value) is str) and (type(key) is str):
                desc = value
            variables.append([key, desc])
        self.args = variables
        self.window.show_quick_panel(
            variables, self.command_execution, sublime.MONOSPACE_FONT)

    def command_execution(self, idx):
        variable = self.drush_api.run_command('variable-get',
                                              self.args[idx][0])
        window = self.view.window()
        if window:
            output = window.create_output_panel("variable_get")
            output.run_command('erase_view')
            output.run_command('insert_view', {'string': variable})
            window.run_command("show_panel", {"panel": "output.variable_get"})
