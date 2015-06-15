docker build -t="rpyc_docker_vnc" .
#http://askubuntu.com/questions/150159/how-to-get-a-window-from-a-remote-box-command-line-only
#https://github.com/paimpozhil/docker-novnc/blob/master/startup.sh

To start vncserver in docker with openbox run docker as
see http://askubuntu.com/questions/229989/how-to-setup-x11vnc-to-access-with-graphical-login-screen

docker run -i -t -p 5901:5901/tcp rpyc_docker_vnc /bin/bash


vncserver
vncserver -kill :1
edit ./vnc/startup replace manager with openbox-session in this line "x-terminal-emulator -geometry 80x24+10+10 -ls -title "$VNCDESKTOP Desktop" &
openbox-session &"

vncserver
export DISPLAY=:0
chromium-browser --no-sandbox --user-data-dir=/tmp


setting vncserver options
vncserver -geometry 1000x700 -depth 16 :0 #0 is display number
