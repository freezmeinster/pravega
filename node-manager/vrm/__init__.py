from utils.storage import Storage
from utils.network import SwitchManager, Interface
from utils.log import Logger
from settings import Settings
import sys
import os
import imp

class Vrm(object):
    def __init__(self):
        self.driver = None
        self.is_synced = False
        self.logger = Logger()
        self.settings = Settings()
        self.valid_driver = self.__list_valid_driver()
    
    def __list_valid_driver(self):
        return self.settings.get_item("vrm_default","valid_driver").split(",")
        
    def init_object(self,vm_name,driver,memory=None,hd_size=None,password=None):
        if driver in self.__list_valid_driver() :
            self.driver = __import__("vrm.%s_driver" % driver,
                                 fromlist="*").Driver(vm_name,memory,hd_size,password)
            self.logger.success("[Vrm] Driver Object successfuly initialized for VirtualMacnine %s" % vm_name)
            if self.driver.is_synced :
                self.is_synced = True
                
            return True 
        else :
            self.logger.critical("[Vrm] Invalid or not supported Driver, %s" % driver)
            return False
        
        
    def register_instance(self):
        if self.is_synced :
            self.logger.warning("[Vrm] Instance %s already created" % self.driver.vm_name)
            return False
        else :
            self.driver.make_server()
            self.logger.success("[Vrm] Instance %s successfuly created" % self.driver.vm_name)
            return True
    
    