import telebot
import random
import json
import os

TOKEN = '7261395606:AAEiLQG9us3AGew00gFteV2MpcGwe9WDvXQ'
bot = telebot.TeleBot(TOKEN)

DATA_FILE = 'kullanici_verileri.json'

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

def verileri_yukle():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def verileri_kaydet(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

film_listesi = [
    "🎬 Inception", "🎥 La La Land", "🎞 Whiplash", "🧠 The Imitation Game"
]

muzikler = {
    "lofi": ["Lo-fi Beats", "Rainy Jazzhop", "Coffee Time"],
    "pop": ["Dua Lipa - Levitating", "Harry Styles - As It Was"],
    "rock": ["Nirvana - Smells Like Teen Spirit", "Muse - Supermassive Black Hole"]
}

def kullanici_kontrol_et(user_id):
    data = verileri_yukle()
    if str(user_id) not in data:
        data[str(user_id)] = {"dersler": [], "notlar": []}
        verileri_kaydet(data)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    kullanici_kontrol_et(message.from_user.id)
    bot.send_message(message.chat.id, "🎉 Hoş geldin Süper Mini GPT'ye!\n\nKomutlar:\n"
                                      "/film – Film öner\n"
                                      "/muzik – Müzik öner\n"
                                      "/muzik_tur – Müzik kategorisi seç\n"
                                      "/ders_ekle – Ders takvimine ders ekle\n"
                                      "/derslerim – Derslerini göster\n"
                                      "/notekle – Not ekle\n"
                                      "/notlarim – Notları göster\n")

@bot.message_handler(commands=['film'])
def film_oner(message):
    bot.send_message(message.chat.id, f"📽 Bugünlük önerim: {random.choice(film_listesi)}")

@bot.message_handler(commands=['muzik_tur'])
def muzik_tur_sec(message):
    bot.send_message(message.chat.id, "🎧 Bir müzik türü yaz (lofi / pop / rock):")
    bot.register_next_step_handler(message, muzik_gonder)

def muzik_gonder(message):
    tur = message.text.lower()
    if tur in muzikler:
        bot.send_message(message.chat.id, f"🎶 Önerim: {random.choice(muzikler[tur])}")
    else:
        bot.send_message(message.chat.id, "❌ Tür bulunamadı. Lütfen /muzik_tur komutuyla tekrar dene.")

@bot.message_handler(commands=['ders_ekle'])
def ders_ekle(message):
    bot.send_message(message.chat.id, "📚 Eklemek istediğin dersi yaz:")
    bot.register_next_step_handler(message, dersi_kaydet)

def dersi_kaydet(message):
    user_id = str(message.from_user.id)
    ders = message.text
    data = verileri_yukle()
    data[user_id]["dersler"].append(ders)
    verileri_kaydet(data)
    bot.send_message(message.chat.id, f"✅ '{ders}' dersi kaydedildi!")

@bot.message_handler(commands=['derslerim'])
def dersleri_goster(message):
    user_id = str(message.from_user.id)
    data = verileri_yukle()
    dersler = data[user_id]["dersler"]
    if dersler:
        bot.send_message(message.chat.id, "📚 Derslerin:\n" + "\n".join(f"- {d}" for d in dersler))
    else:
        bot.send_message(message.chat.id, "Henüz ders eklemedin. /ders_ekle komutunu dene.")

@bot.message_handler(commands=['notekle'])
def not_ekle(message):
    bot.send_message(message.chat.id, "📝 Eklemek istediğin notu yaz:")
    bot.register_next_step_handler(message, not_kaydet)

def not_kaydet(message):
    user_id = str(message.from_user.id)
    not_metni = message.text
    data = verileri_yukle()
    data[user_id]["notlar"].append(not_metni)
    verileri_kaydet(data)
    bot.send_message(message.chat.id, "✅ Not kaydedildi!")

@bot.message_handler(commands=['notlarim'])
def notlari_goster(message):
    user_id = str(message.from_user.id)
    data = verileri_yukle()
    notlar = data[user_id]["notlar"]
    if notlar:
        bot.send_message(message.chat.id, "🗒️ Notların:\n" + "\n".join(f"- {n}" for n in notlar))
    else:
        bot.send_message(message.chat.id, "Henüz not eklemedin.")

@bot.message_handler(func=lambda message: True)
def genel_cevap(message):
    bot.send_message(message.chat.id, "🤖 Komutları görmek için /start yazabilirsin!")

bot.polling(none_stop=True)
