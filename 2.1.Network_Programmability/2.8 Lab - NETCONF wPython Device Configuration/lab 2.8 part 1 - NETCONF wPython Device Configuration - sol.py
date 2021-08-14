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

# use the "get_config" method of the NETCONF object
# to get back the current "source" configuration
netconf_reply = m.get_config(source="running")
print(netconf_reply)


input("###### Press Enter to continue to Step 3 ######")
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())


input("###### Press Enter to continue to Step 4 ######")
# limit the output from the NETCONF reply using a NETCONF filter
# in this case, filtering only data defined in
# the native cisco ios xe yang model
netconf_filter = """
<filter>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native" />
</filter>
"""

# use the "get_config" method of the NETCONF object
# to get back the current "source" configuration
# limiting the output using the filter
netconf_reply = m.get_config(source="running", filter=netconf_filter)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
