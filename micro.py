import speech_recognition as sr
import pyttsx3
import openai 

def fn_speech_recognition():
    sr.Microphone(device_index = 0)
    #print(f"MICs Found on this Computer: \n {sr.Microphone.list_microphone_names()}")
    # Creating a recognition object
    r = sr.Recognizer()
    r.energy_threshold=100
    r.dynamic_energy_threshold = False

    with sr.Microphone() as source:
        print('Please Speak Loud and Clear:')
        #reduce noise
        r.adjust_for_ambient_noise(source)
        #take voice input from the microphone
        audio = r.listen(source)
        print(audio)
        try:
            phrase = r.recognize_google(audio, language="es-US")
            print(f"Did you just say: {phrase} ?")
           
        # speech is unintelligible
        except LookupError:
            print("Could not understand what you've requested.")
        else:
            print("Good")

        return phrase

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 150)    # Establece la velocidad de lectura
    engine.setProperty('voice', voices[1].id)   # Establece la voz en español
    engine.say(text)
    engine.runAndWait()

def enviar_texto(lineas):
    
    openai.api_key = '###'
    
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=lineas
    )
    
    print(completion)
    return completion["choices"][0]["message"]["content"]


messages = [
    {"role": "user", "content": "Tu nuevo nombre es Nova"}
]

while True:
    frase = fn_speech_recognition()
    messages.append({"role": "user", "content": frase})
    res = enviar_texto(messages)
    messages.append({"role": "assistant", "content": res})
    speak(res)