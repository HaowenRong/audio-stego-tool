import numpy     as np
import soundfile as sf
from commonFunctions import *

def decodeMessage(filePath, messageLength):
  print('Decoding')

  # read audio file
  data, channels, samplerate = readAudio(filePath)

  bitsInChar = 8
  messageLength = messageLength * bitsInChar

  stegoBits = ''
  for frame in range(messageLength):
    lsb = extractFromFrame(data[frame][0])
    stegoBits += lsb
  
  print(stegoBits)
  print(bitsToText(stegoBits))
