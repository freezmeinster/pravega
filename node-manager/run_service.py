#!/usr/bin/env python
import os
import sys
from settings import Settings
from utils.server import Server, prepare_kmod
from vrm import Vrm


if __name__=="__main__" :
    server = Server()
    prepare_kmod()
    server.hook_object(Vrm())
    server.run()