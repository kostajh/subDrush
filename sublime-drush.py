import sublime
import sublime_plugin
import subprocess
import json
import os
import sys
import fnmatch
import re
import pprint

class DrushAPI():

    global working_dir

    def get_drush_path(self):
        return subprocess.Popen(['which', 'drush'], stdout=subprocess.PIPE).communicate()[0].decode('utf-8').rstrip()

    def load_commands(self):
        data = json.loads(subprocess.Popen([self.get_drush_path(), '--format=json'], stdout=subprocess.PIPE).communicate()[0].decode('utf-8'))
        return data[u'core'][u'commands']

    def load_command_info(self, command):
        commands = dict()
        data = json.loads(subprocess.Popen([self.get_drush_path(), '--format=json'], stdout=subprocess.PIPE).communicate()[0].decode('utf-8'))
        commands = data[u'core'][u'commands'][command]
        return commands

    def load_command_args(self, command):
        return subprocess.Popen([self.get_drush_path(), '--root=%s' % self.get_drupal_root(), '--pipe', command], stdout=subprocess.PIPE).communicate()[0].decode('utf-8').splitlines()

    def build_command_list(self):
        command = []
        command.append(self.get_drush_path())
        command.append('--root=%s' % self.get_drupal_root())
        return command

    def run_command(self, command, args):
        cmd = self.build_command_list()
        cmd.append(command)
        cmd.append(args)
        print(cmd)
        return subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0].decode('utf-8')

    def set_working_dir(self, directory):
        global working_dir
        working_dir = directory

    def get_drupal_root(self):
        global working_dir
        matches = []
        for root, dirnames, filenames in os.walk(working_dir):
            for filename in fnmatch.filter(filenames, 'system.module'):
                matches.append(os.path.join(root, filename))
                break
            if len(matches) > 0:
                break
        if len(matches) > 0:
            # Get path to Drupal root
            paths = matches[0].split('/')
            del(paths[-3:-1])
            del(paths[-1])
            drupal_root = "/".join(paths)
            return drupal_root
        else:
            # @TODO throw error
            print('error')
        return working_dir

class DrushVariableGetCommand (sublime_plugin.WindowCommand):
    quick_panel_command_selected_index = None

    def run(self):
        global args
        global drush
        self.view = self.window.active_view()
        working_dir = self.view.window().folders()
        drush = DrushAPI()
        drush.set_working_dir(working_dir[0])
        command_options = drush.load_command_info('variable-get')
        variable_data = json.loads(drush.run_command('variable-get', '--format=json'))
        variables = []
        for key, value in variable_data.items():
            if (type(value) is str) and (type(key) is str):
                variables.append([key, value])
        args = variables
        self.window.show_quick_panel(variables, self.command_execution, sublime.MONOSPACE_FONT)

    def command_execution(self, idx):
        global args
        global drush
        ret = drush.run_command('variable-get', args[idx][0])
        print(ret)

class DrushCacheClearCommand (sublime_plugin.WindowCommand):
    quick_panel_command_selected_index = None

    def run(self):
        global args
        global drush
        self.view = self.window.active_view()
        working_dir = self.view.window().folders()
        drush = DrushAPI()
        drush.set_working_dir(working_dir[0])
        command_options = drush.load_command_info('cache-clear')
        args = drush.load_command_args('cache-clear')
        self.window.show_quick_panel(args, self.command_execution, sublime.MONOSPACE_FONT)

    def command_execution(self, idx):
        global args
        global drush
        ret = drush.run_command('cache-clear', args[idx])

