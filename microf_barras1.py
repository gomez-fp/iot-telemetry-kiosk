import struct
import numpy as np
import pyaudio as pa
import scipy.io.wavfile as waves

global decibel
def MicrofonoPlacid():
    FRAMES = 256                                   # Tamaño del paquete a procesar
    FORMAT = pa.paInt16                              # Formato de lectura INT 16 bits
    CHANNELS = 1
    Fs = 44100                                       # Frecuencia de muestreo típica para audio
    dev_index = 1


    p = pa.PyAudio()

    stream = p.open(                                  # Abrimos el canal de audio con los parámeteros de configuración
        format = FORMAT,
        channels = CHANNELS,
        rate = Fs,
        input=True,
        frames_per_buffer=FRAMES
    )
    
#def MicrofonoPlacid():
    
    data = stream.read(FRAMES)                         # Leemos paquetes de longitud FRAMES
    dataInt = struct.unpack(str(FRAMES) + 'h', data)   # Convertimos los datos que se encuentran empaquetados en bytes   
    dataInt = np.array(dataInt)/2**31

    rms = np.sqrt(np.mean(dataInt**2))

    lin = 0.0019*(rms) + 63.917
    log = 12.565*np.log(rms) - 22.84
    pol = ((6.593064617029218e-12*np.power(rms, 3)) - (3.126758109633165e-07*np.power(rms, 2)) + (0.005706874207914*rms) + (57.782499032903810))

    if rms >= 19486.02102:
        decibel = lin
    elif 19486.02102 >= rms > 17500:
        decibel = lin
    elif 17500 >= rms > 15155.34739:
        decibel = lin
    elif 15155.34739 >= rms > 12900.9618:     
        decibel = lin
    elif 12900.9618 >= rms > 6137.804984:
        decibel = (lin*0.74)+(pol*0.26)
    elif 6137.804984 >= rms > 2127.967942:
        decibel = (lin*0.36)+(pol*0.64)
    elif 2127.967942 >= rms > 777.8289213:
        decibel = pol
    elif 777.8289213 >= rms > 468.568061:
        decibel = log
    elif 468.568061 <= rms:
        decibel = log
    else :
        decibel = 0
                  
    nuevoValor = decibel
    #print("rms = ", rms)
    #print("dB.ok = ", decibel)
    
    return nuevoValor
