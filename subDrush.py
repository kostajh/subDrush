import sublime_plugin
from .lib.drush import DrushAPI


class SublimeDrush(sublime_plugin.EventListener):

    def on_load_async():
        drush_api = DrushAPI()
        print('Loading Drush command args for current directory')
        drush_api.load_command_args('core-status')
