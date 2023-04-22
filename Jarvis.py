import os  
import openai  
import pvporcupine 
import speech_recognition as sr
import struct
import pyaudio
import pvporcupine
import time
import pvcobra
import wave
from pydub import AudioSegment
from pydub.playback import play
from gtts import gTTS  
from playsound import playsound 


import sys
import psutil
import logging



import subprocess

def copy2clip(txt):
    cmd='echo '+txt.strip()+'|clip'
    return subprocess.check_call(cmd, shell=True)

def restart_program():
   
    

    python = sys.executable
    os.execl(python, python, *sys.argv)






cobra = pvcobra.create(access_key='/I+3vpA9ZSiKVCE/Fixqo5HiG2oW0lzxEuoNAlpPGTrG/JUGDx5RzA==')

openai.api_key = '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'  
voice_file = "voice.wav"
filename = voice_file
chunk = 1024
FORMAT = pyaudio.paInt16
channels = 1
sample_rate = 44100
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=channels,
                rate=sample_rate,
                input=True,
                output=True,
                frames_per_buffer=chunk)
frames = []

wake_word_path = 'C:/Users/tata_/Downloads/Jarvis-main/Jarvis-main/hey-jarvis_en_raspberry-pi_v2_2_0.ppn'
porcupine = pvporcupine.create(
  access_key='/I+3vpA9ZSiKVCE/Fixqo5HiG2oW0lzxEuoNAlpPGTrG/JUGDx5RzA==',keyword_paths=['Hey-Friday_en_windows_v2_2_0.ppn'],
  keywords=['Hey Jarvis']
)

r = sr.Recognizer()



wake_word = 'hey assistant'
pa = pyaudio.PyAudio()
audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length)

print("Listening for wake word ('{}')...".format(wake_word))

while True:
    pcm = audio_stream.read(porcupine.frame_length)
    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
    
    keyword_index = porcupine.process(pcm)
    if keyword_index >= 0:
        stream.start_stream()
       
        
        
        
        
        prompt = None


        start_time = time.time()

        while True:
            pcm = audio_stream.read(cobra.frame_length)
            pcm = struct.unpack_from("h"*cobra.frame_length,pcm)
            voice_probability = cobra.process(pcm)

            data = stream.read(chunk)
            frames.append(data)

            if voice_probability <= 0.5:
                elapsed_time = time.time() - start_time
                if elapsed_time >= 2.0:
                    stream.stop_stream()
                   
                    
                    wf = wave.open(filename, "wb")
                    wf.setnchannels(channels)
                    wf.setsampwidth(p.get_sample_size(FORMAT))
                    wf.setframerate(sample_rate)
                    wf.writeframes(b"".join(frames))
                    
                    transcript = ' '

                    with sr.AudioFile(filename) as source:
                        text = None
                        try:  
                            text = r.recognize_google(r.record(source),None,"en-US",0,False)
                        except TypeError as e:
                            transcript = ' say "sorry i didnt get that"'
                        transcript = text
                        print(transcript)
                        
                       
                        
                    
                        
                        if not isinstance(transcript, str):
                            transcript = ' say "sorry i didnt get that"'
                    wf.close()
                   
                    os.remove('voice.wav')
                    prompt = 'your name will be Friday and your job is an AI Voice Assistant, here is your text, ' + transcript 

                    
                    break

            else:
                start_time = time.time()




        
       
        response = openai.Completion.create(
            model="text-davinci-003",prompt=prompt, temperature = 0,n=1)
        if 'choices' in response and len(response['choices']) > 0:
            message = response['choices'][0]['text']
            copy2clip(message)

            #
            tts = gTTS(text=message, lang='en', tld='co.za')
            tts.save('generated_message.mp3')

          
            audio_file = AudioSegment.from_file('generated_message.mp3',format='mp3')
            
            play(audio_file)
            restart_program()

          
        else:
            print('Failed to generate message using OpenAI GPT-3.5 API.')
        print("Listening for wake word ('{}')...".format(wake_word))