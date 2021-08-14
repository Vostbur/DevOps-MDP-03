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

netconf_data = """
<config><native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
     <hostname>NEWHOSTNAME</hostname>
</native></config>"""


netconf_reply = m.edit_config(target="running", config=netconf_data)


print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())


input("###### Press Enter to continue to Step 3 ######")

# create a new NETCONF config dataset
# it starts with the <config> element
# and inside includes the actual YANG config data
# It defines a Loopback 100 with 100.100.100.100/24
netconf_data = """
<config>
 <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  <interface>
   <Loopback>
    <name>100</name>
    <description>TEST100</description>
    <ip>
     <address>
      <primary>
       <address>100.100.100.100</address>
       <mask>255.255.255.0</mask>
      </primary>
     </address>
    </ip>
   </Loopback>
  </interface>
 </native>
</config>
"""

# to edit the config, use the edit_config() method
# target config and source NETCONF dataset
# print the output (should include <ok/>)
netconf_reply = m.edit_config(target="running", config=netconf_data)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())


input("###### Press Enter to continue to Step 4 ######")

# create a new NETCONF config dataset
# it starts with the <config> element
# and inside includes the actual YANG config data
# It defines a Loopback 111 with 100.100.100.100/24
#  Note that it is the same IP as on the existing Lo100
netconf_data = """
<config>
 <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
  <interface>
   <Loopback>
    <name>111</name>
    <description>TEST111</description>
    <ip>
     <address>
      <primary>
       <address>100.100.100.100</address>
       <mask>255.255.255.0</mask>
      </primary>
     </address>
    </ip>
   </Loopback>
  </interface>
 </native>
</config>
"""

# to edit the config, use the edit_config() method
# target config and source NETCONF dataset
# print the output (in this case this transaction  should fail)
netconf_reply = m.edit_config(target="running", config=netconf_data)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
