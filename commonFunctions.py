import numpy as np
import soundfile as sf


def textToBits(stegoText):
  return ''.join(format(ord(char), '08b') for char in stegoText)

def bitsToText(bits):
  chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
  return ''.join(chr(int(char, 2)) for char in chars)


def readAudio(filePath):
  data, samplerate = sf.read(filePath, dtype='int16')
  channels = len(data.shape)
  seconds  = data.shape[0] / samplerate
  minutes  = seconds       / 60

  print('\n' + filePath)
  print('Shape      :', data.shape)
  print('Samplerate :', samplerate)
  print('Seconds    :', seconds)
  print('Minutes    :', minutes)
  print('Channels   :', channels)

  return data, channels, samplerate

def compareAudio(audioPath1, audioPath2):
  readAudio(audioPath1)
  readAudio(audioPath2)

def modifyFrame(frameValue, display=False):
  frameFloat = np.float32(frameValue)
  frameInt   = frameFloat.view(np.int32)

  frameFlipped = frameInt ^ 1

  frameFinal = frameFlipped.view(np.float32)

  if display:
    print('Modifying Frame________')
    print('Original Float :', frameFloat)
    print('   Final Float :', frameFinal)
    print('Original bits :', bin(frameInt))
    print(' Flipped bits :', bin(frameFlipped))

  return frameFinal

def extractFromFrame(frameValue, display=False):
  frameFloat = np.float32(frameValue)
  frameInt   = frameFloat.view(np.int32)
  frameLSB   = frameInt & 1
  
  if display:
    print('Extracting From Frame________')
    print('Frame value  :', frameFloat)
    print('Frame Binary :', bin(frameInt))
    print('Frame LSB    :', frameLSB)
  
  return str(frameLSB)
