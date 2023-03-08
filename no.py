import speech_recognition as sr
import pyttsx3
import openai 

def fn_speech_recognition():
    sr.Microphone(device_index = 0)
    r = sr.Recognizer()
    mic = sr.Microphone()
    r.energy_threshold=1
    r.dynamic_energy_threshold = False

    with mic as source:
        print('Puedes hablar:')
        #reduce noise
        r.adjust_for_ambient_noise(source)
        #take voice input from the microphone
        try:
            audio = r.listen(source)
            phrase = r.recognize_google(audio, language="es-US")
            print(f"Dijiste: {phrase}")
           
        except sr.WaitTimeoutError:
            print("No se detectó entrada de audio en los últimos 5 segundos.")
            phrase = False
            pass
        
        except sr.UnknownValueError:
            print("No se pudo entender lo que dijiste")
            phrase = False
            pass
        
        except sr.RequestError as e:
            print("No se pudo conectar con el servicio de reconocimiento de voz; {0}".format(e))
            phrase = False
            pass
        
        else:
            print("Entendido")

        return phrase

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate', 150)    # Establece la velocidad de lectura
    engine.setProperty('voice', voices[1].id)   # Establece la voz en español
    engine.say(text)
    engine.runAndWait()

def enviar_texto(lineas):
    
    customError = "No estoy disponible para responder en este momento"
    
    try:
        openai.api_key = 'XXX'

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=lineas
        )
        
        response = completion["choices"][0]["message"]["content"]
        
    except openai.error.APIError as e:
        response = customError
        pass

    except openai.error.APIConnectionError as e:
        response = customError
        pass
    
    except openai.error.AuthenticationError as e:
        response = customError
        pass

    except openai.error.RateLimitError as e:
        response = customError
        pass
    
    except openai.error.OpenAIError as e:
        response = customError
        pass
    
    return response


messages = [
    {"role": "user", "content": "Hola"}
]

while True:
    frase = fn_speech_recognition()
    if frase: 
        messages.append({"role": "user", "content": frase})
        res = enviar_texto(messages)
        messages.append({"role": "assistant", "content": res})
        speak(res)