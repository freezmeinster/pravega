from utils.storage import Storage
from utils.network import SwitchManager, Interface
from utils.log import Logger
from settings import Settings

class Driver(object):
    def __init__(self):
        self.settings = Settings()
        
    def init_server(self):
        pass
    
    def destroy_server(self):
        pass
    
    def alter_attribute(self):
        pass
    
    def start_server(self):
        pass
    
    def stop_server(self):
        pass