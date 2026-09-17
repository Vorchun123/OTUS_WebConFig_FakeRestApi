from frontend.page.connection_page.connection_page_electricity_meter import ConnectionPageElectricityMeter


class ElectricityMeterConnectionBuilder:
    URL = 'http://localhost:5004/setting/connection'

    def __init__(self, browser):
        self.browser = browser
        self.interface_type = None
        self.port = None
        self.host = None
        self.port_ip = None
        self.password = None
        self.authorization_type = None
        self.logical_address = '1'
        self.physical_address = '17'
        self.size_address = '4'
        self.timeout = '5000'
        self.retries = '3'
        self.delay = '0'
        self.pdu = '65635'
        self.keep_alive = '5000'

    def with_opto(self, port):
        self.interface_type = 'Opto'
        self.port = port
        return self

    def with_rs_485(self, port):
        self.interface_type = 'Rs485'
        self.port = port
        return self

    def with_tcp_ip(self, host, port_ip):
        self.interface_type = 'TcpIP'
        self.host = host
        self.port_ip = port_ip
        return self

    def with_configurator_access(self):
        self.authorization_type = 'ConfiguratorAccess'
        self.password = '0000000100000001'
        return self

    def with_read_access(self):
        self.authorization_type = 'ReaderAccess'
        self.password = '00000001'
        return self

    def with_public_access(self):
        self.authorization_type = 'PublicAccess'
        self.password = None
        return self

    def server_address_parameters(self, logical_address, physical_address, size_address):
        self.logical_address = logical_address
        self.physical_address = physical_address
        self.size_address = size_address
        return self

    def additional_parameters(self, timeout, retries, delay, pdu, keep_alive):
        self.timeout = timeout
        self.retries = retries
        self.delay = delay
        self.pdu = pdu
        self.keep_alive = keep_alive
        return self

    def build(self):
        meter_connect = ConnectionPageElectricityMeter(self.browser)

        meter_connect.load_page_url()

        if self.interface_type == "Opto":
            meter_connect.opto(self.port)
        elif self.interface_type == 'Rs485':
            meter_connect.rs_485(self.port)
        elif self.interface_type == 'TcpIP':
            meter_connect.tcp_ip(self.host, self.port_ip)

        if self.authorization_type == 'ConfiguratorAccess':
            meter_connect.authorization_configuration()
        elif self.authorization_type == 'ReaderAccess':
            meter_connect.authorization_read()
        elif self.authorization_type == 'PublicAccess':
            meter_connect.authorization_public()

        meter_connect.server_address(self.logical_address,
                                     self.physical_address,
                                     self.size_address)
        meter_connect.additionally(self.timeout, self.retries,
                                   self.delay, self.pdu, self.keep_alive)
        meter_connect.connection()

        return meter_connect
