import os
import time
import threading
import telebot
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8216730412:AAGhjFoxoiUNvtq0gYJSuqPU58ARRX-NOJo"
MONGO_URI = "mongodb+srv://sanjublogscom_db_user:Mahakal456@cluster0.cwi48dt.mongodb.net/telegram_bot_db?appName=Cluster0"
ADMIN_IDS = [6335046711, 8552084416]
PUBLIC_CHANNEL = "-1003582278269"
PRIVATE_CHANNEL = "-1003582278269"
MAIN_LINK = "https://t.me/+_FVPR7qaQuRhYmY1"
BACKUP_LINK = "https://t.me/+FkReusMf7r44Nzhl"

bot = telebot.TeleBot(BOT_TOKEN)

# In-memory storage (temporary, data lost on restart)
media_store = {}

def save_media(media_id, files):
    media_store[media_id] = files

def get_media(media_id):
    return media_store.get(media_id, [])

def delete_media(media_id):
    if media_id in media_store:
        del media_store[media_id]

@bot.message_handler(commands=['start'])
def start(message):
    params = message.text.split(' ')[1] if len(message.text.split(' ')) > 1 else None
    user_id = message.from_user.id
    
    if params and not params.startswith("joined_"):
        media_id = params
        try:
            pub_status = bot.get_chat_member(PUBLIC_CHANNEL, user_id).status
            priv_status = bot.get_chat_member(PRIVATE_CHANNEL, user_id).status
            if pub_status in ['member', 'administrator', 'creator'] and priv_status in ['member', 'administrator', 'creator', 'left']:
                files = get_media(media_id)
                if not files:
                    bot.send_message(message.chat.id, "❌ No media found for this link.")
                else:
                    username = f"@{message.from_user.username}" if message.from_user.username else "No username"
                    bot.send_message(6335046711, f"🔗 Link opened\n{message.from_user.first_name}\n👤 {user_id}\n{username}")
                    
                    sent_msgs = []
                    for f in files:
                        m = None
                        if f["type"] == "photo":
                            m = bot.send_photo(message.chat.id, f["file_id"], caption=f.get("caption", ""), protect_content=True)
                        elif f["type"] == "video":
                            m = bot.send_video(message.chat.id, f["file_id"], caption=f.get("caption", ""), protect_content=True)
                        elif f["type"] == "audio":
                            m = bot.send_audio(message.chat.id, f["file_id"], protect_content=True)
                        elif f["type"] == "voice":
                            m = bot.send_voice(message.chat.id, f["file_id"], protect_content=True)
                        elif f["type"] == "document":
                            m = bot.send_document(message.chat.id, f["file_id"], protect_content=True)
                        elif f["type"] == "animation":
                            m = bot.send_animation(message.chat.id, f["file_id"], protect_content=True)
                        elif f["type"] == "sticker":
                            m = bot.send_sticker(message.chat.id, f["file_id"], protect_content=True)
                        if m:
                            sent_msgs.append(m.message_id)
                    
                    note = bot.send_message(message.chat.id, "⚠️ <b>Note:</b> Files will be deleted after <b>30 minutes</b>.", parse_mode="html")
                    sent_msgs.append(note.message_id)
                    
                    threading.Thread(target=delete_after, args=(message.chat.id, sent_msgs, media_id)).start()
            else:
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("📢 Join Channel", url=MAIN_LINK))
                markup.add(InlineKeyboardButton("📢 Join Channel ", url=BACKUP_LINK))
                markup.add(InlineKeyboardButton("🌹 I Joined", url=f"https://t.me/{bot.get_me().username}?start=joined_{media_id}"))
                bot.send_message(message.chat.id, "🚫 <b>Phele channel Join to karle babu !</b>\n\nFriends ko bhi refer kar diyo 😋", parse_mode="html", reply_markup=markup)
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Error checking subscription: {str(e)}")
    
    elif params and params.startswith("joined_"):
        media_id = params.split("_")[1]
        try:
            pub_status = bot.get_chat_member(PUBLIC_CHANNEL, user_id).status
            priv_status = bot.get_chat_member(PRIVATE_CHANNEL, user_id).status
            if pub_status in ['member', 'administrator', 'creator'] and priv_status in ['member', 'administrator', 'creator', 'left']:
                files = get_media(media_id)
                if not files:
                    bot.send_message(message.chat.id, "❌ No media found.")
                else:
                    username = f"@{message.from_user.username}" if message.from_user.username else "No username"
                    bot.send_message(6335046711, f"🔗 Link opened\n{message.from_user.first_name}\n👤 {user_id}\n{username}")
                    
                    sent_msgs = []
                    for f in files:
                        m = None
                        if f["type"] == "photo":
                            m = bot.send_photo(message.chat.id, f["file_id"], caption=f.get("caption", ""), protect_content=True)
                        elif f["type"] == "video":
                            m = bot.send_video(message.chat.id, f["file_id"], caption=f.get("caption", ""), protect_content=True)
                        elif f["type"] == "audio":
                            m = bot.send_audio(message.chat.id, f["file_id"], protect_content=True)
                        elif f["type"] == "voice":
                            m = bot.send_voice(message.chat.id, f["file_id"], protect_content=True)
                        elif f["type"] == "document":
                            m = bot.send_document(message.chat.id, f["file_id"], protect_content=True)
                        elif f["type"] == "animation":
                            m = bot.send_animation(message.chat.id, f["file_id"], protect_content=True)
                        elif f["type"] == "sticker":
                            m = bot.send_sticker(message.chat.id, f["file_id"], protect_content=True)
                        if m:
                            sent_msgs.append(m.message_id)
                    
                    note = bot.send_message(message.chat.id, "⚠️ <b>Note:</b> Files will be deleted after <b>30 minutes</b>.", parse_mode="html")
                    sent_msgs.append(note.message_id)
                    
                    threading.Thread(target=delete_after, args=(message.chat.id, sent_msgs, media_id)).start()
            else:
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton("📢 Join Main Channel", url=MAIN_LINK))
                markup.add(InlineKeyboardButton("📢 Join Backup Channel (Request)", url=BACKUP_LINK))
                markup.add(InlineKeyboardButton("✅ Check Again", url=f"https://t.me/{bot.get_me().username}?start=joined_{media_id}"))
                bot.send_message(message.chat.id, "🚫 <b>Phele channel Join to karle babu !</b>\n\nFriends ko bhi refer kar diyo 😋", parse_mode="html", reply_markup=markup)
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Error: {str(e)}")
    
    else:
        if user_id in ADMIN_IDS:
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("📨 Start Uploading", callback_data="/upload"))
            bot.send_message(message.chat.id, "<b>📨 Welcome to Multi File Sharing Bot!</b>\n\nUse /upload to add files.", parse_mode="html", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "<b>Dude channel vali link use kar video ke liye👇\nChannel:- t.me/+_FVPR7qaQuRhYmY1\n<code>Join bhi karliyo bhai 😉</code></b>", parse_mode="HTML")

