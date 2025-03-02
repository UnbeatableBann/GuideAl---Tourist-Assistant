from flask import Flask, render_template, request, jsonify, redirect, session
from google.cloud import translate_v2 as translate
from livelocation import chatbot
from trip_planning import generate_trip_plan
from image import get_all_img
import os
import langid
import io
from ibm_watson import AssistantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import base64
from ibm_watson import TextToSpeechV1
import requests
from dotenv import load_dotenv
from flask_session import Session

app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "guideai-447815-5e60d5271224.json"
translate_client = translate.Client()

load_dotenv()

#session management
app.secret_key = os.getenv("SECRET_KEY")

# IBM App ID credentials from environment variables
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
OAUTH_SERVER_URL = os.getenv("OAUTH_SERVER_URL")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# IBM Watson Text-to-Speech setup
tts_API_KEY = 'P7Dn9UBTTAfN8PP0VqFSZHzFYqIoyd_ogdaGjPUXXh_W'
SERVICE_URL_TEXT_TO_SPEECH = 'https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/d6fc4858-565f-4c83-bc8d-05fc279d2ac9'
authenticator_text_to_speech = IAMAuthenticator(tts_API_KEY)
text_to_speech = TextToSpeechV1(authenticator=authenticator_text_to_speech)
text_to_speech.set_service_url(SERVICE_URL_TEXT_TO_SPEECH)

# Configure server-side session storage
app.config['SESSION_TYPE'] = 'filesystem'  # Use filesystem-based session storage
app.config['SESSION_PERMANENT'] = False  # Session expires when the browser closes
app.config['SESSION_FILE_DIR'] = './.flask_session/'  # Directory to store session files
Session(app)  # Initialize session with Flask-Session

@app.route('/')
def login():
    """Redirect users to the IBM App ID login page."""
    auth_url = f"{OAUTH_SERVER_URL}/authorization" \
        f"?client_id={CLIENT_ID}" \
        f"&response_type=code" \
        f"&redirect_uri={REDIRECT_URI}" \
        f"&scope=openid email profile"

    return redirect(auth_url)


@app.route('/callback')
def callback():
    """Handle the callback and exchange the code for an access token."""
    code = request.args.get('code')
    if not code:
        return "Error: Authorization code not provided.", 400

    # Exchange authorization code for access token
    token_url = f"{OAUTH_SERVER_URL}/token"
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "redirect_uri": REDIRECT_URI,
        "code": code
    }

    try:
        response = requests.post(token_url, data=payload)
        response.raise_for_status()
        token_data = response.json()
        access_token = token_data.get('access_token')
        id_token = token_data.get('id_token')
        
        if access_token:
            user_info = get_user_info(access_token)   # this function not required but can be used in future
            session['access_token'] = access_token  # Store token in session
            session['id_token'] = id_token  # Store ID token
            return redirect('/home')

        return "Error: Failed to retrieve access token.", 400

    except requests.exceptions.RequestException as e:
        return f"Error during token exchange: {e}", 500


def get_user_info(access_token):
    """Fetch user profile using the access token."""
    userinfo_url = f"{OAUTH_SERVER_URL}/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(userinfo_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to fetch user info"}

# Define a mapping of language codes to IBM TTS voices
LANGUAGE_TO_VOICE = {
    'en': 'en-US_AllisonV3Voice',  # English
    'hi': 'hi-IN_MaleVoice',       # Hindi
    'de': 'de-DE_BirgitV3Voice',   # German
    'fr': 'fr-FR_ReneeV3Voice',    # French
    'es': 'es-ES_EnriqueV3Voice',  # Spanish
    'ja': 'ja-JP_EmiV3Voice',      # Japanese
    'it': 'it-IT_FrancescaV3Voice' # Italian
}

def ibm_text_to_speech(text, detected_lang):
    
    # Get the appropriate voice for the detected language
    voice = LANGUAGE_TO_VOICE.get(detected_lang, 'en-US_AllisonV3Voice')  # Default to English
    print(voice)
    """Generate audio from text and return it as a base64 string."""
    response = text_to_speech.synthesize(
        text,
        voice=voice,
        accept='audio/wav'
    ).get_result()
    
    audio_data = io.BytesIO(response.content)
    base64_audio = base64.b64encode(audio_data.getvalue()).decode('utf-8')
    return base64_audio

@app.route('/home')
def home():
    if 'access_token' not in session:
        return redirect('/')

    # Initialize query and result lists in session if they don't exist
    if 'query' not in session:
        session['query'] = []
    if 'result' not in session:
        session['result'] = []

    # Combine queries and results
    query_result_pairs = zip(session['query'], session['result'])

    return render_template('index.html', query_result_pairs=query_result_pairs)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route("/get", methods=["POST"])
def translate_and_chat():
    user_msg = request.form.get("msg")

    if not user_msg:
        return "Error: No input received", 400

    detection_result = translate_client.detect_language(user_msg)
    detected_lang = detection_result['language']

    if not detected_lang or detected_lang.strip() == "" or detected_lang=="und":
        detected_lang = "en"  # Default to English if not provided

    if detected_lang != "en":
        translated_input = translate_client.translate(
            user_msg, target_language="en")['translatedText']
    else:
        translated_input = user_msg

    bot_response_in_english = chatbot(translated_input)
    print(translated_input)

    if detected_lang != "en":
        translated_response = translate_client.translate(
            bot_response_in_english, target_language=detected_lang)['translatedText']
    else:
        translated_response = bot_response_in_english


    session['query'].append(translated_input)
    session['result'].append(translated_response)

    return  translated_response


@app.route("/plan")
def plan():
    return render_template('plantour.html')


@app.route("/plantour", methods=["GET", "POST"])
def plantour():
    if request.method == "POST":
        destination = request.form.get("destination")
        origin = request.form.get("origin")
        departure_date = request.form.get("departure_date")
        suggestions = request.form.get("suggestions")
        response = generate_trip_plan(
            destination, origin, departure_date, suggestions)
        return response


@app.route("/image")
def image():
    return render_template('image.html')


@app.route("/imageupload", methods=["POST"])
def imageupload():
    uploaded_file = request.files.get("image")
    if not uploaded_file:
        return jsonify({"error": "No file uploaded"}), 400

    image_bytes = uploaded_file.read()
    if not image_bytes:
        return jsonify({"error": "File is empty"}), 400

    get_info = get_all_img(image_bytes)
    if get_info is None:
        return jsonify({"error": "Image processing failed"}), 500

    return str(get_info)


if __name__ == '__main__':
    app.run(debug=True)
