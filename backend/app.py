from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from database import Database
from models import User
import webbrowser
from colorama import init, Fore, Back, Style
import os
import threading
import time

# Initialize colorama for colored terminal output
init()

app = Flask(__name__, static_folder='../frontend')
CORS(app)
db = Database()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_terminal()
    print(f"{Fore.CYAN}╔══════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║      Saved and Single Server         ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════════╝{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Server Status: Running{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}App URL: http://localhost:5000{Style.RESET_ALL}")
    print("\nPress Ctrl+C to stop the server\n")

# Serve frontend files
@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('../frontend', path)

# Test route
@app.route('/api/test')
def test():
    return jsonify({"message": "Backend is working!"})

@app.route('/api/users/random')
def get_random_user():
    # For testing, return a dummy user
    dummy_user = {
        "id": "1",
        "name": "John Doe",
        "age": 25,
        "bio": "Love hiking and coffee ☕",
        "photos": ["https://picsum.photos/400/600"]
    }
    return jsonify(dummy_user)

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(
        name=data['name'],
        age=data['age'],
        bio=data['bio'],
        photos=data['photos']
    )
    db.add_user(user)
    print(f"{Fore.GREEN}➜ New user created: {user.name}{Style.RESET_ALL}")
    return jsonify({"message": "User created successfully"})

@app.route('/api/swipe', methods=['POST'])
def swipe():
    data = request.json
    if data['direction'] == 'right':
        if db.check_match(data['swiper_id'], data['swiped_id']):
            print(f"{Fore.MAGENTA}➜ New match created!{Style.RESET_ALL}")
            return jsonify({"match": True})
    print(f"{Fore.BLUE}➜ New swipe recorded{Style.RESET_ALL}")
    db.add_swipe(data['swiper_id'], data['swiped_id'], data['direction'])
    return jsonify({"match": False})

def open_browser():
    time.sleep(1.5)  # Wait for server to start
    webbrowser.open('http://localhost:5000')

if __name__ == '__main__':
    print_banner()
    # Open browser in a separate thread
    threading.Thread(target=open_browser).start()
    app.run(host='0.0.0.0', port=5000, debug=False) 