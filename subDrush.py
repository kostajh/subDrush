import sublime
import sublime_plugin
import subprocess
import json
import os
import fnmatch
import hashlib
import pickle
import time
import shutil
import threading
from .commands import *
from .lib import drush

class SublimeDrush(sublime_plugin.EventListener):

    def on_load_async(self, view):
        drush_api = DrushAPI()
        drush_api.load_command_args('core-status')
