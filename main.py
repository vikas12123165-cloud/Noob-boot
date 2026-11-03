import telebot
import requests

# Bot Info:
# Name: FF Profile Bot
# Username: @my_ff_profile_bot
TOKEN = '9270528412:AAE9yLQR94DLlwHuhyWHjUkOiLehQLhL93Q'
bot = telebot.TeleBot(TOKEN)

# Free Fire Profile fetch karne ka function
def get_ff_profile(uid):
    try:
        url = f"https://api.freefireinfo.in/profile?uid={uid}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data and 'accountInfo' in data:
                acc = data['accountInfo']
                name = acc.get('nickname', 'N/A')
                level = acc.get('level', 'N/A')
                likes = acc.get('likes', 'N/A')
                region = acc.get('region', 'N/A')
                exp = acc.get('exp', 'N/A')
                
                result = (
                    f"🎮 **Free Fire Profile Found!** 🎮\n\n"
                    f"👤 **Name:** {name}\n"
                    f"🆔 **UID:** {uid}\n"
                    f"📊 **Level:** {level}\n"
                    f"❤️ **Likes:** {likes}\n"
                    f"🌍 **Region:** {region}\n"
                    f"✨ **EXP:** {exp}"
                )
                return result
            else:
                return "❌ Player nahi mila! Sahi UID dalein."
        else:
            return "❌ API server se connect nahi ho paya. Kuch der baad try karein."
    except Exception as e:
        return f"⚠️ Error aa gaya: {str(e)}"

# Start Command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! 👋 Mujhe kisi bhi Free Fire player ka **UID** bhejein, main uski profile details nikal kar bhej dunga.")

# Jab user koi UID (number) bhejega
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    uid = message.text.strip()
    
    if uid.isdigit():
        bot.reply_to(message, "🔍 Profile search ki ja rahi hai, thoda intezaar karein...")
        profile_info = get_ff_profile(uid)
        bot.send_message(message.chat.id, profile_info, parse_mode="Markdown")
    else:
        bot.reply_to(message, "⚠️ Kripya sirf valid numeric **UID** bhejein!")

# Bot ko start karne ke liye
print("Bot is running...")
bot.infinity_polling()
