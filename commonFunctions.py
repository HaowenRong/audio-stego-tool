import numpy     as np
import soundfile as sf


def textToBits(stegoText):
  return ''.join(format(ord(char), '08b') for char in stegoText)

def bitsToText(bits):
  chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
  return ''.join(chr(int(char, 2)) for char in chars)


def readAudio(filePath, display=True):
  data, samplerate = sf.read(filePath, dtype='int16')
  channels = len(data.shape)
  seconds  = data.shape[0] / samplerate
  minutes  = seconds       / 60

  if display == True:
    print('\n' + filePath)
    print('Shape      :', data.shape)
    print('Samplerate :', samplerate)
    print('Seconds    :', seconds)
    print('Minutes    :', minutes)
    print('Channels   :', channels)

  return data, channels, samplerate

def viewAudio(filePath, frameRange=(0, 100)):
  data, channels, samplerate = readAudio(filePath)

  startFrame, endFrame = frameRange
  print(data[startFrame:endFrame])

def compareAudio(audioPath1, audioPath2):
  readAudio(audioPath1)
  readAudio(audioPath2)

def modifyFrame(frameValue, display=False):
  if display:
    print('\n____Modifying Frame________')
    print('Original Float :', frameValue)
    print('Original bits  :', bin(frameValue))

  frameValue |= 1

  if display:
    print('Original Float :', frameValue)
    print('Original bits  :', bin(frameValue))
    print('------------------------------')

  return frameValue

def extractFromFrame(frameValue, display=False):
  frameLSB = frameValue & 1
  
  if display:
    print('\n____Extracting From Frame________')
    print('Frame value  :', frameValue)
    print('Frame Binary :', bin(frameValue))
    print('Frame LSB    :', frameLSB)
    print('------------------------------')
  
  return str(frameLSB)
