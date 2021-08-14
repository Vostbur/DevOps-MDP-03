from netmiko import ConnectHandler

# create a variable object that represents the ssh cli session
sshCli = ConnectHandler(
    device_type='cisco_ios',
    host='192.168.56.101',
    port=22,
    username='cisco',
    password='cisco123!'
)

# send some simple "exec" commands and display the returned output
print("Sending 'sh ip int brief'.")
output = sshCli.send_command("show ip int brief")
print("IP interface status and configuration:\n{}\n".format(output))


# define a set of commands to be run in the config mode
# each command is one item in a Python list data
# this one creates a loopback interface 1 with IP 2.2.2.2/24
config_commands = [
    'int loopback 1',
    'ip address 2.2.2.2 255.255.255.0',
    'description WHATEVER'
]

print("Sending the config commands.")
output = sshCli.send_config_set(config_commands)
print("Config output from the device:\n{}\n".format(output))

print("Sending 'sh ip int brief'.")
output = sshCli.send_command("show ip int brief")
print("IP interface status and configuration:\n{}\n".format(output))

# define a set of commands to be run in the config mode
# each command is one item in a Python list data
# this one creates a loopback interface 2 with IP 2.2.2.2/24
#  note that the IP address is the same as on the existing Lo1
config_commands = [
    'int loopback 2',
    'ip address 2.2.2.2 255.255.255.0',
    'description NEWBUTSAMEIP'
]

print("Sending the config commands.")
output = sshCli.send_config_set(config_commands)
print("Config output from the device:\n{}\n".format(output))

print("Sending 'sh ip int brief'.")
output = sshCli.send_command("show ip int brief")
print("IP interface status and configuration:\n{}\n".format(output))

print("Sending 'sh int desc'.")
output = sshCli.send_command("sh int desc")
print("Interface description:\n{}\n".format(output))
