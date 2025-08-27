from flask import Flask, request, jsonify
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import json
import threading

# ===== CONFIG =====
BOT_TOKEN = '8364904135:AAHfzDZ2sODAFHGXinNO5PdgDdd7YtvdHa8'
OWNER_ID = 6426997934
MEMBERS_FILE = 'members.json'
# ==================

bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)

# Members helper functions
def load_members():
    try:
        with open(MEMBERS_FILE, 'r') as f:
            return json.load(f).get("members", [])
    except:
        return []

def save_members(members):
    with open(MEMBERS_FILE, 'w') as f:
        json.dump({"members": members}, f)

def send_booking_message(message_text):
    members = load_members()
    for user_id in members:
        bot.send_message(chat_id=user_id, text=message_text)

# Flask API route for booking
@app.route('/book', methods=['POST'])
def book_ride():
    data = request.json
    user_name = data.get("user_name")
    from_place = data.get("from_place")
    to_place = data.get("to_place")

    message = f"New E-Rickshaw booked!\nUser: {user_name}\nFrom: {from_place}\nTo: {to_place}"
    send_booking_message(message)
    return jsonify({"status": "success", "message": "Notification sent"})

# Telegram bot commands
def add_member(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        update.message.reply_text("You are not authorized.")
        return
    if len(context.args) != 1:
        update.message.reply_text("Usage: /add_member <user_id>")
        return
    user_id = int(context.args[0])
    members = load_members()
    if user_id not in members:
        members.append(user_id)
        save_members(members)
        update.message.reply_text(f"Member {user_id} added.")
    else:
        update.message.reply_text("Member already exists.")

def remove_member(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        update.message.reply_text("You are not authorized.")
        return
    if len(context.args) != 1:
        update.message.reply_text("Usage: /remove_member <user_id>")
        return
    user_id = int(context.args[0])
    members = load_members()
    if user_id in members:
        members.remove(user_id)
        save_members(members)
        update.message.reply_text(f"Member {user_id} removed.")
    else:
        update.message.reply_text("Member not found.")

def start_bot():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("add_member", add_member))
    dp.add_handler(CommandHandler("remove_member", remove_member))
    updater.start_polling()

# Start bot in background
threading.Thread(target=start_bot).start()
