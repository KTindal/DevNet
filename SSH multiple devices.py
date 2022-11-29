## SSH to multiple hosts from a text file host.txt ##
from netmiko import ConnectHandler

with open('host.txt') as switches:
    for IP in switches:
        Switch = {
            'device_type': 'cisco_ios',
            'ip': IP,
            'username': 'admin',
            'password': 'cisco'
        }

        net_connect = ConnectHandler(**Switch)

        print('Connecting to ' + IP)
        print('-'*79)
        output = net_connect.send_command('sh ver')
        print(output)
        print()
        print('-'*79)

# Close Connection
net_connect.disconnect()

