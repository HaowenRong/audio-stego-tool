import numpy     as np
import soundfile as sf
from commonFunctions import *

def decodeMessage(coverPath, messageLength,
                  outputPath=None,
                  startingFrame=0, channels=1, lsbDepth=1):
  print('\n\n____Decoding________________')

  # read audio file
  data, totalChannels, samplerate = readAudio(coverPath)

  totalFrames   = len(data)

  bitsInChar    = 8
  messageLength = messageLength * bitsInChar

  channels      = checkSelectedChannels(channels, totalChannels)
  startingFrame = checkStartingFrame(startingFrame, totalFrames)
  endingFrame   = startingFrame + messageLength

  stegoBits = ''
  for frame in range(startingFrame, endingFrame):
    channel = frame % channels
    lsb     = extractLSBs(data[frame][channel], lsbDepth, display=True)
    stegoBits += lsb
    
  
  # convert extracted bits to text and remove null values
  stegoText = bitsToText(stegoBits).replace('\x00', '')

  print(stegoBits)
  print(stegoText)
  print('------------------------------')

  # save to file
  if outputPath != None:
    saveStegoText(outputPath, stegoText)
