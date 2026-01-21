import warnings
warnings.filterwarnings("ignore")

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import mysql.connector
from mysql.connector import pooling
from langdetect import detect, DetectorFactory
from deep_translator import GoogleTranslator

# Seed fix karne se detection thoda stable hota hai
DetectorFactory.seed = 0

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# --- DATABASE SETUP ---
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "@12345",
    "database": "college_event"
}

try:
    connection_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **db_config)
    print("✅ Database Connected")
except Exception as e:
    print(f"❌ Database Error: {e}")
    connection_pool = None

def get_smart_response(user_msg, selected_lang):
    try:
        # STEP 1: Determine Language (User Choice vs Auto Detect)
        if selected_lang and selected_lang != "auto":
            # Agar user ne dropdown se select kiya hai, wahi maano
            user_lang = selected_lang
            print(f"🔒 User Selected Language: {user_lang}")
        else:
            # Agar 'Auto' hai, tab detect karo
            try:
                user_lang = detect(user_msg)
                print(f"🕵️ Detected Language: {user_lang}")
            except:
                user_lang = 'en'

        # STEP 2: Translate to English for Database Search
        # Agar user English nahi bol raha, tabhi translate karo
        if user_lang != 'en':
            try:
                translator = GoogleTranslator(source='auto', target='en')
                translated_text = translator.translate(user_msg)
            except:
                translated_text = user_msg # Fallback
        else:
            translated_text = user_msg

        print(f"🔍 Searching DB for: {translated_text}")

        # STEP 3: Database Search
        db_reply = "NO_MATCH"
        if connection_pool:
            conn = connection_pool.get_connection()
            cur = conn.cursor()
            
            # Smart Search: Check agar keyword sentence mein hai
            query = "SELECT response FROM admin_knowledge WHERE %s LIKE CONCAT('%%', trigger_word, '%%') LIMIT 1"
            cur.execute(query, (translated_text.lower(),))
            row = cur.fetchone()
            cur.close()
            conn.close()
            
            if row:
                db_reply = row[0]

        # STEP 4: Fallback Message
        if db_reply == "NO_MATCH":
            # Default message bhi English mein rakhein
            db_reply = "I'm sorry, I don't have information about that right now. Can you ask about anxiety, depression, or fees?"

        # STEP 5: Final Translation to User's Language
        if user_lang != 'en':
            try:
                final_reply = GoogleTranslator(source='en', target=user_lang).translate(db_reply)
            except Exception as e:
                print(f"Translation Error: {e}")
                final_reply = db_reply # Error aaye to English hi bhejo
        else:
            final_reply = db_reply
            
        return final_reply

    except Exception as e:
        print(f"❌ Processing Error: {e}")
        return "System Error. Please try again."

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    # Frontend se aa rahi language ko capture karein
    selected_lang = data.get("language", "auto") 

    if not user_msg:
        return jsonify({"reply": "..."})

    print(f"\n📩 User ({selected_lang}): {user_msg}")
    
    bot_reply = get_smart_response(user_msg, selected_lang)
    
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True, port=5000)