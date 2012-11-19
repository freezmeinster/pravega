from utils.storage import Storage
from utils.network import SwitchManager, Interface
from utils.log import Logger
from settings import Settings
import sys

class Vrm(object):
    def __init__(self):
        self.logger = Logger()
        self.settings = Settings()
        self.valid_driver = self.__list_valid_driver()
    
    def __list_valid_driver(self):
        return sets.get_item("vrm_default","valid_driver").split(",")
        
    def make_instance(self,name,driver,memory=None,ip=None,storage=None):
        pass
    
    def __init_storage(self,name,size):
        pass