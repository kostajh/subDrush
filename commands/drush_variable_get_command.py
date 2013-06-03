import threading
from ..lib.drush import DrushAPI

import sublime
import sublime_plugin

class DrushVariableGetCommand (sublime_plugin.WindowCommand):
    """
    A command to return the value of a Drupal variable.
    """
    quick_panel_command_selected_index = None

    def run(self):
        global args
        global drush
        drush_api = DrushAPI()
        self.view = self.window.active_view()
        working_dir = self.view.window().folders()
        drush_api.set_working_dir(working_dir[0])
        variable_data = json.loads(drush_api.run_command(
            'variable-get', '--format=json'))
        variables = []
        for key, value in variable_data.items():
            if (type(value) is str) and (type(key) is str):
                variables.append([key, value])
        self.args = variables
        self.window.show_quick_panel(
            variables, self.command_execution, sublime.MONOSPACE_FONT)

    def command_execution(self, idx):
        global args
        global drush_api
        drush_api.run_command('variable-get', self.args[idx][0])
