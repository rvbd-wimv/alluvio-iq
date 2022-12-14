import socket
import argparse
import sys
import warnings
import logging
import math

import pwinput
from steelscript.common.service import UserAuth
from steelscript.common import Service
from steelscript.netprofiler.core import NetProfiler
from steelscript.netprofiler.core.filters import TimeFilter
from steelscript.netprofiler.core.report import TrafficSummaryReport
from steelscript.common.exceptions import RvbdHTTPException
from steelscript.netim.core import NetIM
from rich import print as rprint

warnings.filterwarnings("ignore")
logging.disable(logging.WARNING)

class AlluvioDevice():

    def __init__(self,device_type,hostname,port):
        self._device_type = device_type
        self._hostname = hostname
        self._port = port

    def get_hostname(self):
        return self._hostname

    def get_port(self):
        return self._port

    def get_device_type(self):
        return self._device_type

    def check_reachable(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((self.get_hostname(), self.get_port()))
        except:
            rprint(f'\n[bold red]unable to open socket to {self.get_hostname()}[/]')
            sys.exit()

        if result == 0:
            rprint(f"\n[bold green]{self.get_device_type()} is reachable, Port {self.get_port()} is open[/]")
            sock.close()
            return True
        else:
            rprint(f"\n[bold red]{self.get_device_type()} is not reachable, Port {self.get_port()} is not open, check ip address or hostname[/]")
            return False


class NetIMCLIApp(AlluvioDevice):

    def __init__(self, device_type,hostname,port,username, password):
        super(AlluvioDevice).__init__()
        self._device_type = device_type
        self._hostname = hostname
        self._port = port
        self._username = username
        self._password = password

    def get_json_result(self,api_url):
        _m_netim = NetIM(self._hostname,UserAuth(self._username,self._password))
        _m_dict = _m_netim._get_json(api_url)
        _m_results = []
        _total_devices = 0

        for i in range(len(_m_dict['items'])):

            _total_devices = _total_devices + _m_dict['items'][i]['aggregatedPollerStatsBean']['totalDevices']

            for key in _m_dict['items'][i]:
                if 'name' in key:
                    if 'SNMP' in _m_dict['items'][i][key]:
                        _total_interfaces = _m_dict['items'][i]['aggregatedPollerStatsBean']['polledIfcs']

        _m_results.append(_total_devices)
        _m_results.append(_total_interfaces)
        return _m_results

    def create_report(self,devices,interfaces):
        _unique_metrics_interfaces = interfaces *7

        print('*****************************************************************************************************************************\n')
        print('{:20s} {:40s} {:25s} {:30s} {:15s}'.format('Product', 'Object Kind', '#Unique Objects','#Metrics per Object','Unique Metrics'))
        print('{:20s} {:40s} {:25s} {:30s} {:15s}'.format('--------','------------','----------------','-------------------','--------------'))
        print('{:20s} {:40s} {:25s} {:30s} {:15s}'.format('NetIM','Network Interfaces',f'{interfaces}','7',f'{_unique_metrics_interfaces}'))
        print('{:20s} {:40s} {:25s} {:30s} {:15s}'.format('NetIM','Network Devices',f'{devices}','1',f'{devices}'))
        rprint('{:20s} {:40s} {:25s} {:30s} {:15s}'.format('NetIM total',' ',' ',' ',f'[bold magenta]{_unique_metrics_interfaces+devices}[/]'))
        print('*****************************************************************************************************************************\n')
        _metric_packs=_unique_metrics_interfaces+devices
        return _metric_packs


class NetprofilerCLIApp(AlluvioDevice):

    def __init__(self, device_type,hostname,port,username, password):
        super(AlluvioDevice).__init__()
        self._device_type = device_type
        self._hostname = hostname
        self._port = port
        self._username = username
        self._password = password

    def _count_entries(self,netprofiler, columns, grouping, timefilter):
        # initialize a new report, and run it
        # set maximum number of rows to 100K so we are sure to get all data (more or less)
        report = TrafficSummaryReport(netprofiler)
        report.run(grouping, columns, timefilter=timefilter, limit=100000)

        # grab the data, and legend (it should be what we passed in for most cases)
        data = report.get_data(limit=100000)

        # once we have what we need, delete the report from the NetProfiler
        report.delete()

        # now count how many entries there were and return the value
        if data != None:
            nentries = len(data)
        else:
            nentries = 0
        return nentries

    def get_information(self,info,timerange):

        netprofiler = NetProfiler(self._hostname,auth=UserAuth(self._username, self._password))

        # create the time-range object
        timefilter = TimeFilter.parse_range(timerange)

        if info == 'applications':
            # Collect the data for the number of applications
            columns = [netprofiler.columns.key.app_name,
                       netprofiler.columns.value.avg_bytes]
            napps = self._count_entries(netprofiler, columns, 'app', timefilter)
            del netprofiler
            return napps

        if info == 'host_group_types':
            # Collect the data for the number of host groups - ByLocation is the default
            columns = [netprofiler.columns.key.group_name,
                       netprofiler.columns.value.avg_bytes]
            ngrps = self._count_entries(netprofiler, columns, 'gro', timefilter)
            del netprofiler
            return ngrps

        if info == 'interfaces':
            columns = [netprofiler.columns.key.interface,
                       netprofiler.columns.value.avg_bytes]
            nifcs = self._count_entries(netprofiler, columns, 'ifc', timefilter)
            del netprofiler
            return nifcs

    def get_version(self):
        _version_url = '/api/common/1.1/info'
        try:
            netprofiler = Service("netprofiler", self._hostname, auth=UserAuth(self._username, self._password),supports_auth_basic=True, supports_auth_oauth=False)
        except RvbdHTTPException:
            rprint(f'[bold red]Username or Password incorrect![/]')
            sys.exit()

        try:
            content_dict = netprofiler.conn.json_request('GET', _version_url,extra_headers={'Content-Type': 'application/json'})
        except RvbdHTTPException:
            rprint(f'[bold red]Something went wrong! Is this a NetProfiler appliance?[/]')
            sys.exit()

        del netprofiler
        _version = content_dict['sw_version']
        _mayor = int(_version[0:2])
        _minor = int(_version[3:5:1])
        if _mayor == 10 and _minor >= 23:
            rprint(f'[bold green]NetProfiler is at version {_mayor}.{_minor} which is supported by Alluvio IQ[/]')
            return True
        else:
            rprint(f'[bold red]NetProfiler is at version {_mayor}.{_minor} which is not supported by Alluvio IQ[/]')
            return False

    def create_report(self,applications,hostgroups,interfaces):
        _unique_metrics_applications = applications *5
        _locations = applications * hostgroups
        _unique_metrics_locations = _locations * 5
        _unique_metrics_interfaces = interfaces * 3

        print('*****************************************************************************************************************************\n')
        print('{:20s} {:40s} {:25s} {:30s} {:15s}'.format('Product', 'Object Kind', '#Unique Objects','#Metrics per Object','Unique Metrics'))
        print('{:20s} {:40s} {:25s} {:30s} {:15s}'.format('--------','------------','----------------','-------------------','--------------'))
        print('{:20s} {:40s} {:25s} {:30s} {:15s}'.format('NetProfiler','Applications',f'{applications}','5',f'{_unique_metrics_applications}'))
        print('{:20s} {:40s} {:25s} {:30s} {:15s}'.format('NetProfiler','Locations (ByLocation Host Groups)',f'{hostgroups}','',''))
        print('{:20s} {:40s} {:25s} {:30s} {:15s}'.format('NetProfiler','Applications * Locations',f'{_locations}','5',f'{_unique_metrics_locations}'))
        print('{:20s} {:40s} {:25s} {:30s} {:15s}'.format('NetProfiler','Network interfaces',f'{interfaces}','3',f'{_unique_metrics_interfaces}'))
        rprint('{:20s} {:40s} {:25s} {:30s} {:15s}'.format('NetProfiler total',' ',' ',' ',f'[bold magenta]{_unique_metrics_applications+_unique_metrics_locations+_unique_metrics_interfaces}[/]'))
        print('*****************************************************************************************************************************\n')
        _metric_packs=_unique_metrics_applications+_unique_metrics_locations+_unique_metrics_interfaces
        return _metric_packs


def main(args):

    m_totals_netprofiler = None
    m_totals_netim = None

    if not args.nonetprofiler:
        ### Ask for Netprofiler ip or hostname if not given via command line
        if args.hostname is None:
            m_hostname = input('Please provide NetProfiler ipv4 address or Hostname: ').strip()
        else:
            m_hostname = args.hostname.strip()

        if args.username is None:
            m_username = input('Please provide NetProfiler username: ').strip()
        else:
            m_username = args.username.strip()

        if args.password is None:
            m_password = pwinput.pwinput(prompt='Please provide NetProfiler password: ', mask='*').strip()
            #m_password = input('Please provide NetProfiler password: ').strip()
        else:
            m_password = args.password.strip()

        if args.timerange is None:
            m_timerange = 'previous 1 d'
        else:
            m_timerange = args.timerange.strip()

        m_netprofiler_app = NetprofilerCLIApp('NetProfiler',m_hostname,443,m_username,m_password)

        ### Check if port 443 on netprofiler can be reached
        m_reachable = m_netprofiler_app.check_reachable()

        ### Check the netprofiler version
        #if m_reachable:
        #    supported = m_app.get_version()

        ### Connect to Netprofiler
        #if m_reachable and supported:
        if m_reachable:

            ### Check the netprofiler version
            supported = m_netprofiler_app.get_version()

            ### Get the number of applications via REST
            try:
                m_applications = m_netprofiler_app.get_information('applications',m_timerange)

            except:
                results = f"Error retrieving information on {m_applications}"
                print(results)

            ### Get the number of hostgroups via REST
            try:
                m_hostgroups = m_netprofiler_app.get_information('host_group_types',m_timerange)

            except:
                results = f"Error retrieving information on {m_hostgroups}"
                print(results)

            ### Get the number of network interfaces via REST
            try:
                m_interfaces = m_netprofiler_app.get_information('interfaces',m_timerange)

            except:
                results = f"Error retrieving information on {m_interfaces}"
                print(results)

            m_totals_netprofiler = m_netprofiler_app.create_report(m_applications,m_hostgroups,m_interfaces)

    #Check if netIM needs to added
    if args.netim:

        if args.hostname is None:
            m_netim_hostname = input('Please provide NetIM ipv4 address or Hostname: ').strip()
        else:
            m_netim_hostname = args.hostname-netim.strip()

        if args.username is None:
            m_netim_username = input('Please provide NetIM username: ').strip()
        else:
            m_netim_username = args.username-netim.strip()

        if args.password is None:
            m_netim_password = pwinput.pwinput(prompt='Please provide NetIM password: ', mask='*').strip()
            #m_netim_password = input('Please provide NetIM password: ').strip()
        else:
            m_netim_password = args.password-netim.strip()

        m_netim_app = NetIMCLIApp('NetIM',m_netim_hostname,8543,m_netim_username,m_netim_password)

        m_netim_reachable = m_netim_app.check_reachable()

        if m_netim_reachable:
            _api_url = '/api/netim/v2/pollers-stats'
            list_result = m_netim_app.get_json_result(_api_url)
            m_totals_netim = m_netim_app.create_report(list_result[0],list_result[1])

    else:
        sys.exit()

    if m_totals_netprofiler is None:
        m_totals_netprofiler = 0
    if m_totals_netim is None:
        m_totals_netim = 0

    m_total = m_totals_netprofiler + m_totals_netim
    rprint(f'[magenta]Estimated total:[/] [bold magenta]{m_total}[/]\n')
    rprint(f'[magenta]Number of metric packs:[/] [bold magenta]{math.ceil((m_total) / 100000)}[/]\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Alluvio IQ price estimator get parameters for NetProfiler.')
    parser.add_argument('-i', '--hostname', metavar='Hostname', help='NetProfiler IPv4 address or Hostname')
    parser.add_argument('-u', '--username', metavar='Username', help='NetProfiler REST API username')
    parser.add_argument('-p', '--password', metavar='Password', help='NetProfiler REST API password')
    parser.add_argument('-t', '--timerange', metavar='TimeRange',help='Time range to be used for the data collection default="previous 1 d".')
    parser.add_argument('-in', '--hostname-netim', metavar='Hostname', help='NetIM IPv4 address or Hostname')
    parser.add_argument('-un', '--username-netim', metavar='Username', help='NetIM REST API username')
    parser.add_argument('-pn', '--password-netim', metavar='Password', help='NetIM REST API password')
    parser.add_argument("--nonetprofiler", help="Remove NetProfiler sizing", action="store_true")
    parser.add_argument("--netim", help="Add NetIM sizing", action="store_true")
    args = parser.parse_args()
    main(args)
