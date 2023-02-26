import pyaudio
import wave
import os
import whisper

def grabar_audio(nombre_archivo, duracion_segundos):
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
    for i in range(0, int(input_rate / chunk * duracion_segundos)):
        data = stream.read(chunk)  # Leer los datos de audio del stream
        frames.append(data)

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
    
    model = whisper.load_model('base')
    
    audio = whisper.load_audio("grabacion.wav")
    audio = whisper.pad_or_trim(audio)
    
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    
    _, probs = model.detect_language(mel)
    print(f"Detected language: {max(probs, key=probs.get)}")
    
    options = whisper.DecodingOptions(fp16=False)
    result = whisper.decode(model, mel, options)
    
    return result.text

# Ejemplo de uso
grabar_audio("grabacion.wav", 10)  # Grabar 10 segundos de audio y guardarlos en un archivo .wav con el nombre "grabacion.wav"

resultado = obtener_texto()
print(resultado)