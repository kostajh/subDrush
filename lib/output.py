import sublime


class Output(object):
    """
    This class displays output returned from a subDrush command.
    All parameters are required.
    """

    def __init__(self, window, command, syntax, output):
        self.window = window
        self.command = command
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
        self.window.run_command("show_panel", {"panel": "output.%s" % self.command})

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
