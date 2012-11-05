from utils.storage import Storage
from utils.network import SwitchManager, Interface
from utils.log import Logger
import sys

class Vrm(object):
    def __init__(self):
        l=Logger()
        l.critical("Storage alrady in use")