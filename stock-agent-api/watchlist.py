from flask import Blueprint, request, jsonify
import json
import os

watchlist_bp = Blueprint('watchlist', __name__)

WATCHLIST_FILE = 'watchlist.json'

def load_watchlist():
    if not os.path.exists(WATCHLIST_FILE):
        return {}
    with open(WATCHLIST_FILE) as f:
        return json.load(f)

def save_watchlist(data):
    with open(WATCHLIST_FILE, 'w') as f:
        json.dump(data, f)

@watchlist_bp.route('/watchlist', methods=['GET'])
def get_watchlist():
    data = load_watchlist()
    user = "user1"  # משתמש ברירת מחדל
    return jsonify({"watchlist": data.get(user, [])})

@watchlist_bp.route('/watchlist', methods=['POST'])
def add_to_watchlist():
    data = load_watchlist()
    user = "user1"
    symbol = request.json.get('symbol')
    if not symbol:
        return jsonify({"error": "symbol is required"}), 400
    user_list = data.get(user, [])
    if symbol not in user_list:
        user_list.append(symbol)
    data[user] = user_list
    save_watchlist(data)
    return jsonify({"message": f"{symbol} added", "watchlist": user_list})

@watchlist_bp.route('/watchlist', methods=['DELETE'])
def delete_from_watchlist():
    data = load_watchlist()
    user = "user1"
    symbol = request.json.get('symbol')
    if not symbol:
        return jsonify({"error": "symbol is required"}), 400
    user_list = data.get(user, [])
    if symbol in user_list:
        user_list.remove(symbol)
    data[user] = user_list
    save_watchlist(data)
    return jsonify({"message": f"{symbol} removed", "watchlist": user_list})
