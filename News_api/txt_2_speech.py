import os
import datetime
import wave
import azure.cognitiveservices.speech as speechsdk
import json
from . import create_con_text
import uuid

class TextToSpeech:
    def __init__(self, subscription_key, region):
        self.speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
        self.speech_config.speech_synthesis_output_format = speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3

    def _create_synthesizer(self, voice_name, output_file):
        self.speech_config.speech_synthesis_voice_name = voice_name
        audio_output = speechsdk.audio.AudioOutputConfig(filename=output_file)
        return speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=audio_output)

    def synthesize_speech(self, voice_name, text, output_file):
        # Create a synthesizer with the specified voice and output file
        synthesizer = self._create_synthesizer(voice_name, output_file)
        
        # Synthesize the text to the MP3 file
        result = synthesizer.speak_text_async(text).get()
        
        # Check result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"Speech synthesis succeeded for {output_file}")
            return output_file
        else:
            print(f"Speech synthesis failed for {output_file}")
            return None

    def process_conversation(self, input_file, output_folder):
        os.makedirs(output_folder, exist_ok=True)
        unique_id = str(uuid.uuid4())
        output_dir = os.path.join(output_folder, unique_id)
        os.makedirs(output_dir, exist_ok=True)

        with open(input_file, 'r') as f:
            conversation_data = json.load(f)

        audio_files = []
        for i, turn in enumerate(conversation_data['conversation']):
            if turn['speaker'] == 'Andrew Krepthy':
                output_file = os.path.join(output_dir, f'andrew_part_{i}.mp3')
                result = self.synthesize_speech("en-US-AndrewMultilingualNeural", turn['text'], output_file)
            elif turn['speaker'] == 'Smithi':
                output_file = os.path.join(output_dir, f'smithi_part_{i}.mp3')
                result = self.synthesize_speech("en-US-AvaMultilingualNeural", turn['text'], output_file)
            
            if result:
                audio_files.append(result)

        merged_audio = self.merge_audio_files_wave(audio_files, output_dir)
        self.cleanup_files(audio_files + [os.path.join(output_dir, 'input.txt')])
        
        return merged_audio

    def merge_audio_files_wave(self, audio_files, output_dir):
        # Sort the files based on the numeric value in their names
        sorted_files = sorted(audio_files, key=lambda x: int(x.split("_")[-1].split(".")[0]))

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Define output file path
        output_file_path = os.path.join(output_dir, 'output.wav')

        # Open the first file to get the parameters
        with wave.open(sorted_files[0], 'rb') as wf:
            params = wf.getparams()
            combined_frames = wf.readframes(wf.getnframes())

        # Append the rest of the files
        for file_path in sorted_files[1:]:
            with wave.open(file_path, 'rb') as wf:
                combined_frames += wf.readframes(wf.getnframes())

        # Write the combined frames to the output file
        with wave.open(output_file_path, 'wb') as wf:
            wf.setparams(params)
            wf.writeframes(combined_frames)

        print(f"Audio files have been merged into '{output_file_path}'")
        return output_file_path
    def cleanup_files(self, files_to_remove):
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)

def text_to_speech(urls, output_folder= "summarized/audio"):
    os.makedirs("summarized/audio" , exist_ok=True)
    os.makedirs("summarized/text" , exist_ok=True)
    if not os.path.exists(output_folder + "/history.json"):
        with open(output_folder + "/history.json", "w") as file:
            json.dump({"history": []}, file)
    with open(output_folder + "/history.json", "r") as file:
        history = json.load(file)
    for i in history["history"]:
        if i["urls"] == urls:
            return i["path"]

    subscription_key = "2324b94511cc4c079974e40a0285f3d5"
    region = "centralindia"
    input_file = f"summarized/text/{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M')}.json"
    create_con_text.get_context(urls ,input_file)
    tts = TextToSpeech(subscription_key, region)

    out = tts.process_conversation(input_file, output_folder)

    history["history"].append({"urls": urls , "path": out})
    with open(output_folder+"/history.json" , "w") as file:
        json.dump(history , file , indent=4)
    return out