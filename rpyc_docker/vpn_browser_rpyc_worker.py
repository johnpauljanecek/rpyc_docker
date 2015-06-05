import os,time,ifcfg,rpyc_docker

class OpenVpnMixin(object):
    
    def get_vpngate_certificate(self,filename):
        with open(filename,"r") as f:
            lines = map(lambda l: l.rstrip(),f.read().splitlines())
        return os.linesep.join(lines)

    def get_interfaces(self):
        ifcfg = self.conn.modules["ifcfg"]
        return ifcfg.interfaces()

    def connect_vpn(self):
        assert self.connect_openvpn(
        self.vpnCert,self.vpnUser,self.vpnPass),"Unable to connect to VPN"
        
    def connect_openvpn(self,certificate,user,passwd,timeout = 30):
        """timeOut how long to try to connect"""
        pathPasswd = "/tmp/passwd.txt"
        certPath = "/tmp/cert.ovpn"
        self.write_file(pathPasswd,os.linesep.join([user,passwd]))
        
        notFound = True
        lines = certificate.splitlines()
        
        for i in range(len(lines)) :
            line = lines[i]
            if line.startswith("dev tun"):
                lines[i] = "dev tun%d" % self.workerNum
            elif line.find("auth-user-pass") > -1 :
                lines[i] = "auth-user-pass %s" % pathPasswd
                notFound = not(notFound)
            elif notFound and line.startswith("<ca>"):
                lines.insert(i,"auth-user-pass %s" % pathPasswd)
                break
            else:
                pass

        self.write_file(certPath,os.linesep.join(lines)) 
        
        logger.info("self.docker.exec_create %s %s",user,passwd)
        self.exec_id = self.docker.exec_create(
            self.container,
            "openvpn %s" % certPath, 
            stdout=False, 
            stderr=False,
            tty=False,
        )

        self.docker.exec_start(self.exec_id,
                               detach=True,
                               stream=False)
        

        interfaceUp = False
        for i in range(timeout):
            time.sleep(1)
            interfaces = " ".join(self.get_interfaces().keys())
            if interfaces.find("tun") > -1 :
                logger.info("check interfaces %s",interfaces)
                interfaceUp = True
                break
        
        return interfaceUp
    
    def docker_cmd(self,cmd):
        psId = self.docker.exec_create(self.container,cmd)
        lines = self.docker.exec_start(psId,stream=False).splitlines()
        return lines
    
    
class VpnBrowserRpycWorker(OpenVpnMixin,rpyc_docker.BrowserRpycWorker):
    def __init__(self,docker,mount = None,vpnUser=None,vpnPass=None,vpnCert = None,vpnCertPath = None):
        rpyc_docker.BrowserRpycWorker.__init__(self,docker,mount = mount)
        assert not(vpnCertPath and vpnCert),"both certPath and cert can not be set"
        assert vpnCertPath or vpnCert,"either certPath or cert must be set"
        if vpnCertPath :
            vpnCert = self.get_vpngate_certificate(vpnCertPath)
        self.vpnCert = vpnCert
        self.vpnUser = vpnUser
        self.vpnPass = vpnPass
        
    def connect_rpyc(self):
        rpyc_docker.BrowserRpycWorker.connect_rpyc(self)
        self.conn.modules.sys.path.insert(0,"/Development/amazon")
