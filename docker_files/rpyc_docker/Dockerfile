FROM ubuntu
FROM ubuntu:14.04

RUN echo "deb http://archive.ubuntu.com/ubuntu trusty main universe\\n" > /etc/apt/sources.list
RUN echo "deb http://archive.ubuntu.com/ubuntu trusty-updates main universe\\n" >> /etc/apt/sources.list

RUN apt-get update -y
RUN apt-get install -y python2.7 python-pip openvpn xvfb vnc4server firefox xclip python2.7-dev libjpeg-dev libfreetype6-dev zlib1g-dev chromium-browser chromium-chromedriver
RUN apt-get autoclean -y

#install python stuff
RUN /usr/bin/pip2 install rpyc selenium pyvirtualdisplay beautifulsoup4 pexpect pyperclip install selenium-requests

