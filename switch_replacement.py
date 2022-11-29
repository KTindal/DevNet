### switch_replacement.py ###
### This script is automates the replacement of a switch/stack in our environment by correctly configuring VTP, AAA, TACACS+, and Ports. ##
from csv import reader
from datetime import date, datetime
from netmiko import ConnectHandler
from ping3 import ping, verbose_ping
import getpass
import os
import sys
import ipaddress
import serial
from time import sleep
import sys


# This function pushes the new config to the device and makes sure it follows the standard
def push_new_config():

    # Open serial port. THe settings are set to the Cisco default.
    serial_port = serial.Serial(2, baudrate=9600, timeout=None, parity=serial.PARITY_NONE,
                                bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, xonxoff=False)

#    Flush serial port input(information waiting to be received)
    serial_port.flushInput()

    print(serial_port.name)
# enter command to get to IOS cli
    serial_port.write("\n".encode())
# sends the "?" to the IOS cli for testing
    serial_port.write("?".encode())

    bytes_to_read = serial_port.inWaiting()

# Give the line a small amount of time to receive input
    sleep(.5)

# This while loop iterates the commands to send through the serial connection
    while bytes_to_read < serial_port.inWaiting():
        bytes_to_read = serial_port.inWaiting()
        sleep(1)


push_new_config()
# This function establishes the connection to the old host and pulls the configuration


def get_old_config(host, username, password, enable_secret):
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
    output = net_connect.send_command("show ver")
    print(output)


# This function defines the initial variables needed to pull the config from the old host and checks their validity.
def initial_input():
    print(
        "Hello! This script autoamtes switch/stack replacement. \nEnsure the information you enter is accurate."
    )

    old_host = input("\nEnter the IP of the old_host: ")

    username = input("\nEnter the username to establish SSH to the old host: ")

    password = input("\nEnter the password to establish SSH to the old host: ")

    enable_secret = input("\nEnter the enable secret for the old host: ")

    info_check = input(
        f"\nJust to make sure, you want to repalce {old_host}\n and use {username} to establish the connection? (yes/no) "
    )

    if info_check.lower() == "yes":
        ip = old_host
        ip_ping = ping(ip)
        if ip_ping == None:
            print("\nThe IP provided did not respond, reinitializing program.")
            print("\n." * 3)
            initial_input()
        else:
            print("Information Confirmed. Obtaining old configuration.")
            get_old_config(old_host, username, password, enable_secret)

    elif info_check.lower() == "no":
        print("\nYou entered 'no', reinitializing program.")
        print("\n." * 3)
        initial_input()


initial_input()
