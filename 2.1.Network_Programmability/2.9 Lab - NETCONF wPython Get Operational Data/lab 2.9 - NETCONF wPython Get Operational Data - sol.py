import xmltodict
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

# define a NETCONF filter to get only the required data
# w/o this filter the NETCONF GET operation will try to
# return everything and will crash (aka. similar to 'debug all')
# the filter defines that we want to get only data defined
# in the ietf-interfaces model in the interfaces-state container
netconf_filter = """
<filter>
 <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>
</filter>
"""

# using the NETCONF get method, get data:
netconf_reply = m.get(filter=netconf_filter)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())


input("###### Press Enter to continue to Step 3 ######")

# use the xmldict module to parse the NETCONF reply (in xml form)
# the retuned object is a Python dictionary
netconf_reply_dict = xmltodict.parse(netconf_reply.xml)

# loop over the Python dictionary object and print the interesting data
for interface in netconf_reply_dict["rpc-reply"]["data"]["interfaces-state"]["interface"]:
    print("Name: {} MAC: {} Input: {} Output {}".format(
        interface["name"],
        interface["phys-address"],
        interface["statistics"]["in-octets"],
        interface["statistics"]["out-octets"]
    )
    )
