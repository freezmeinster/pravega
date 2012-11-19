import Pyro4

Pyro4.config.HMAC_KEY = "ilkom2012"
uri = "PYRO:Vrm@192.168.1.6:9090"
obj = Pyro4.Proxy(uri)
print obj.register_instance(vm_name='labnet',driver='vserver')
