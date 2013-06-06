from ..lib.drush import DrushAPI
import threading

import sublime
import sublime_plugin


class DrushEvalCommand (sublime_plugin.WindowCommand):
    """
    A command to evaluate arbitrary php code after bootstrapping Drupal
    """

    def run(self):
        sublime.status_message('Evaluating %s' % 'test')
        self.view = self.window.active_view()
        selections = self.view.sel()
        syntax = self.view.settings().get('syntax')
        if 'HTML' in syntax or 'PHP' in syntax:
            for selection in selections:
                code = self.view.substr(selection)
            if code:
                sublime.status_message('Evaluating "%s"' % code)
                thread = DrushEvalThread(self.window, code)
                thread.start()
            else:
                sublime.status_message('You have no text selected. Please '
                                       'select the string you want to evaluate'
                                       ', then try again.')
        else:
            sublime.status_message('Make sure the syntax for your buffer is '
                                   'set to PHP or HTML.')


class DrushEvalThread(threading.Thread):
    """
    A thread to evaluate PHP code.
    """
    def __init__(self, window, code):
        self.window = window
        self.code = code
        threading.Thread.__init__(self)

    def run(self):
        drush_api = DrushAPI()
        self.view = self.window.active_view()
        working_dir = self.view.window().folders()
        drush_api.set_working_dir(working_dir[0])
        args = list()
        args.append(self.code)
        result = drush_api.run_command('php-eval', args, list())
        if result:
            output = self.window.create_output_panel("eval")
            output.run_command('erase_view')
            output.run_command('append', {'characters': result})
            self.window.run_command("show_panel", {"panel": "output.eval"})
        else:
            sublime.status_message('There was an error in running the '
                                   'selection through eval.')
