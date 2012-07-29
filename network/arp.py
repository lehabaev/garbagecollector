from subprocess import Popen, PIPE
import re

class arp:
    def get_dictionary(self):
        (stdout, stderr) = Popen(["arp", "-a"], stdout=PIPE).communicate()

        if stderr is not None:
            raise Exception(stderr)

        lines = stdout.split('\n')
        regex = re.compile('\((?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\) at (?P<mac>\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2}:\w{1,2})')

        addresses = {}
        
        for line in lines:
            match = regex.search(line)
            if match is not None:
                ip = match.group('ip')
                mac = match.group('mac')
                addresses[ip] = mac

        return addresses