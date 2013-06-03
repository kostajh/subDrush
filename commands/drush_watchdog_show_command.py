import threading
from ..lib.drush import DrushAPI

import sublime
import sublime_plugin

class DrushWatchdogShowCommand (sublime_plugin.WindowCommand):

    def run(self):
        self.panel_name = 'watchdog'
        self.window.create_output_panel(self.panel_name)
        self.panel = self.window.get_output_panel('watchdog')
        self.view = self.window.active_view()
        # self.window.run_command("show_panel", {"panel": "output.%s" %
        # self.panel_name})
        test = 'hello'
        self.panel.run_command('drush_watchdog_show_output', {
                               "panel": "output.%s" % test})

    def on_done(self):
        print('done')


class DrushWatchdogShowOutputCommand (sublime_plugin.TextCommand):

    def run(self, edit, output):
        print('test')
        self.view.insert(edit, self.view.size(), output)
        print('running')
