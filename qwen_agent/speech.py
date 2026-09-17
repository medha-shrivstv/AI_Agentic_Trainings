import base64
import requests
 
SARVAM_API_KEY = "sk_7z6zmak0_daBLXZjVrmMJkECZ62RqAegp"  # Optional for the notebook test; Gradio has a password field.
 
def text_to_audio(text, api_key, language="en-IN", filename="agent_audio.wav"):
    response = requests.post(
        "https://api.sarvam.ai/text-to-speech",
        headers={
            "api-subscription-key": api_key,
            "Content-Type": "application/json"
        },
        json={
            "text": str(text)[:2500],
            "language_code": language,
            "speaker": "shubh",
            "model": "bulbul:v3",
            "pace": 1.0,
            "output_audio_codec": "wav"
        },
        timeout=60
    )
    response.raise_for_status()
 
    audio_bytes = base64.b64decode(response.json()["audios"][0])
    with open(filename, "wb") as audio_file:
        audio_file.write(audio_bytes)
    return filename