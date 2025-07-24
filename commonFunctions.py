import numpy     as np
import soundfile as sf

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
