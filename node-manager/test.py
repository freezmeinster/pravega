import Pyro4

Pyro4.config.HMAC_KEY = "ilkom2012"
uri = "PYRO:Vrm@192.168.1.6:9090"
obj = Pyro4.Proxy(uri)
obj.init_object(vm_name="zia",driver="vserver",memory="1024",hd_size="3G")
obj.register_instance()
