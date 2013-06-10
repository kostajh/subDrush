import os
import pickle
import hashlib
import fnmatch
import subprocess
import json
import time
import shutil

import sublime


class DrushAPI():

    def __init__(self):
        self.drupal_root = ""
        self.working_dir = ""

    def get_drush_path(self):
        """
        Get the path to the Drush executable.
        """
        return shutil.which('drush')

    def load_command_info(self, command):
        """
        Check if cached data exists. If cache is older than a minute, don't
        use it.
        """
        commands = dict()
        bin = self.get_cache_bin(self.get_drupal_root()) + "/commands"
        if os.path.isfile(bin):
            last_modified = os.path.getmtime(bin)
            if (time.time() - last_modified < 360):
                cache_bin = open(bin, 'rb')
                data = pickle.load(cache_bin)
                cache_bin.close()
                if command in data[u'core'][u'commands']:
                    commands = data[u'core'][u'commands'][command]
                    return commands
        data = json.loads(
            subprocess.Popen([self.get_drush_path(), '--format=json'],
                             stdout=subprocess.PIPE
                             ).communicate()[0].decode('utf-8'))
        output = open(bin, 'wb')
        pickle.dump(data, output)
        output.close()
        commands = data[u'core'][u'commands'][command]
        return commands

    def load_command_args(self, command):
        """
        Loads valid arguments for a command. This is useful for identifying,
        for example, which cache bins to display in a given environment.
        """
        bin = self.get_cache_bin(
            self.get_drupal_root() + "/" + command) + "/" + command
        if os.path.isfile(bin):
            cache_bin = open(bin, 'rb')
            last_modified = os.path.getmtime(bin)
            if (time.time() - last_modified < 360):
                args = pickle.load(cache_bin)
                cache_bin.close()
                return args
        args = subprocess.Popen([self.get_drush_path(),
                                '--root=%s' % self.get_drupal_root(),
                                '--pipe', command],
                                stdout=subprocess.PIPE
                                ).communicate()[0].decode('utf-8').splitlines()
        output = open(bin, 'wb')
        pickle.dump(args, output)
        output.close()
        return args

    def build_command_list(self):
        """
        Build the command list to pass to subprocess. We are adding the path
        to drush, then the path to the Drupal root.
        """
        command = []
        command.append(self.get_drush_path())
        command.append('--root=%s' % self.get_drupal_root())
        return command

    def run_command(self, command, args, options):
        """
        Run a Drush command. args and options must both be lists.
        """
        cmd = self.build_command_list()
        cmd.append(command)
        if args:
            for arg in args:
                cmd.append(arg)
        if options:
            for opt in options:
                cmd.append(opt)
        cmd.append('--nocolor')
        response = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        decoded = response.communicate()[0].decode('utf-8')
        return decoded.replace('\r\n', '\n')

    def get_local_site_aliases(self):
        """
        Returns a list of local site aliases.
        """
        options = list()
        options.append('--local')
        options.append('--format=json')
        aliases = self.run_command('site-alias', list(), options)
        if not aliases:
            return False
        aliases = json.loads(aliases)
        local_aliases = list()
        for alias, values in aliases.items():
            local_aliases.append(values[u'#id'].rsplit('.', 1)[0])
        return local_aliases

    def get_site_alias_from_drupal_root(self, directory):
        """
        Returns a string of the alias name that corresponds
        to `directory`, or False if an alias could not be found.
        Alias name will look like `@example.local`
        """
        options = list()
        options.append('-r')
        options.append('--local')
        options.append('--full')
        options.append('--format=json')
        drush_aliases = self.run_command('site-alias', list(), options)

        if not drush_aliases:
            return False
        drush_aliases = json.loads(drush_aliases)
        for alias, values in drush_aliases.items():
            if 'root' in values and directory == values[u'root'].replace(
                    '\/', '/'):
                return values['#id'].replace('@', '').rsplit('.', 1)[0]
        return False

    def set_working_dir(self, directory):
        """
        Sets the working directory.
        """
        self.working_dir = directory

    def get_drupal_root(self):
        """
        Returns the path to Drupal root, based on looking at self.working_dir
        """
        if self.drupal_root:
            return self.drupal_root
        if not self.working_dir:
            # If the working directory hasn't been set, return "drush"
            return 'drush'
        matches = []
        for root, dirnames, filenames in os.walk(self.working_dir):
            for filename in fnmatch.filter(filenames, 'system.module'):
                matches.append(os.path.join(root, filename))
                break
            if len(matches) > 0:
                break
        if len(matches) > 0:
            # Get path to Drupal root
            paths = matches[0].split('/')
            # Ugly, but works
            del(paths[-3:-1])
            del(paths[-1])
            drupal_root = "/".join(paths)
            self.get_cache_bin(drupal_root)
            return drupal_root
        else:
            # Default to Drush cache bin.
            self.get_cache_bin('drush')
            return 'drush'
        return self.working_dir

    def get_cache_bin(self, drupal_root):
        """
        Returns a cache bin for a Drupal root. If the bin doesn't exist, it is
        created.
        """
        cache_bin = hashlib.sha224(drupal_root.encode('utf-8')).hexdigest()
        sublime_cache_path = sublime.cache_path()
        bin = sublime_cache_path + "/" + "sublime-drush" + "/" + cache_bin
        if os.path.isdir(bin) is False:
            os.makedirs(bin)
        return bin
