import os
import datetime
import json
from . import create_con_text
import uuid
from google.cloud import texttospeech
import base64
import io
from concurrent.futures import ThreadPoolExecutor

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/gen-ai-448511-bce054155d75.json"

class TextToSpeech:
    def __init__(self, subscription_key, region):
        pass

    def synthesize_speech(self, voice_name, text, output_file):
        client = texttospeech.TextToSpeechClient()
        input_text = texttospeech.SynthesisInput(text=text)
        # Set language_code based on voice_name to match the expected voice
        language_code = "es-us" if voice_name == "es-US-Chirp-HD-D" else "en-US"
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name,
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
        )
        response = client.synthesize_speech(
            request={"input": input_text, "voice": voice, "audio_config": audio_config}
        )
        b_64 = base64.b64encode(response.audio_content).decode("utf-8")
        print(f"Speech synthesis succeeded with Google TTS.")
        return b_64

    def process_conversation(self, input_file, output_folder):
        os.makedirs(output_folder, exist_ok=True)
        unique_id = str(uuid.uuid4())
        output_dir = os.path.join(output_folder, unique_id)
        os.makedirs(output_dir, exist_ok=True)

        with open(input_file, 'r') as f:
            conversation_data = json.load(f)

        # Process synthesis concurrently using threads
        with ThreadPoolExecutor() as executor:
            futures = []
            for i, turn in enumerate(conversation_data['conversation']):
                if turn['speaker'] == 'Andrew Krepthy':
                    # Use boy voice: es-US-Chirp-HD-D
                    futures.append(executor.submit(self.synthesize_speech, "es-US-Chirp-HD-D", turn['text'], None))
                elif turn['speaker'] == 'Smithi':
                    # Use girl voice: Aoede
                    futures.append(executor.submit(self.synthesize_speech, "Aoede", turn['text'], None))
                else:
                    continue
            results = [future.result() for future in futures if future.result()]

        # Merge audio segments: decode base64 and combine into a BytesIO stream
        audio_bytes = [base64.b64decode(segment) for segment in results]
        merged_bytes = b''.join(audio_bytes)
        audio_stream = io.BytesIO(merged_bytes)
        audio_stream.seek(0)  # Ensure stream is ready to be read

        print(f"Processed conversation with {len(results)} segments.")
        return audio_stream

    def merge_audio_files_wave(self, audio_files, output_dir):
        pass

    def cleanup_files(self, files_to_remove):
        pass

def text_to_speech(urls, output_folder="summarized/audio"):
    # Convert urls to a list of integers if necessary
    if isinstance(urls, str):
        urls = [int(item.strip()) for item in urls.split(",") if item.strip()]
        
    # Removed history caching for audio stream to always generate fresh output
    os.makedirs("summarized/audio", exist_ok=True)
    os.makedirs("summarized/text", exist_ok=True)
    subscription_key = "2324b94511cc4c079974e40a0285f3d5"
    region = "centralindia"
    input_file = f"summarized/text/{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')}.json"
    create_con_text.get_context(urls, input_file)
    tts = TextToSpeech(subscription_key, region)
    out = tts.process_conversation(input_file, output_folder)
    return out