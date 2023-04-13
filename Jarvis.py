import os  # For working with file paths
import openai  # For using the OpenAI API
import pvporcupine 
import pvleopard  # For wake word detection and speech-to-text
from gtts import gTTS  # For text-to-speech synthesis
from playsound import playsound  # For playing the synthesized audio

# Set up the OpenAI API credentials
openai.api_key = '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'  # Replace with your OpenAI API key

# Configure PicoVoice Porcupine wake word detection
wake_word_path = 'home/pi/Jarvis/hey-jarvis_en_raspberry-pi_v2_2_0.ppn'
porcupine = pvporcupinecreate(
  access_key='/I+3vpA9ZSiKVCE/Fixqo5HiG2oW0lzxEuoNAlpPGTrG/JUGDx5RzA==',
  keywords=['picovoice', 'bumblebee']
)
# Configure PicoVoice Leopard STT
leopard = pvleopard()

# Define the wake word to trigger Leopard STT
wake_word = 'hey assistant'

# Loop for wake word detection and voice input capture
print("Listening for wake word ('{}')...".format(wake_word))
while True:
    keyword_index = porcupine.process()
    if keyword_index >= 0:
        print('Wake word detected! Speak your prompt:')
        prompt = leopard.transcribe()

        # Generate a text message using OpenAI GPT-3.5 API
        response = openai.Completion.create(
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5
        )
        if 'choices' in response and len(response['choices']) > 0:
            message = response['choices'][0]['text']
            print(f'Generated message: {message}')

            # Use gTTS to synthesize speech with Australian English accent and save as audio file
            tts = gTTS(text=message, lang='en-au')
            tts.save('generated_message.mp3')

            # Play the synthesized audio using playsound library
            playsound('generated_message.mp3')

            # Remove the temporary audio file
            os.remove('generated_message.mp3')
        else:
            print('Failed to generate message using OpenAI GPT-3.5 API.')
        print("Listening for wake word ('{}')...".format(wake_word))
