from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Configuration (Replace with your OpenAI API key)
OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'

@app.route('/voice_to_chat', methods=['POST'])
def voice_to_chat():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify(error='No file part'), 400
    
    file = request.files['file']

    # Check if user did not select file
    if file.filename == '':
        return jsonify(error='No selected file'), 400

    # Check if the file is of audio type (simplified check)
    if not (file.filename.endswith('.wav') or file.filename.endswith('.mp3')):
        return jsonify(error='Invalid file type'), 400

    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Note: Update the API endpoint to the correct Whisper API endpoint
    response = requests.post('https://api.openai.com/v1/whisper/voice-to-text', headers=headers, data=file.read())

    if response.status_code != 200:
        return jsonify(error='Failed to transcribe audio'), 500

    return jsonify(text=response.json()['text'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
