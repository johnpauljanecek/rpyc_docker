Welcome to rpyc_docker's documentation!
=======================================

Rpyc_docker uses the python module Rpyc_ to control docker containers, that means you can run multiple instances of docker_ containers and control them externally and transparently using rpyc.

It can be used for other things, but right now it is primarily designed to run multiple selenium_ headless browsers on a single server or vps. The advantage of this approach is each browser is self contained in its own docker virtual machine, this makes it easier to customize the browser. Also if one of the browsers crashes, since it is isolated in its own virual machine it will not bring down the entire grid.

Since rpyc works over network protocols, it would be possible to have one server controlling multiple headless browsers on other machines. This feature has not been added in yet. If I have a need to do this, I might do this in the future.

.. _Rpyc: http://rpyc.readthedocs.org 
.. _docker: https://www.docker.com/
.. _selenium: http://selenium-python.readthedocs.org/

Requirements
============
* An OS which supports Docker
* Docker - instructions_ on how to install docker
* Python 2.7.X - right now rpyc_docker only runs on python 2.7.X because that is the version of Python I use. At this point in time I have no need to make it run on Python 3.X

.. _instructions: https://docs.docker.com/installation/
  
Setup
=====
1. Download rpyc_docker from its repository_ . To download click the buttom marked Download Zip.
2. Unpack the archive.
3. From the command line switch to the directory docker_files/rpyc_docker
4. Built the docker image with the command "docker build -t="rpyc_docker" ." If you wish you can create your own custom docker image.
5. Install the package with "pip2 install ." You could also use "python setup.py install" but it is better to use pip. 
   
.. _repository: https://github.com/johnpauljanecek/rpyc_docker

Examples
========

All of the examples are in ipython notebooks, that way you can experiment with the examples and modify them. 

1. Using the `Browser Object`_ - how to setup and use browser object stand alone.
2. Using a single Browser Object running inside a docker container to scrape duckduckgo and python subreddit. BrowserRpycWorker_.
3. Using a Manager to run a series of requests to query duckerduckgo and fetch the headlines off a python subreddit simultaniously. Each job will run in its own isolated docker container. `Example using manager to run multiple dockers at once`_      

.. _Browser Object: http://nbviewer.ipython.org/github/johnpauljanecek/rpyc_docker/blob/master/examples/Example%20Browser%20Alone.ipynb
.. _BrowserRpycWorker: http://nbviewer.ipython.org/github/johnpauljanecek/rpyc_docker/blob/master/examples/Example%20BrowserRpycWorker%20.ipynb
.. _Example using manager to run multiple dockers at once: http://nbviewer.ipython.org/github/johnpauljanecek/rpyc_docker/blob/master/examples/Example%20using%20manager%20to%20run%20multiple%20dockers%20at%20once.ipynb

Contents:
=========

.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

