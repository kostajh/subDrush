import sublime_plugin

from .commands import *
from .lib.drush import DrushAPI


class SublimeDrush(sublime_plugin.EventListener):

    def on_load_async():
        drush_api = DrushAPI()
        drush_api.load_command_args('core-status')
