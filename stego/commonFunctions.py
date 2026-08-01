import numpy     as np
import soundfile as sf
from .fileHandling import readAudio
import math

def textToBits(stegoText, display=False):
  bits = ''.join(format(ord(char), '08b') for char in stegoText)

  if display == True:
    print('\n____Converting text to bits________')
    print('Text ----------------\n', frameValue)
    print('Bits ----------------\n', bin(frameValue))

  return bits

def bitsToText(bits, display=False):
  chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
  text  = ''.join(chr(int(char, 2)) for char in chars)

  if display == True:
    print('\n____Converting bits to text________')
    print('Bits ----------------\n', bits)
    print('Text ----------------\n', text)

  return text


def checkSelectedChannels(channels, totalChannels):
    # make sure selected number of channels does not exceed total channels
  if channels > totalChannels:
    print(f'Selected channels ({channels}) exceeds total channels of selected audio file ({totalChannels}).')
    print(f'Setting channels to audios total. {channels} > {totalChannels}')
    channels = totalChannels
  
  return channels

def checkStartingFrame(frame, totalFrames):

  if frame >= totalFrames:
    print(f'Selected starting frame ({frame}) exceeds total frames of selected audio file ({totalFrames}).')
    print(f'Setting starting frame to 0. {frame} > {0}')
    frame = totalFrames
  
  return frame

def checkEndingFrame(frame, totalFrames):

  if frame >= totalFrames:
    print(f'Ending frame ({frame}) exceeds total frames of selected audio file ({totalFrames}).')
    print(f'Setting ending frame to {totalFrames}. {frame} > {totalFrames}')
    frame = totalFrames
  
  return frame

def calcCapacity(filePath, startingFrame=0, channels=1, lsbDepth=1):
  if startingFrame == '':
    startingFrame = 0
  if channels == '':
    channels = 1
  if lsbDepth == '':
    lsbDepth = 1
  
  try:
    audio = readAudio(filePath, display=True)
  except Exception as e:
    print(f"Invalid file path during capacity calculation: {e}")
    return 0

  totalFrames = audio['data'].size
  print(audio['data'])
  print('tf', totalFrames)
  framesUsed  = totalFrames - int(startingFrame)
  print(framesUsed)

  capacity = totalFrames * int(channels) * int(lsbDepth)

  print(capacity)
  return capacity

def calcDuration(audio, message, startingFrame=0, channels=1, lsbDepth=1):
  sampleRate = audio['samplerate']
  totalFrames = audio['data'].shape[0]

  # convert to bit string
  #messageBits = ''.join(f'{ord(c):08b}' for c in message)

  if not startingFrame:
    startingFrame = 0

  if not channels:
    channels = 1

  if not lsbDepth:
    lsbDepth = 1

  messageLen = len(message)  # number of bits

  bitsPerFrame = int(channels) * int(lsbDepth)
  # print('bpf Mlen', bitsPerFrame, messageLen)
  # print('params', startingFrame, channels, lsbDepth)

  framesNeeded = math.ceil(messageLen / bitsPerFrame)
  # print('tframes', framesNeeded, sampleRate)
  duration = framesNeeded / sampleRate

  return duration
