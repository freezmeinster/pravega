import os
from glob import glob
from ConfigParser import ConfigParser

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

class Settings(object):
    def __init__(self):
        
        self.confs = glob("%s/config/*.conf" % PROJECT_ROOT)
        self.__parse_config()
        self.__join_config()
    
    def __parse_config(self):
        config_parse = ConfigParser()
        config_parse.read(self.confs)
        self.config_parse = config_parse
            
    
    def __join_config(self):
        conf = ConfigParser()
        conf.read(['%s/node.conf' % PROJECT_ROOT])
        for section_name in conf.sections():
            for name,value in conf.items(section_name):
                self.config_parse.set(section_name,name,value)
    
    def get_item(self,section,field):
        try :
            value = self.config_parse.get(section,field)
            if value.isdigit() :
                return int(value)
            else :
                return value
        except :
            return None