@bot.message_handler(commands=['upload'])
def upload(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.send_message(message.chat.id, "❌ You are not authorized to use this command.")
        return
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.add("✅")
    media_id = str(int(time.time()))
    bot.send_message(message.chat.id, "👉 Send me the text you want to upload. When you are done.", reply_markup=markup)
    bot.register_next_step_handler(message, handle_media, media_id=media_id, files=[])

def handle_media(message, media_id, files):
    if message.text == "✅":
        if files:
            save_media(media_id, files)
            shareable_link = f"https://t.me/{bot.get_me().username}?start={media_id}"
            bot.send_message(message.chat.id, f"✅ Upload complete!\nShare this link:\n{shareable_link}", reply_markup=ReplyKeyboardRemove())
        else:
            bot.send_message(message.chat.id, "❌ No media was uploaded.")
    else:
        media_entry = None
        if message.photo:
            media_entry = {"type": "photo", "file_id": message.photo[-1].file_id, "caption": message.caption or ""}
        elif message.video:
            media_entry = {"type": "video", "file_id": message.video.file_id, "caption": message.caption or ""}
        elif message.audio:
            media_entry = {"type": "audio", "file_id": message.audio.file_id}
        elif message.voice:
            media_entry = {"type": "voice", "file_id": message.voice.file_id}
        elif message.document:
            media_entry = {"type": "document", "file_id": message.document.file_id}
        elif message.animation:
            media_entry = {"type": "animation", "file_id": message.animation.file_id}
        elif message.sticker:
            media_entry = {"type": "sticker", "file_id": message.sticker.file_id}
        
        if media_entry:
            files.append(media_entry)
            bot.send_message(message.chat.id, "✅ Media saved. Send more or type ✅ to finish.")
            bot.register_next_step_handler(message, handle_media, media_id, files)
        else:
            bot.send_message(message.chat.id, "❌ Unsupported input. Please send media files only.")
            bot.register_next_step_handler(message, handle_media, media_id, files)

def delete_after(user_id, msg_ids, media_id):
    time.sleep(1800)
    for mid in msg_ids:
        try:
            bot.delete_message(chat_id=user_id, message_id=mid)
        except Exception:
            pass
    try:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📢 Join Backup Channel", url=BACKUP_LINK))
        bot.send_message(chat_id=user_id, text="Join our backup channel 💔", reply_markup=markup)
    except Exception:
        pass
    delete_media(media_id)

if __name__ == "__main__":
    print("Bot is running... Press Ctrl+C to stop.")
    bot.polling()
