import numpy     as np
import soundfile as sf
from commonFunctions import *

def decodeMessage(coverPath, messageLength):
  print('\n\n____Decoding________________')

  # read audio file
  data, channels, samplerate = readAudio(coverPath)

  bitsInChar = 8
  messageLength = messageLength * bitsInChar

  stegoBits = ''
  for frame in range(messageLength):
    lsb = extractFromFrame(data[frame][0])
    stegoBits += lsb
  
  print(stegoBits)
  print(bitsToText(stegoBits))

  print('------------------------------')
