import logging
import subprocess
import sys
import inspect
import wishful_upis as upis
from uniflex.core import modules
from uniflex.core import exceptions

__author__ = "Piotr Gawlowicz, Anatolij Zubow"
__copyright__ = "Copyright (c) 2015, Technische Universität Berlin"
__version__ = "0.1.0"
__email__ = "{gawlowicz, zubow}@tkn.tu-berlin.de"


'''
    Application layer - packet flows generated using IPerf tool.
'''


@modules.build_module
class IperfModule(modules.AgentModule):
    def __init__(self):
        super(IperfModule, self).__init__()
        self.log = logging.getLogger('IperfModule')

    @modules.bind_function(upis.net.install_application)
    def install_application(self, app):

        self.log.info('Function: install_application')
        self.log.info('args = %s' % str(app))

        try:
            appType = app.type
            port = app.port
            protocol = app.protocol

            if appType == "Server":
                self.log.info('Installing Server application')

                # cmd = str("killall -9 iperf")
                # os.system(cmd);
                bind = app.bind

                cmd = ['/usr/bin/iperf', '-s']
                if protocol == "TCP":
                    pass
                elif protocol == "UDP":
                    cmd.extend(['-u'])

                if port:
                    cmd.extend(['-p', str(port)])

                if bind:
                    cmd.extend(['-B', str(bind)])

                throughput = None
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

                while True:
                    line = process.stdout.readline()
                    line = line.decode('utf-8')
                    throughput = self.helper_parseIperf(line)
                    if throughput:
                        break

                process.kill()
                self.log.info('Server side Throughput : ' + str(throughput))
                sys.stdout.flush()
                msg = {"type": "Server",
                       "throughput": throughput}
                return msg

            elif appType == "Client":
                self.log.info('Installing Client application')

                serverIp = app.destination
                udpBandwidth = app.udpBandwidth
                dualTest = app.dualtest
                dataToSend = app.dataToSend
                transmissionTime = app.transmissionTime

                cmd = ['/usr/bin/iperf', '-c', serverIp]

                if protocol == "TCP":
                    pass
                elif protocol == "UDP":
                    cmd.extend(['-u'])
                    if udpBandwidth:
                        cmd.extend(['-b', str(udpBandwidth)])

                if port:
                    cmd.extend(['-p', str(port)])

                if dualTest:
                    cmd.extend(['-d'])

                if dataToSend:
                    cmd.extend(['-n', str(dataToSend)])

                if transmissionTime:
                    cmd.extend(['-t', str(transmissionTime)])

                throughput = None
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
                while True:
                    line = process.stdout.readline()
                    line = line.decode('utf-8')
                    throughput = self.helper_parseIperf(line)
                    if throughput:
                        break

                process.kill()
                self.log.info('Client Side Throughput : ' + str(throughput))
                sys.stdout.flush()
                msg = {"type": "Client",
                       "throughput": throughput}
                return msg

            else:
                self.log.info('Application Type not supported')

        except Exception as e:
            self.log.fatal("Install app failed: err_msg: %s" % (str(e)))
            raise exceptions.FunctionExecutionFailedException(
                func_name=inspect.currentframe().f_code.co_name,
                err_msg='Failed to install app: ' + str(e))

    def helper_parseIperf(self, iperfOutput):
        """Parse iperf output and return bandwidth.
           iperfOutput: string
           returns: result string"""
        import re

        r = r'([\d\.]+ \w+/sec)'
        m = re.findall(r, iperfOutput)
        if m:
            return m[-1]
        else:
            return None
