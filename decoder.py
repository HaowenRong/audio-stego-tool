import numpy     as np
import soundfile as sf
from commonFunctions import *

np.set_printoptions(threshold=1000)

def decodeMessage(filePath, stegoText):
  print('Decoding')

  # read audio file
  data, channels, samplerate = readAudio(filePath)

  stegoBits = textToBits(stegoText)
  length = len(stegoBits)

  print(data)

  print(stegoBits)

  stegoText = ''
  for frame in range(length):
    print(data[frame][0])
    lsb = extractFromFrame(data[frame][0])
    print(lsb)
    stegoText += lsb
  
  print(stegoText)
  print(bitsToText(stegoText))

