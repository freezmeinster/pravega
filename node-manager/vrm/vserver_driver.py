import os
from utils.storage import Storage
from utils.network import SwitchManager, Interface
from utils.log import Logger
from settings import Settings
from utils.server import execute_command

class Driver(object):
    def __init__(self,name,ip=None,memory=None):
        self.settings = Settings()
        suff_name = self.settings.get_item("driver_vserver","prefix_name")
        self.vm_name = suff_name+name
        self.conf_base = self.settings.get_item("driver_vserver","conf_dir")
        self.repo_base = self.settings.get_item("driver_vserver","repo_dir")
        self.buildroot = self.settings.get_item("driver_vserver","buildroot")
        if not memory :
            self.memory = self.settings.get_item("resource","default_memory")
        else :
            self.memory = memory
            
        if not ip :
            pass
        else :
            self.ip = ip
        
    def init_server(self):
        if self.__check_vm():
            pass
        else :
            self.__create_storage()
            self.__create_vm()
    
    def destroy_server(self):
        pass
    
    def alter_attribute(self,paramater,new_value):
        pass
    
    def start_server(self):
        pass
    
    def stop_server(self):
        pass
    
    def restart_server(self):
        pass
    
    def __create_vm(self):
        conf_dir = os.path.join(self.conf_base,self.vm_name)
        home = os.path.join(self.repo_base, self.vm_name)
        command = """
            vserver %s build -m skeleton \
            --hostname %s \
            --interface %s \
            --flags lock,virt_mem,virt_uptime,virt_cpu,virt_load,hide_netif\
            --initstyle sysv
            """ % (name,vps_hostname,interface)
        execute_command("rsync -arv %s /tmp/pravega/volume/%s" %
                        (home, self.vm_name))
        execute_command("umount /tmp/pravega/volume/%s" % self.vm_name)
        execute_command("rm -rf %s/*" % self.vm_name) 
        execute_command()
        
        execute_command(command)
        
        os.mkdir(os.path.join(conf_dir,'cgroup'))
        mem = open(os.path.join(conf_dir,'cgroup/memory.limit_in_bytes'),'w')
        mem.write(""+str(self.memory)+"M\n")
        mem.close()
        
        swap = open(os.path.join(conf,'cgroup/memory.memsw.limit_in_bytes'),'w')
        swap.write(""+str(int(self.memory)+2*int(self.memory))+"M\n")
        swap.close()
        

        old_password = execute_command("openssl passwd "+self.vm_name+"").read().strip()
        execute_command("chroot "+home+" /usr/sbin/usermod -p \""+old_password+"\" root") 
    
    def __create_storage(self):
        com1 = "lvcreate -L 1G -n %s --addtag %s %s" % (
            self.vm_name, self.vm_name,
            self.settings.get_item("driver_vserver","volume_group"))
        
        com2 = "mkfs.%s /dev/%s/%s" % (
            self.settings.get_item("resource","default_storage_filesystem"),
            self.settings.get_item("driver_vserver","volume_group"),
            self.vm_name
        )
        
        com3 = "mkdir -p /tmp/pravega/volume/%s" % self.vg_name
        
        com4 = "mount /dev/%s/%s /tmp/pravega/volume/%s" % (
            self.settings.get_item("driver_vserver","volume_group"),
            self.vm_name,
            self.vm_name
        )
        
        execute_command(com1)
        execute_command(com2)
        execute_command(com3)
        execute_command(com4)
    
    def __prepare_fstab(self):
        lv = execute_command("cat /etc/fstab | grep -c /dev/%s/%s") % (
        )
    
    def __check_vm(self):
        repo_dir = self.settings.get_item("driver_vserver","repo_dir")
        vm_dir = os.path.join(repo_dir,self.vm_name)
        return os.path.isdir(vm_dir)
    

    #def __check_storage(self):
    #    comm = "lvs --units m  @%s | grep -v -c \"LV\"" % self.vm_name
    #    if int(comm) == 0 :
    #        return True
    #    elif int(comm) == 1:
    #        return False
    #    else :
    #        return False
        
    