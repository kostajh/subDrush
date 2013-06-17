import sublime
import sublime_plugin


class Output(object):
    """
    This class displays output returned from a subDrush command.
    All parameters are required.
    """

    def __init__(self, window, command, syntax, output):
        self.window = window
        self.command = command
        self.view = self.window.active_view()
        self.output_panel = self.window.create_output_panel(self.command)
        self.output_panel.run_command('erase_view')
        self.syntax = self.get_syntax_file(syntax)
        self.output_panel.set_syntax_file(self.syntax)
        self.output = output

    def render(self):
        """
        Create an output panel and display the output.
        """
        self.output_panel.run_command('append', {'characters': self.output})
        self.window.run_command("show_panel",
                                {"panel": "output.%s" % self.command})

    def get_syntax_file(self, syntax):
        """
        Return a valid syntax file.
        """
        if syntax is 'YAML':
            return "Packages/YAML/YAML.tmLanguage"
        if syntax is 'PHP':
            self.output_panel.run_command('append', {'characters': "<?php\n"})
            return "Packages/PHP/PHP.tmLanguage"
        if syntax is 'Text':
            return "Packages/Text/Plain Text.tmLanguage"

    def renderWindow(self):
        self.view.run_command("render_window_results",
                              {"formatted_results": self.output,
                              "command": self.command,
                              "syntax": self.syntax})


class RenderWindowResultsCommand(sublime_plugin.TextCommand):

    def run(self, edit, formatted_results, command, syntax):
        """
        Create a new window with output results.
        """
        active_window = sublime.active_window()
        view_name = command
        existing_results = [v for v in active_window.views()
                            if v.name() == view_name and v.is_scratch()]
        if existing_results:
            result_view = existing_results[0]
        else:
            result_view = active_window.new_file()
            result_view.set_name(view_name)
            result_view.set_scratch(True)
            result_view.settings().set('pm_list', True)

        result_view.erase(edit, sublime.Region(0, result_view.size()))
        result_view.insert(edit, result_view.size(), formatted_results)

        result_view.assign_syntax(syntax)
        active_window.focus_view(result_view)
