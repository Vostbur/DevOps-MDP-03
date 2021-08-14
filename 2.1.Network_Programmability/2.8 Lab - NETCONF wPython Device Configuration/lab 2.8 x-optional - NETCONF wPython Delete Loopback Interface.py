# Follow up of the lab 2.8 part 2 - NETCONF wPython Device Configuration
# Delete a Loopback interface

from ncclient import manager
import xml.dom.minidom

# create a variable object that represents the NETCONF session
m = manager.connect(
    host="192.168.56.101",
    port=830,
    username="cisco",
    password="cisco123!",
    hostkey_verify=False
)

# the important XML tag parameters are:
#  define the he "nc" namespace: xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"
#  call from the "nc" namespace the operation to delete  nc:operation="delete"
netconf_data = """
<config>
 <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  <interface>
   <Loopback xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" nc:operation="delete">
    <name>100</name>
   </Loopback>
  </interface>
 </native>
</config>
"""

netconf_reply = m.edit_config(target="running", config=netconf_data)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
