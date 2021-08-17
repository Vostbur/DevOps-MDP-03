# Get configured interfaces using Netconf
import sys
import xml.dom.minidom

from ncclient import manager

from device_info import ios_xe_16_9_4 as ios_xe

# Doesn't work with IOS XE 17.3.1 !!!
# from device_info import ios_xe_17_3_1 as ios_xe

netconf_filter = 'get_interfaces.xml'


def get_configured_interfaces(xml_filter):
    with manager.connect(**ios_xe, hostkey_verify=False,
                         device_params={'name': 'default'},
                         allow_agent=False, look_for_keys=False) as m:
        with open(xml_filter) as f:
            return(m.get_config('running', f.read()))


def main():
    netconf_reply = get_configured_interfaces(netconf_filter)
    interfaces = xml.dom.minidom.parseString(netconf_reply.xml)

    print(interfaces.toprettyxml())
    print('*' * 40)

    # Example for parse XML
    child_list = interfaces.getElementsByTagName("interfaces")[0].childNodes
    for child in child_list:
        interface = child.getElementsByTagName("name")[0]
        ip = child.getElementsByTagName("ip")
        if ip:
            ip = ip[0].childNodes[0].nodeValue
        else:
            ip = ""
        print(f"{interface.childNodes[0].nodeValue} - {ip}")


if __name__ == '__main__':
    sys.exit(main())

''' OUTPUT
>>>
<?xml version="1.0" ?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" \
    message-id="urn:uuid:2fcc075c-8357-436d-9259-80e14965af48">
        <data>
                <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                        <interface>
                                <name>GigabitEthernet1</name>
                                <description>VBox</description>
                                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd\
                                    </type>
                                <enabled>true</enabled>
                                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
                                <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
                        </interface>
                        <interface>
                                <name>Loopback1</name>
                                <description>WHATEVER</description>
                                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback\
                                    </type>
                                <enabled>true</enabled>
                                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                                        <address>
                                                <ip>2.2.2.2</ip>
                                                <netmask>255.255.255.0</netmask>
                                        </address>
                                </ipv4>
                                <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
                        </interface>
                        <interface>
                                <name>Loopback2</name>
                                <description>NEWBUTSAMEIP</description>
                                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback\
                                    </type>
                                <enabled>true</enabled>
                                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
                                <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
                        </interface>
                        <interface>
                                <name>Loopback99</name>
                                <description>WHATEVER99</description>
                                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback\
                                    </type>
                                <enabled>true</enabled>
                                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                                        <address>
                                                <ip>99.99.99.99</ip>
                                                <netmask>255.255.255.0</netmask>
                                        </address>
                                </ipv4>
                                <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
                        </interface>
                </interfaces>
        </data>
</rpc-reply>

****************************************
GigabitEthernet1 -
Loopback1 - 2.2.2.2
Loopback2 -
Loopback99 - 99.99.99.99
'''
