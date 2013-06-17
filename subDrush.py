import sublime_plugin
from .commands import *
from .lib.drush import DrushAPI


class SublimeDrush(sublime_plugin.EventListener):

    def on_load_async(self, view):
        if (view.file_name()):
          drush_api = DrushAPI(view)
          drush_api.check_requirements()
          print('Loading Drush command args for current directory')
          drush_api.load_command_args('core-status')
