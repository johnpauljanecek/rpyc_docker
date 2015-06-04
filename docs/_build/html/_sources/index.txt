Welcome to rpyc_docker's documentation!
=======================================

Rpyc_docker uses the python module Rpyc_ to control docker containers, that means you can run multiple instances of docker_ containers and control them externally and transparently using rpyc.

It can be used for other things, but right now it is primarily designed to run multiple selenium_ headless browsers on a single server or vps. The advantage of this approach is each browser is self contained in its own docker virtual machine, this makes it easier to customize the browser. Also if one of the browsers crashes, since it is isolated in its own virual machine it will not bring down the entire grid.

Since rpyc works over network protocols, it would be possible to have one server controlling multiple headless browsers on other machines. This feature has not been added in yet. If I have a need to do this, I might do this in the future.

.. _Rpyc: http://rpyc.readthedocs.org 
.. _docker: https://www.docker.com/
.. _selenium: http://selenium-python.readthedocs.org/

Contents:
=========

.. toctree::
   :maxdepth: 2

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

