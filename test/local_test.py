import logging
import datetime
import wishful_upis as upis
from uniflex.core import modules

__author__ = "Anatolij Zubow"
__copyright__ = "Copyright (c) 2016, Technische Universität Berlin"
__version__ = "0.1.0"
__email__ = "{zubow}@tkn.tu-berlin.de"

'''
Local test of iperf component.
'''

@modules.build_module
class IperfController(modules.ControllerModule):
    def __init__(self):
        super(IperfController, self).__init__()
        self.log = logging.getLogger('IperfController')

    @modules.on_start()
    def my_start_function(self):
        self.log.info("start iperf test")

        try:
            node = self.localNode

            startServer = False
            startClient = True

            if startServer:
                self.log.info('Installing iperf server on node')
                serverApp0 = upis.net.ServerApplication()
                serverApp0.setBind("192.168.14.142")
                serverApp0.setProtocol("TCP")
                server_thr = node.net.install_application(serverApp0)
                self.log.info('Iperf client; throughput is %s' % str(server_thr['throughput']))

            if startClient:
                self.log.info('Installing iperf client on node')
                clientApp0 = upis.net.ClientApplication()
                clientApp0.setDestination("192.168.14.142")
                clientApp0.setProtocol("TCP")

                client_thr = node.net.install_application(clientApp0)
                self.log.info('Iperf client; throughput is %s' % str(client_thr['throughput']))

            self.log.info('... done')

        except Exception as e:
            self.log.error("{} Ctrl:: !!!Exception!!!: {}".format(datetime.datetime.now(), e))


    @modules.on_exit()
    def my_stop_function(self):
        self.log.info("stop iperf test")
