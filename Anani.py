
import telebot
import time
import threading
import re

# የቦቱ መረጃዎች - (TOKEN ብቻ ተቀይሯል)
TOKEN = '8743880231:AAHRIeiv-H5sEzhQ9M0BSYKtjwagaGnhPSE'
bot = telebot.TeleBot(TOKEN)

# የአባላትን መረጃ ለመያዝ (Memory storage)
user_data = {}

# መልእክቶችን ከተወሰነ ጊዜ በኋላ ለማጥፋት
def delete_message_later(chat_id, message_id, delay):
    time.sleep(delay)
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        pass

# 1ኛ እና 3ኛ፡ አዲስ ሰው ሲገባ ሰላምታ እና መቁጠር
@bot.message_handler(content_types=['new_chat_members'])
def handle_new_member(message):
    inviter = message.from_user
    inviter_id = inviter.id
    
    # የጋበዘውን ሰው መመዝገብ
    if inviter_id not in user_data:
        user_data[inviter_id] = 0
    
    added_count = len(message.new_chat_members)
    user_data[inviter_id] += added_count
    total_added = user_data[inviter_id]

    for member in message.new_chat_members:
        # 1ኛ፡ የእንኳን ደህና መጡ መልእክት
        welcome_text = f"""
🌟 እንኳን ወደ Tell birr በሰላም መጡ {member.first_name}! 🌟
በዚህ ግሩፕ ውስጥ ሰዎችን Add በማድረግ ብቻ የቤተሰባችን አባል መሆንና የገቢ ምንጭ መፍጠር ይችላሉ! ስራው በጣም ቀላል እና ምንም አይነት ቅድመ ክፍያ የማይጠይቅ ነው! 💸
✨ የክፍያ ተመኖች፦
• 1 ሰው Add ሲያደርጉ ➭ 10 ብር 💵
• 10 ሰው Add ሲያደርጉ ➭ 100 ብር 💵
• 100 ሰው Add ሲያደርጉ ➭ 1,000 ብር 💵
(የፈለጉትን ያህል ሰው በመጋበዝ ገቢዎን ማሳደግ ይችላሉ!)
💳 ክፍያው እንዴት ይፈጸማል?
ይህ ስራ 100% እውነተኛ ሲሆን፣ የተባለውን የሰው ብዛት Add አድርገው እንደጨረሱ ወዲያውኑ በሰከንዶች ውስጥ በፈለጉት አማራጭ፦
✅ በ Telebirr
✅ በ ኢትዮጵያ ንግድ ባንክ (CBE) ክፍያዎን መቀበል ይችላሉ።
🎁 ልዩ ሽልማቶች!
ከክፍያው በተጨማሪ በየሳምንቱ ብዙ ሰው ለሚያስገቡ እና ንቁ ለሆኑ አባላት የካርድ እና የገንዘብ ሽልማቶችን አዘጋጅተናል!
🚀 አሁኑኑ ይጀምሩ!
የግሩፑን ስም በመጫን "Add Members" የሚለውን መርጠው በስልክዎ ያሉ ሰዎችን በመጋበዝ ዛሬውኑ የመጀመሪያ ክፍያዎን ይቀበሉ!
(ማሳሰቢያ፦ ክፍያ ለመቀበል Add አድርገው ሲጨርሱ አድሚኖችን ማነጋገር አይርሱ!) መልካም ገቢ! 💰👇
        """
        msg = bot.reply_to(message, welcome_text)
        # ለ 5 ደቂቃ (300 ሰከንድ) አቆይቶ ማጥፋት
        threading.Thread(target=delete_message_later, args=(message.chat.id, msg.message_id, 300)).start()

    # 3ኛ፡ የጋባዡ መረጃ ለ 4 ደቂቃ (240 ሰከንድ)
    status_text = f"📊 {inviter.first_name} እስካሁን {total_added} ሰው አስገብተዋል።\n💰 በ {total_added} ሰው {total_added * 10} ብር ሰርተዋል!"
    status_msg = bot.send_message(message.chat.id, status_text)
    threading.Thread(target=delete_message_later, args=(message.chat.id, status_msg.message_id, 240)).start()

    # 4ኛ፡ 100 ሰው ሲሞላ የሚላክ ሽልማት
    if total_added >= 100:
        win_text = f"""
እንኳን ደስ አለዎት {inviter.first_name}! የሽልማቱ ባለቤት ሆነዋል! 🎊
ውድ አባል፤ ቃል በገባነው መሰረት 100 ሰዎችን ወደ ግሩፓችን ስላገቡ የ 1,000 ብር አሸናፊ መሆንዎን በደስታ እንገልጻለን! 💸🏆
አሁኑኑ ክፍያዎን ለመቀበል፦
1️⃣ በውስጥ መስመር (Inbox) ያናግሩን
2️⃣ የ ቴሌ ብር (Telebirr) ወይም የ ንግድ ባንክ አካውንትዎን ይላኩልን
ልክ አካውንትዎን እንደላኩ ክፍያውን ወዲያውኑ እንፈጽማለን! 💳✨
ለቀጣዩ ሽልማት ሰዎችን Add ማድረጉን ይቀጥሉ! አሁንም በድጋሚ እንኳን ደስ አለዎት! 🎈🚀
        """
        bot.send_message(message.chat.id, win_text)

# 2ኛ እና 5ኛ፡ መጻፍ መከልከል እና ሊንክ ማጥፋት
@bot.message_handler(func=lambda message: True)
def filter_messages(message):
    user_id = message.from_user.id
    user_adds = user_data.get(user_id, 0)
    
    # 5ኛ፡ ማንኛውንም ሊንክ ማጥፋት
    if re.search(r'(https?://\S+|www\.\S+|t\.me/\S+)', message.text):
        bot.delete_message(message.chat.id, message.message_id)
        return

    # 2ኛ፡ ከ 100 በታች የጋበዘ ሰው መጻፍ አይችልም
    if user_adds < 100:
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
            
        warn_text = f"""
⚠️ ይቅርታ {message.from_user.first_name}! መጻፍ አይችሉም! ⚠️
በዚህ ግሩፕ ላይ መልዕክት ለመጻፍ እና ክፍያዎን ለመጠየቅ መጀመሪያ ግዴታዎን መወጣት አለብዎት።
🛑 መጻፊያው እንዲከፈትላችሁ፦
ቢያንስ 100 ሰዎችን (Add Members) ወደ ግሩፑ መጋበዝ አለባችሁ።
💰 ሽልማቱን ለማግኘት፦
100 ሰው Add ሲያደርጉ የ 1,000 ብር ክፍያ ያገኛሉ፤ እንዲሁም መጻፊያው ይከፈትላችኋል።
🚀 አሁኑኑ መጋበዝ ይጀምሩ!
የግሩፑን ስም ተጭነው "Add Members" የሚለውን በመምረጥ ሰዎችን ያስገቡ።
(ሰዎችን ጨምረው ሲጨርሱ መጻፊያው ይከፈትላችኋል፤ ከዚያም አድሚኖችን ማነጋገር ትችላላችሁ!) 💸🎁
        """
        warn_msg = bot.send_message(message.chat.id, warn_text)
        threading.Thread(target=delete_message_later, args=(message.chat.id, warn_msg.message_id, 300)).start()

# ስሙ ብቻ ተቀይሯል
print("Anani Group Protector ስራ ጀምሯል...")
bot.infinity_polling()
