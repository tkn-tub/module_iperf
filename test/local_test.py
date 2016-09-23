import logging
import datetime
import time
import random
import wishful_upis as upis
from wishful_agent.core import wishful_module
from wishful_agent.timer import TimerEventSender

__author__ = "Anatolij Zubow"
__copyright__ = "Copyright (c) 2016, Technische Universität Berlin"
__version__ = "0.1.0"
__email__ = "{zubow}@tkn.tu-berlin.de"

'''
Local test of iperf component.
'''

@wishful_module.build_module
class IperfController(wishful_module.ControllerModule):
    def __init__(self):
        super(IperfController, self).__init__()
        self.log = logging.getLogger('IperfController')

    @wishful_module.on_start()
    def my_start_function(self):
        self.log.info("start iperf test")

        node = self.localNode

        startServer = False
        startClient = True

        try:

            if startServer:
                self.log.info('Installing iperf server on node')
                serverApp0 = upis.net.ServerApplication()
                serverApp0.setBind("192.168.14.142")
                serverApp0.setProtocol("TCP")
                node.callback(self.appCallback).net.install_application(serverApp0)

            if startClient:
                self.log.info('Installing iperf client on node')
                clientApp0 = upis.net.ClientApplication()
                clientApp0.setDestination("192.168.14.142")
                clientApp0.setProtocol("TCP")

                thr = node.net.install_application(clientApp0)
                self.log.info('Iperf client; throughput is %s' % str(thr['throughput']))

            self.log.info('... done')

        except Exception as e:
            self.log.error("{} Ctrl:: !!!Exception!!!: {}".format(datetime.datetime.now(), e))


    @wishful_module.on_exit()
    def my_stop_function(self):
        self.log.info("stop iperf test")
