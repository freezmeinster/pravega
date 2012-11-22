import os
import glob
from random import randint
from utils.storage import Storage
from utils.network import SwitchManager, Interface
from utils.log import Logger
from settings import Settings
from utils.server import execute_command

class Driver(object):
    def __init__(self,name,memory=None,hd_size=None,password=None):
        self.settings = Settings()
        suff_name = self.settings.get_item("driver_vserver","prefix_name")
        self.vm_name = suff_name+name
        self.conf_base = self.settings.get_item("driver_vserver","conf_dir") + "/" + self.vm_name
        self.repo_base = self.settings.get_item("driver_vserver","repo_dir")
        self.buildroot = self.settings.get_item("vrm_default","buildroot")
        self.ip = self.__get_ip()
        self.is_synced = self.__check_vm()
        
        if not memory :
            self.memory = self.settings.get_item("resource","default_memory")
        else :
            self.memory = memory
        
        if not password :
            self.passwd = self.vm_name
        else :
            self.passwd = password
            
        if not hd_size :
            self.size = self.settings.get_item("resource","default_storage_space")
        else :
            self.size = hd_size
        
    def make_server(self):
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
        interface = "dummy0:%s/%s" % (self.ip, self.settings.get_item(
            "driver_vserver","network_netmask_cidr"))
        init_command = """
            vserver %s build -m skeleton \
            --hostname %s \
            --interface %s \
            --flags lock,virt_mem,virt_uptime,virt_cpu,virt_load,hide_netif\
            --initstyle sysv
            """ % (self.vm_name,self.vm_name,interface)
        execute_command(init_command)
        execute_command("rsync -arv %s /tmp/pravega/volume/%s" %
                        (home, self.vm_name))
        execute_command("umount /tmp/pravega/volume/%s" % self.vm_name)
        execute_command("rm -rf %s/*" % home) 
        execute_command("mount /dev/%s/%s" % (
            self.settings.get_item("driver_vserver","volume_group"),
            self.vm_name,
            ))
        execute_command("mount aufs-%s" % self.vm_name)
        
        os.mkdir(os.path.join(self.conf_base,'cgroup'))
        mem = open(os.path.join(self.conf_base,'cgroup/memory.limit_in_bytes'),'w')
        mem.write(""+str(self.memory)+"M\n")
        mem.close()
        
        swap = open(os.path.join(self.conf_base,'cgroup/memory.memsw.limit_in_bytes'),'w')
        swap.write(""+str(int(self.memory)+2*int(self.memory))+"M\n")
        swap.close()
        

        old_password = execute_command("openssl passwd "+self.passwd+"").strip()
        execute_command("chroot "+home+" /usr/sbin/usermod -p \""+old_password+"\" root") 
    
    def __create_storage(self):
        com1 = "lvcreate -L %s -n %s --addtag %s %s" % (
            self.size,
            self.vm_name, self.vm_name,
            self.settings.get_item("driver_vserver","volume_group"))
        
        com2 = "mkfs.%s /dev/%s/%s" % (
            self.settings.get_item("resource","default_storage_filesystem"),
            self.settings.get_item("driver_vserver","volume_group"),
            self.vm_name
        )
        
        com3 = "mkdir -p /tmp/pravega/volume/%s" % self.vm_name
        
        com4 = "mount /dev/%s/%s /tmp/pravega/volume/%s" % (
            self.settings.get_item("driver_vserver","volume_group"),
            self.vm_name,
            self.vm_name
        )
        
        execute_command(com1)
        execute_command(com2)
        execute_command(com3)
        execute_command(com4)
        self.__prepare_fstab()
    
    def __prepare_fstab(self):
        lvs = "/dev/%s/%s" % (
            self.settings.get_item("driver_vserver","volume_group"),
            self.vm_name)
        mnt = os.path.join(self.repo_base, self.vm_name)
        lv = execute_command("cat /etc/fstab | grep -c %s " % lvs)
        
        if lv != None :
            pass
        else :
            execute_command("echo '%s %s ext4 defaults 1 1' >> /etc/fstab" % (lvs,mnt))
            cmd = "echo 'aufs-%s %s aufs br:%s=rw:%s=ro 1' 1 >> /etc/fstab" % (
                self.vm_name,
                mnt,
                mnt,
                self.buildroot
            )
            execute_command(cmd)
            
    def __check_vm(self):
        repo_dir = self.settings.get_item("driver_vserver","repo_dir")
        vm_dir = os.path.join(repo_dir,self.vm_name)
        return os.path.isdir(vm_dir)
    
    def __get_ip(self):
        range_down = int(self.settings.get_item(
            "driver_vserver","network_ip_range").split("-")[0])
        range_up = int(self.settings.get_item(
            "driver_vserver","network_ip_range").split("-")[1])
        ips = self.__check_all_ip()
        ip_prefix = self.settings.get_item("driver_vserver","network_ip_prefix")
        ip = ""
        while True:
            rand = randint(range_down,range_up)
            if rand not in ips :
                ip = ip_prefix+"."+str(rand)
                break
            else :
                pass
        return ip
    
    def __check_all_ip(self):
        ip_list = []
        for vm in glob.glob("%s/../*" % self.conf_base):
            suff = execute_command("cat %s/interfaces/0/ip | cut -d '.' -f4" % vm
            )
            ip_list.append(suff)
        return ip_list
