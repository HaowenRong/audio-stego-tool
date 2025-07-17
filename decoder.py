import numpy     as np
import soundfile as sf
from commonFunctions import *

def decodeMessage(coverPath, messageLength,
                  output=None,
                  startingFrame=0, channels=1):
  print('\n\n____Decoding________________')

  # read audio file
  data, totalChannels, samplerate = readAudio(coverPath)

  totalFrames   = len(data)

  bitsInChar    = 8
  messageLength = messageLength * bitsInChar

  channels      = checkSelectedChannels(channels, totalChannels)
  startingFrame = checkStartingFrame(startingFrame, totalFrames)

  stegoBits = ''
  for frame in range(startingFrame, messageLength):
    channel = frame % channels
    lsb     = extractFromFrame(data[frame][channel])
    stegoBits += lsb
  
  # convert extracted bits to text and remove null values
  stegoText = bitsToText(stegoBits).replace('\x00', '')

  print(stegoBits)
  print(stegoText)
  print('------------------------------')

  # save to file
  if output != None:
    saveStegoText(output, stegoText)
