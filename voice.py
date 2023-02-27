import openai
import pyttsx3
import pyaudio
import wave
import os
import whisper
from pydub import AudioSegment
from pydub.playback import play

def grabar_audio(nombre_archivo, duracion_segundos):
    
    # Carga audios de inicio y fin de grabación
    audio_start = AudioSegment.from_wav("start.wav")
    audio_end = AudioSegment.from_wav("end.wav")
    
    # Eliminar el archivo grabacion.wav
    if os.path.exists("grabacion.wav"):
        os.remove("grabacion.wav")
    
    # Obtener información del dispositivo de entrada predeterminado
    pa = pyaudio.PyAudio()
    input_info = pa.get_default_input_device_info()
    input_channels = input_info['maxInputChannels']
    input_rate = int(input_info['defaultSampleRate'])
    input_format = pyaudio.paInt16

    # Tamaño del buffer
    chunk = 4096

    # Abrir el stream de entrada
    stream = pa.open(format=input_format,   # Formato de audio de entrada
                     channels=input_channels,  # Número de canales de audio de entrada
                     rate=input_rate,  # Tasa de muestreo de audio de entrada
                     input=True,  # Indica que se utilizará el dispositivo de entrada
                     frames_per_buffer=chunk)  # Tamaño del buffer de entrada

    # Duración de la grabación
    frames = []
    
    # Reproduce el audio de inicio
    play(audio_start)
    
    for i in range(0, int(input_rate / chunk * duracion_segundos)):
        data = stream.read(chunk)  # Leer los datos de audio del stream
        frames.append(data)

    # Reproduce el audio de fin
    play(audio_end)
    
    # Detener la captura de audio
    stream.stop_stream()
    stream.close()
    pa.terminate()

    # Escribir los datos de audio en un archivo WAV
    wf = wave.open(nombre_archivo, 'wb')  # Crear un nuevo archivo WAV
    wf.setnchannels(input_channels)  # Establecer el número de canales de audio
    wf.setsampwidth(pa.get_sample_size(input_format))  # Establecer el tamaño de muestra de audio
    wf.setframerate(input_rate)  # Establecer la tasa de muestreo de audio
    wf.writeframes(b''.join(frames))  # Escribir los datos de audio en el archivo
    wf.close()

    print(f"Se ha grabado el archivo {nombre_archivo}")

def obtener_texto():
    # Carga el modelo de detección de idioma
    model = whisper.load_model('base')
    
    # Carga el archivo de audio grabado previamente
    audio = whisper.load_audio("grabacion.wav")
    
    # Aplica padding o recorte al audio para que tenga la longitud requerida por el modelo
    audio = whisper.pad_or_trim(audio)
    
    # Calcula el espectrograma de Mel en escala logarítmica a partir del audio
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    
    # Detecta el idioma en base al espectrograma de Mel
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")
    
    # Configura las opciones de decodificación del modelo
    options = whisper.DecodingOptions(fp16=False)
    
    # Decodifica el espectrograma de Mel para obtener el texto transcrito
    result = whisper.decode(model, mel, options)
    
    # Devuelve el texto transcrito
    return result.text

def enviar_texto(texto):
    
    openai.api_key = '###'
    
    prompt = (texto)
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024
    )
    
    return response["choices"][0]["text"]
    
def generar_voz(texto):
    
    engine = pyttsx3.init()
    engine.say(texto)
    
    for voice in engine.getProperty('voices'):
        print(voice)
    
    voice = engine.getProperty('voices')
    engine.setProperty('voice', "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_trTR_Tolga")
    #engine.setProperty('voice',voice[2].id)
    engine.runAndWait()

grabar_audio("grabacion.wav", 5)  # Grabar 10 segundos de audio y guardarlos en un archivo .wav con el nombre "grabacion.wav"

resultadoMicro = obtener_texto() # Tomar el archivo .wav y convertirlo a texto usando la libreria whisper
print(resultadoMicro)

resultadoGPT = enviar_texto(resultadoMicro)
print(resultadoGPT)

generar_voz(resultadoGPT)