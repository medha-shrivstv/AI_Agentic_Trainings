import gradio as gr
from agent import agent
import requests
from speech import text_to_audio
 
def audio_to_text(audio_path, api_key, input_language="unknown"):
    if not audio_path:
        raise ValueError("Record or upload an audio prompt.")
    if not api_key:
        raise ValueError("Enter the Sarvam API key.")
 
    with open(audio_path, "rb") as audio_file:
        response = requests.post(
            "https://api.sarvam.ai/speech-to-text",
            headers={"api-subscription-key": api_key},
            files={"file": audio_file},
            data={
                "model": "saaras:v4",
                "language_code": input_language
            },
            timeout=60
        )
    response.raise_for_status()
    return response.json()["transcript"]
 
def gradio_reply(message, chat_history, make_audio, language, api_key):
    if not message.strip():
        return "", chat_history, None, "Please enter a message."
 
    answer = agent(message)
    chat_history = (chat_history or []) + [
        {"role": "user", "content": message},
        {"role": "assistant", "content": answer}
    ]
 
    audio_path, status = None, "Text response generated."
    if make_audio:
        if not api_key:
            status = "Enter the Sarvam API key to generate audio."
        else:
            try:
                audio_path = text_to_audio(answer, api_key, language)
                status = "Text and audio generated."
            except Exception as error:
                status = f"Audio error: {error}"
 
    return "", chat_history, audio_path, status
 
def gradio_voice_reply(
    audio_prompt, chat_history, make_audio,
    output_language, input_language, api_key
):
    try:
        transcript = audio_to_text(audio_prompt, api_key, input_language)
        _, history, audio_path, status = gradio_reply(
            transcript, chat_history, make_audio, output_language, api_key
        )
        return "", history, audio_path, f"Transcript: {transcript}  \n{status}", None
    except Exception as error:
        return "", chat_history, None, f"Voice input error: {error}", audio_prompt
 
with gr.Blocks(title="Qwen Agent") as demo:
    gr.Markdown("# Qwen Voice Agent with Live Weather and Sarvam Speech")
    chatbot = gr.Chatbot(height=400)
 
    with gr.Row():
        message = gr.Textbox(
            label="Ask a question",
            placeholder="Try: What is the weather in Bhopal?"
        )
        send = gr.Button("Send", variant="primary")
 
    audio_prompt = gr.Audio(
        sources=["microphone", "upload"],
        type="filepath",
        label="Speak or upload your prompt"
    )
    voice_send = gr.Button("Send voice prompt")
 
    with gr.Row():
        language = gr.Dropdown(
            choices=["en-IN", "hi-IN"],
            value="en-IN",
            label="Speech language"
        )
        make_audio = gr.Checkbox(label="Generate Sarvam audio")
        api_key = gr.Textbox(label="Sarvam API key", type="password")
        input_language = gr.Dropdown(
            choices=["unknown", "en-IN", "hi-IN"],
            value="unknown",
            label="Spoken input language"
        )
 
    audio = gr.Audio(label="Agent audio", type="filepath")
    status = gr.Markdown()
    clear = gr.Button("Clear chat")
 
    send.click(
        gradio_reply,
        inputs=[message, chatbot, make_audio, language, api_key],
        outputs=[message, chatbot, audio, status]
    )
    message.submit(
        gradio_reply,
        inputs=[message, chatbot, make_audio, language, api_key],
        outputs=[message, chatbot, audio, status]
    )
    voice_send.click(
        gradio_voice_reply,
        inputs=[
            audio_prompt, chatbot, make_audio,
            language, input_language, api_key
        ],
        outputs=[message, chatbot, audio, status, audio_prompt]
    )
    clear.click(
        lambda: ([], None, "", None),
        outputs=[chatbot, audio, status, audio_prompt]
    )
 
demo.launch(share=True, debug=True)