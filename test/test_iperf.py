#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import uniflex_module_iperf

'''
    Direct module test; without framework.
    Req.: Iperf has to be installed: apt-get install gnuradio
'''
if __name__ == '__main__':

    startServer = False
    startClient = True

    iperf = uniflex_module_iperf.IperfModule()

    if startServer:
        print('Installing iperf server on node')
        serverApp0 = uniflex_module_iperf.ServerApplication()
        serverApp0.setBind("192.168.14.142")
        serverApp0.setProtocol("TCP")
        server_thr = iperf.install_application(serverApp0)
        print('Iperf client; throughput is %s' % str(server_thr['throughput']))

    if startClient:
        print('Installing iperf client on node')
        clientApp0 = uniflex_module_iperf.ClientApplication()
        clientApp0.setDestination("192.168.14.142")
        clientApp0.setProtocol("TCP")

        client_thr = iperf.install_application(clientApp0)
        print('Iperf client; throughput is %s' % str(client_thr['throughput']))
