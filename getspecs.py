import socket
import argparse
import sys
import warnings
import logging
import math

from steelscript.common.app import Application
from steelscript.common.service import UserAuth
from steelscript.common import Service
from steelscript.common.exceptions import RvbdHTTPException
from rich import print as rprint

warnings.filterwarnings("ignore")
logging.disable(logging.WARNING)

class NetprofilerCLIApp(Application):

    def __init__(self, host, username, password):
        super(Application).__init__()
        self._api_url = "/api/profiler/1.14/"
        self._hostname = host
        self._username = username
        self._password = password

    def get_hostname(self):
        return self._hostname

    def get_information(self,info):
        _info_url = self._api_url + info
        netprofiler = Service("netprofiler", self._hostname, auth=UserAuth(self._username, self._password),
                              supports_auth_basic=True, supports_auth_oauth=False)
        content_dict = netprofiler.conn.json_request('GET', _info_url,
                                                     extra_headers={'Content-Type': 'application/json'})
        del netprofiler
        return len(content_dict)

    def get_version(self):
        _version_url = '/api/common/1.1/info'
        netprofiler = Service("netprofiler", self._hostname, auth=UserAuth(self._username, self._password),
                              supports_auth_basic=True, supports_auth_oauth=False)
        content_dict = netprofiler.conn.json_request('GET', _version_url,
                                                     extra_headers={'Content-Type': 'application/json'})
        del netprofiler
        _version = content_dict['sw_version']
        _mayor = int(_version[0:2])
        _minor = int(_version[3:5:1])
        if _mayor == 10 and _minor >= 23:
            rprint(f'[bold green]Netprofiler is at version {_mayor}.{_minor} which is supported by Alluvio IQ[/]')
            return True
        else:
            rprint(f'[bold red]Netprofiler is at version {_mayor}.{_minor} which is not supported by Alluvio IQ[/]')
            return False

    def check_netprofiler_reachable(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((self.get_hostname(), 443))
        if result == 0:
            rprint("\n[bold green]Netprofiler is reachable, Port 443 is open[/]")
            sock.close()
            return True
        else:
            rprint("\n[bold red]Netprofiler is not reachable, Port 443 is not open, check ip address or hostname[/]")
            return False

    def create_report(self,applications,hostgroups,interfaces):
        _unique_metrics_applications = applications *5
        _locations = applications * hostgroups
        _unique_metrics_locations = _locations * 5
        _unique_metrics_interfaces = interfaces * 3

        print('*****************************************************************************************************************************\n')
        print('{:20s} {:30s} {:25s} {:30s} {:15s}'.format('Product', 'Object Kind', '#Unique Objects','#Metrics per Object','Unique Metrics'))
        print('{:20s} {:30s} {:25s} {:30s} {:15s}'.format('--------','------------','----------------','-------------------','--------------'))
        print('{:20s} {:30s} {:25s} {:30s} {:15s}'.format('Netprofiler','Applications',f'{applications}','5',f'{_unique_metrics_applications}'))
        print('{:20s} {:30s} {:25s} {:30s} {:15s}'.format('Netprofiler','Locations(hostgroups)',f'{hostgroups}','',''))
        print('{:20s} {:30s} {:25s} {:30s} {:15s}'.format('Netprofiler','Application(locations)',f'{_locations}','5',f'{_unique_metrics_locations}'))
        print('{:20s} {:30s} {:25s} {:30s} {:15s}'.format('Netprofiler','Network interfaces',f'{interfaces}','3',f'{_unique_metrics_interfaces}'))
        rprint('{:20s} {:30s} {:25s} {:30s} {:15s}'.format('Netprofiler total','','','',f'[bold magenta]{_unique_metrics_applications+_unique_metrics_locations+_unique_metrics_interfaces}[/]'))
        print('*****************************************************************************************************************************\n')
        _metric_packs=math.ceil((_unique_metrics_applications+_unique_metrics_locations+_unique_metrics_interfaces)/100000)
        rprint(f'[magenta]Number of metric packs:[/] [bold magenta]{_metric_packs}[/]\n')


def main():

    parser = argparse.ArgumentParser(description='Alluvio IQ price estimator get parameters for Netprofiler.')
    parser.add_argument('-i', '--hostname', metavar='Hostname', help='Netprofilers IPv4 address or Hostname')
    parser.add_argument('-u', '--username', metavar='Username', help='Netprofilers REST API username')
    parser.add_argument('-p', '--password', metavar='Password', help='Netprofilers REST API password')
    args = parser.parse_args()

    ### Ask for Netprofiler ip or hostname if not given via command line
    if args.hostname is None:
        m_hostname = input('Please provide Netprofiler ipv4 address or Hostname: ').strip()
    else:
        m_hostname = args.hostname.strip()

    if args.username is None:
        m_username = input('Please provide Netprofiler username: ').strip()
    else:
        m_username = args.username.strip()

    if args.password is None:
        m_password = input('Please provide Netprofiler password: ').strip()
    else:
        m_password = args.password.strip()

    m_app = NetprofilerCLIApp(m_hostname,m_username,m_password)

    ### Check if port 443 on netprofiler can be reached
    m_reachable = m_app.check_netprofiler_reachable()

    ### Check the netprofiler version
    supported = m_app.get_version()

    ### Connect to Netprofiler
    #if m_reachable and supported:
    if m_reachable:

        ### Get the number of applications via REST
        try:
            m_applications = m_app.get_information('applications')

        except:
            results = f"Error retrieving information on {m_applications}"
            print(results)

        ### Get the number of hostgroups via REST
        try:
            m_hostgroups = m_app.get_information('host_group_types')

        except:
            results = f"Error retrieving information on {m_hostgroups}"
            print(results)

        ### Get the number of network interfaces via REST
        try:
            m_interfaces = m_app.get_information('interfaces')

        except:
            results = f"Error retrieving information on {m_interfaces}"
            print(results)

        m_app.create_report(m_applications,m_hostgroups,m_interfaces)

if __name__ == '__main__':
    main()




