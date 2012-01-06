======
Liasis
======

An asynchronous Python-powered HTTP daemon that serves RST or HTML websites.

Kernel tweaks
-------------
::

    net.ipv4.tcp_fin_timeout = 5

    net.ipv4.tcp_tw_recycle = 1

    net.ipv4.tcp_tw_reuse = 1
