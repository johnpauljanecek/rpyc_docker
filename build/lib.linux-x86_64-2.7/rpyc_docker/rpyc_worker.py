from rpyc_docker.worker import Worker
import logging,rpyc

logger = logging.getLogger("rpyc_docker")
logger.setLevel(logging.INFO)

class RpycWorker(Worker):
    image = "ubuntu/rpyc_worker:pexpect"
    """
    there is a conflict with the ports when starting containers
    this needs to be fixed
    """
    def __init__(self,docker,mount = None):
        Worker.__init__(self)
        self.docker = docker
        self.mount = mount
        self.rpycPort = 9000 + self.workerNum - 1
        self.vncPort = 5900 + self.workerNum - 1
        self.browser = None
        self.driver = None
        
    def create_container(self,vncExternal=False):
        self.container = self.docker.create_container(
            self.image,
            ports = [5900,18812],
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

    def connect_rpyc(self):
        self.conn = rpyc.classic.connect("127.0.0.1",self.rpycPort)
        self.conn.modules.sys.path.insert(0,"/root")
        self.conn.modules.os.environ["USER"] = "root"
        return True

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

    def enable_logger(self,name = None,stdError=False):
        self.logStream = cStringIO.StringIO()
        
        if name :
            remote_logger = self.conn.modules.logging.getLogger(name)
        else:
            remote_logger = self.conn.modules.logging.getLogger()

        if stdError :
            handler = self.conn.modules.logging.StreamHandler(
                sys.stderr)
            remote_logger.addHandler(handler)
            
        handler = self.conn.modules.logging.StreamHandler(
            self.logStream)
        remote_logger.addHandler(handler)

    def teardown(self):
        self.docker.stop(self.container)
        self.docker.remove_container(self.container)

    def __del__(self):
        try:
            self.teardown()
        except:
            pass
