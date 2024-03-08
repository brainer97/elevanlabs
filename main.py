# app.py

from flask import Flask, render_template, request
import elevenlabs

app = Flask(__name__, template_folder='templates', static_folder='static')

# Set your API key securely
ELEVENLABS_API_KEY = "33b05fc0cf62eb2d5f0783bf50a12add"
elevenlabs.set_api_key(ELEVENLABS_API_KEY)

# Define a list of voice IDs and their corresponding names
voice_ids = [
    {"id": "oWAxZDx7w5VEj9dCyTzz", "name": "Grace"},
    {"id": "pNInz6obpgDQGcFmaJgB", "name": "Adam"},
    # Add more voice IDs as needed
]

@app.route('/', methods=['GET', 'POST'])
def ttsindex():
    if request.method == 'POST':
        # Get the text input and selected voice ID from the form
        user_text = request.form['user_text']
        selected_voice_id = request.form['voice_id']

        # Find the selected voice settings based on the voice ID
        selected_voice_settings = next((v for v in voice_ids if v['id'] == selected_voice_id), None)

        if selected_voice_settings:
            try:
                # Create a Voice object with the selected settings
                voice = elevenlabs.Voice(
                    voice_id=selected_voice_settings['id'],
                    settings=elevenlabs.VoiceSettings(
                        stability=selected_voice_settings.get('stability', 0),
                        similarity_boost=selected_voice_settings.get('similarity_boost', 0.75)
                    )
                )

                # Generate audio from user input text using the selected voice
                audio = elevenlabs.generate(
                    text=user_text,
                    voice=selected_voice_settings['name']
                )

                # Save the audio to a file in the 'static' folder
                elevenlabs.save(audio, "static/audio.mp3")

                # Render a template or return a response
                return render_template('index.html', user_text=user_text, voice_ids=voice_ids, selected_voice_id=selected_voice_id)

            except Exception as e:
                # Handle API request errors
                return render_template('error.html', error_message=str(e))

    # Render the initial form on GET request
    return render_template('index.html', user_text=None, voice_ids=voice_ids, selected_voice_id=voice_ids[0]['id'])

if __name__ == '__main__':
    app.run(debug=True)

