## Automated Python Script to backup Cisco L2/L3 running configs ##
## CSV of hosts and service account information are needed ##
## Ideally scheduled with cron ##


# All pre-installed besides Netmiko.
from csv import reader
from datetime import date, datetime
from netmiko import ConnectHandler
from ping3 import ping, verbose_ping 
import getpass
import os
#import sys

#sys.tracebacklimit = 0

# Checks if the folder exists, if not, it creates it.
if not os.path.exists('mnt/backups/'):
    os.makedirs('mnt/backups/')

# Current time and formats it to the North American time of Month, Day, and Year.
now = datetime.now()
dt_string = now.strftime("%m-%d-%Y_%H-%M")

# Gives us the information we need to connect.
def get_saved_config(host, username, password, enable_secret):
    cisco_ios = {
        'device_type': 'cisco_ios',
        'host': host,
        'username': username,
        'password': password,
        'secret': enable_secret,
    }
    # Creates the connection to the device.
    net_connect = ConnectHandler(**cisco_ios)
    net_connect.enable()
    # Gets the running configuration.
    output = net_connect.send_command("show run")
    # Gets and splits the hostname for the output file name.
    hostname = net_connect.send_command("show ver | i uptime")
    hostname = hostname.split()
    hostname = hostname[0]
    # Creates the file name, which is the hostname, and the date and time.
    fileName = hostname + "_" + dt_string
    # Creates the text file in the mnt/backups/ folder with the special name, and writes to it.
    backupFile = open("/mnt/backups/" + fileName + ".txt", "w+")
    backupFile.write(output)
    print("Outputted to " + fileName + ".txt!")

# Gets the CSV file name, and grabs the information from it.
with open('/home/infadmin/Python-Cisco-Backup/cisco_backup_hosts.csv') as csvfile:
        csv_reader = reader(csvfile)
        list_of_rows = list(csv_reader)
        rows = len(list_of_rows)
        while rows >= 2:
            rows = rows - 1
            ip = list_of_rows[rows][0]
            ip_ping = ping(ip)
            if ip_ping == None:
                fileName = "downDevices_" + dt_string + ".txt"
                downDeviceOutput = open("/mnt/backups/" + fileName, "a")
                downDeviceOutput.write(str(ip) + "\n")
                print(str(ip) + " is down!")
            else:
                get_saved_config(list_of_rows[rows][0], list_of_rows[rows][1], list_of_rows[rows][2], list_of_rows[rows][3])