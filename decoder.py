import numpy     as np
import soundfile as sf
from commonFunctions import *

def decodeMessage(coverPath, messageLength,
                  channels=1):
  print('\n\n____Decoding________________')

  # read audio file
  data, totalChannels, samplerate = readAudio(coverPath)

  bitsInChar = 8
  messageLength = messageLength * bitsInChar

  # make sure selected number of channels does not exceed total channels
  if channels > totalChannels:
    print(f'Selected channels ({channels}) exceeds total channels of selected audio file ({totalChannels}).')
    print(f'Setting channels to audios total. {channels} > {totalChannels}')
    channels = totalChannels

  stegoBits = ''
  for frame in range(messageLength):
    channel = frame % channels
    lsb     = extractFromFrame(data[frame][channel])
    stegoBits += lsb
  
  print(stegoBits)
  print(bitsToText(stegoBits))

  print('------------------------------')
