from rpyc_docker.worker import Worker,decorator_reset_uptime
import logging,rpyc,cStringIO

class RpycWorker(Worker):
    image = "rpyc_docker"
    
    """
    there is a conflict with the ports when starting containers
    this needs to be fixed
    """
    def __init__(self,docker,mount = None):
        Worker.__init__(self)
        self.docker = docker
        self.mount = mount
        self._rpycPort = 9000 + self.workerNum - 1
        self._vncPort = 5900 + self.workerNum - 1
        self._conn = None
        self.enable_logger()
        self.logger.info("RpycWorker __init__")
        
    @property
    def vncPort(self):
        """
        :return: port vncserver is listening on
        :rtype: int
        """
        return self._vncPort

    @property
    def rpycPort(self):
        """
        :return: port rpyc server is listening on
        :rtype: int
        """
        return self._rpycPort
        
    def create_container(self,image = None,vncExternal=False):
        if image :
            self.image = image
        self.container = self.docker.create_container(
            self.image,
            ports = [5900,18812],
            environment = {"DISPLAY" : ":0"},
            working_dir = "/Development",
            volumes = ['/Development'],
            command = "rpyc_classic.py"
        )

        port_bindings = {
            18812: ('127.0.0.1',self.rpycPort),
            5900: ('127.0.0.1',self.vncPort)}

        if vncExternal :
            port_bindings[5900] = (vncExternal,self.vncPort)

        binds = {}
        if self.mount :
            binds = { self.mount : 
                      { 'bind': '/Development', 'ro': False }}
            
        self.response = self.docker.start(
            self.container,
            port_bindings = port_bindings, 
            privileged = True,
            binds = binds,
        )

        #this option does not seem to work
        #set DNS in docker with 
        #https://robinwinslow.co.uk/2014/08/27/fix-docker-networking/
        #patching the container directly by modifying resolv.conf file

        resolvPath = self.docker.inspect_container(self.container)["ResolvConfPath"]
        self.cmd(u"echo 'nameserver 8.8.8.8' | sudo tee %s" % resolvPath)

    @property
    @decorator_reset_uptime
    def conn(self):
        return self._conn
        
    @decorator_reset_uptime
    def connect_rpyc(self):
        self._conn = rpyc.classic.connect("127.0.0.1",self.rpycPort)
        self.conn.modules.sys.path.insert(0,"/root")
        self.conn.modules.os.environ["USER"] = "root"
        self.enable_remote_logger()
        return True

    def read_file(self,filePath):
        os = self.conn.modules.os
        with self.conn.builtins.open(filePath,"r") as f:
            content = f.read()
        return content
    
    def write_file(self,filePath,content):
        os = self.conn.modules.os
        with self.conn.builtins.open(filePath,"w") as f:
            f.write(content)
        return True

    def docker_ps(self):
        """gets all the processes running in the docker container"""
        psId = self.docker.exec_create(self.container,"ps")
        lines = self.docker.exec_start(psId,stream=False).splitlines()
        
        titles = map(lambda t: t.lower(),lines[0].split())
        processes = []
        for line in lines[1:]:
            process = {}
            for title,value in zip(titles,line.split()) :
                process[title] = value
            processes.append(process)
        return processes

    def docker_ls(self,path = ""):
        psId = self.docker.exec_create(self.container,"ls %s" % path)
        lines = self.docker.exec_start(psId,stream=False).splitlines()
        return lines

    def docker_cmd(self,cmd):
        psId = self.docker.exec_create(self.container,cmd)
        lines = self.docker.exec_start(psId,stream=False).splitlines()
        return lines

    def enable_logger(self):
        self.logger_name = "worker %d" % self.workerNum
        self.logger = logging.getLogger(self.logger_name)
        #self.logger.setLevel(logging.INFO)
        self.logStream = cStringIO.StringIO()
        self.streamHandler = logging.StreamHandler(
            self.logStream)
        self.streamHandler.setFormatter(logging.Formatter("%(name)s %(module)s %(lineno)d %(message)s"))
        self.logger.addHandler(self.streamHandler)
        self.logger.propogate = False
        self.streamHandler.setLevel(logging.INFO)
        self.logger.setLevel(logging.INFO)

    def enable_remote_logger(self,name = None):
        if name :
            self.remote_logger = self.conn.modules.logging.getLogger(name)
        else :
            self.remote_logger = self.conn.modules.logging.getLogger()
        self.remote_logger.addHandler(self.streamHandler)
        self.remote_logger.setLevel(logging.INFO)
        self.remote_logger.propogate = False

    def get_log(self):
        self.logStream.seek(0)
        return self.logStream.readlines()
        
    @decorator_reset_uptime
    def start_openbox(self,password = "secret",size = (1024,600),color_depth = 24):
        self.create_vnc_passwd(password)
        xstartupLines = ['#!/bin/sh',
                 '',
                 '# Uncomment the following two lines for normal desktop:',
                 '# unset SESSION_MANAGER',
                 '# exec /etc/X11/xinit/xinitrc',
                 '',
                 '[ -x /etc/vnc/xstartup ] && exec /etc/vnc/xstartup',
                 '[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources',
                 'xsetroot -solid grey',
                 'vncconfig -iconic &',
                 #'x-terminal-emulator -geometry 80x24+10+10 -ls -title "$VNCDESKTOP Desktop" &',
                 'openbox-session &']
        
        #self.write_file("/root/.vnc/xstartup","\n".join(xstartupLines))
        
        self.vncserver_exec_id = self.docker.exec_create(
                self.container,
                "vncserver -geometry %dx%d -depth %d :0" % (size[0],size[1],color_depth), 
                stdout=False, 
                stderr=False,
                tty=False,
            )

        self.docker.exec_start(self.vncserver_exec_id,
                                   detach=True,
                                   stream=False)

    def teardown(self):
        try:
            self.docker.kill(self.container)
            self.docker.remove_container(self.container)
        except:
            pass

    def __del__(self):
        try:
            self.teardown()
        except:
            pass

    @decorator_reset_uptime
    def create_vnc_passwd(self,passWord):
        pexpect = self.conn.modules["pexpect"]
        child = pexpect.spawn('vncpasswd')
        child.expect('Password:')
        child.sendline('secret')
        child.expect('Verify:')
        child.sendline('secret')
        return True
    
