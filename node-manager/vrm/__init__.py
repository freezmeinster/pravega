from utils.storage import Storage
from utils.network import SwitchManager, Interface
from utils.log import Logger
from settings import Settings
import sys
import os

class Vrm(object):
    def __init__(self):
        self.vm_name = None
        self.driver = None
        self.ip = None
        self.memory = None
        self.storage = None
        self.synced = False
        self.logger = Logger()
        self.settings = Settings()
        self.valid_driver = self.__list_valid_driver()
    
    def __list_valid_driver(self):
        return self.settings.get_item("vrm_default","valid_driver").split(",")
        
    def register_instance(self,vm_name,driver,memory=None,ip=None):
        self.driver = driver
        self.vm_name = vm_name
        self.memory = memory
        self.ip = ip
        storage = Storage(vm_name,driver)
        if self.__check_vm() :
            self.logger.warning("[Vrm] Instance %s already created" % self.vm_name)
            return False
        else :
            self.__init_vm()
            self.logger.success("[Vrm] Instance %s successfuly created" % self.vm_name)
            return True
    
    def __init_vm(self,memory,ip,storage):
        pass
    
    def __check_vm(self):
        driver_char = "driver_%s" % self.driver
        repo_dir = self.settings.get_item(driver_char,"repo_dir")
        vm_dir = os.path.join(repo_dir,self.vm_name)
        return os.path.isdir(vm_dir)