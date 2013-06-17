import sublime_plugin
from .commands import *
from .lib.drush import DrushAPI


class SublimeDrush(sublime_plugin.EventListener):

    def on_load_async(self, view):
        if (view.file_name() is not None):
          drush_api = DrushAPI(None)
          drush_api.check_requirements()
