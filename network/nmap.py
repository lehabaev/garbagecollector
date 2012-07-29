from subprocess import Popen, PIPE
import re

class nmap:
    def get_ip_list(self):
        (stdout, stderr) = Popen(["nmap", "-sP", "192.168.73.*"], stdout=PIPE).communicate()

        if stderr is not None:
            raise Exception(stderr)

        lines = stdout.split('\n')
        regex = re.compile('^Nmap scan report for.* \(?(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\)?$')

        ip_list = []
        
        for line in lines:
            match = regex.search(line)
            if match is not None:
                ip_list.append(match.group('ip'))

        return ip_list
