import sublime
import sublime_plugin
import subprocess
import json
import os
import fnmatch
import hashlib
import pickle
import time
import xml.etree.ElementTree as ET
import urllib
import shutil

drupal_root = ""
working_dir = ""
drush_api = ""


class DrushAPI():

    def get_drush_path(self):
        return subprocess.Popen(['which', 'drush'], stdout=subprocess.PIPE).communicate()[0].decode('utf-8').rstrip()

    def load_command_info(self, command):
        commands = dict()
        # Check if cached data exists
        bin = self.get_cache_bin(self.get_drupal_root()) + "/commands"
        if os.path.isfile(bin):
            last_modified = os.path.getmtime(bin)
            if (time.time() - last_modified < 360):
                print('load cache')
                cache_bin = open(bin, 'rb')
                data = pickle.load(cache_bin)
                cache_bin.close()
                if command in data[u'core'][u'commands']:
                    commands = data[u'core'][u'commands'][command]
                    return commands
        print('call drush')
        data = json.loads(subprocess.Popen([self.get_drush_path(), '--format=json'], stdout=subprocess.PIPE).communicate()[0].decode('utf-8'))
        output = open(bin, 'wb')
        pickle.dump(data, output)
        output.close()
        commands = data[u'core'][u'commands'][command]
        return commands

    def load_command_args(self, command):
        bin = self.get_cache_bin(self.get_drupal_root() + "/" + command) + "/" + command
        if os.path.isfile(bin):
            cache_bin = open(bin, 'rb')
            last_modified = os.path.getmtime(bin)
            if (time.time() - last_modified < 360):
                print('load cache')
                args = pickle.load(cache_bin)
                cache_bin.close()
                return args
        print('call drush')
        args = subprocess.Popen([self.get_drush_path(), '--root=%s' % self.get_drupal_root(), '--pipe', command], stdout=subprocess.PIPE).communicate()[0].decode('utf-8').splitlines()
        output = open(bin, 'wb')
        pickle.dump(args, output)
        output.close()
        return args

    def build_command_list(self):
        command = []
        command.append(self.get_drush_path())
        command.append('--root=%s' % self.get_drupal_root())
        return command

    def run_command(self, command, args):
        cmd = self.build_command_list()
        cmd.append(command)
        cmd.append(args)
        return subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0].decode('utf-8')

    def set_working_dir(self, directory):
        global working_dir
        working_dir = directory

    def get_drupal_root(self):
        global working_dir
        global drupal_root
        if drupal_root:
            return drupal_root
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
            # @TODO Ugly, but works
            del(paths[-3:-1])
            del(paths[-1])
            drupal_root = "/".join(paths)
            self.get_cache_bin(drupal_root)
            return drupal_root
        else:
            # @TODO throw error
            self.get_cache_bin('drush')
            return 'drush'
        return working_dir

    def get_cache_bin(self, drupal_root):
        cache_bin = hashlib.sha224(drupal_root.encode('utf-8')).hexdigest()
        sublime_cache_path = sublime.cache_path()
        bin = sublime_cache_path + "/" + "sublime-drush" + "/" + cache_bin
        if os.path.isdir(bin) == False:
            os.makedirs(bin)
        return bin


class DrushVariableGetCommand (sublime_plugin.WindowCommand):
    global drush_api
    drush_api = DrushAPI()
    quick_panel_command_selected_index = None

    def run(self):
        global args
        global drush
        self.view = self.window.active_view()
        working_dir = self.view.window().folders()
        drush_api.set_working_dir(working_dir[0])
        variable_data = json.loads(drush_api.run_command('variable-get', '--format=json'))
        variables = []
        for key, value in variable_data.items():
            if (type(value) is str) and (type(key) is str):
                variables.append([key, value])
        self.args = variables
        self.window.show_quick_panel(variables, self.command_execution, sublime.MONOSPACE_FONT)

    def command_execution(self, idx):
        global args
        global drush_api
        drush_api.run_command('variable-get', self.args[idx][0])


class DrushCacheClearAllCommand (sublime_plugin.WindowCommand):
    global drush_api
    drush_api = DrushAPI()

    def run(self):
        self.view = self.window.active_view()
        working_dir = self.view.window().folders()
        drush_api.set_working_dir(working_dir[0])
        drupal_root = drush_api.get_drupal_root()
        drush_api.run_command('cache-clear', 'all')
        sublime.status_message("Cleared all caches for '%s'" % drupal_root)


class DrushCacheClearCommand (sublime_plugin.WindowCommand):
    quick_panel_command_selected_index = None
    global drush_api
    drush_api = DrushAPI()

    def run(self):
        global drush_api
        self.view = self.window.active_view()
        working_dir = self.view.window().folders()
        drush_api.set_working_dir(working_dir[0])
        self.args = drush_api.load_command_args('cache-clear')
        self.window.show_quick_panel(self.args, self.command_execution, sublime.MONOSPACE_FONT)

    def command_execution(self, idx):
        global drush_api
        drush_api.run_command('cache-clear', self.args[idx])
        drupal_root = drush_api.get_drupal_root()
        if drupal_root == self.args[idx]:
            sublime.status_message("Cleared '%s' cache" % self.args[idx])
        else:
            sublime.status_message("Cleared '%s' cache for '%s'" % (self.args[idx], drush_api.get_drupal_root()))


class DrushDownloadCommand (sublime_plugin.WindowCommand):
    quick_panel_command_selected_index = None
    global drush_api
    drush_api = DrushAPI()

    def run(self):
        global drush_api
        self.view = self.window.active_view()
        working_dir = self.view.window().folders()
        drush_api.set_working_dir(working_dir[0])
        bin = drush_api.get_cache_bin("drush") + '/projects.json'
        # @TODO - Check if cache is older than 24 hours.
        projects = []
        if os.path.isfile(bin):
            cache_bin = open(bin, 'rb')
            projects = pickle.load(cache_bin)
            cache_bin.close()
        else:
            sublime.status_message("Downloading Drupal.org project data, this could take about 30 seconds.")
            response = urllib.request.urlopen('http://updates.drupal.org/release-history/project-list/all')
            xml = response.read()
            root = ET.fromstring(xml)
            for child in root:
                project = dict()
                # Ignore sandbox projects
                if 'sandbox' in child[2].text:
                    continue
                project['shortname'] = child[1].text
                project['title'] = child[0].text
                projects.append(project)
            print('writing to project cache')
            output = open(bin, 'wb')
            pickle.dump(projects, output)
            output.close

        project_list = list()
        for item in projects:
            project_list.append([item[u'title'], item[u'shortname']])
        self.args = project_list
        self.window.show_quick_panel(self.args, self.command_execution, sublime.MONOSPACE_FONT)

    def command_execution(self, idx):
        global drush_api
        drush_api.run_command('pm-download', self.args[idx][1])
        sublime.status_message("Downloaded '%s' to %s" % (self.args[idx][1], drush_api.get_drupal_root()))


class SublimeDrushCacheClearCommand (sublime_plugin.WindowCommand):
    def run(self):
        print('clear')
        sublime_cache_path = sublime.cache_path()
        bin = sublime_cache_path + "/" + "sublime-drush"
        print(bin)
        shutil.rmtree(bin)
        os.makedirs(bin)
        sublime.status_message("Cleared Sublime Drush plugin cache")


class SublimeDrush(sublime_plugin.EventListener):
    def on_load(self, view):
        global drush_api
        drush_api = DrushAPI()
        drush_api.load_command_args('core-status')
