from utils.server import execute_command
from utils.log import Logger
from settings import Settings


class Storage(object):
    def __init__(self,name,driver,vg=None,size=None):
        self.name = name
        self.size = size
        self.volume_group = vg
    
    def __valid_logical_volume(self):
        pass