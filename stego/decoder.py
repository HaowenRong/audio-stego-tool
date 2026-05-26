import numpy     as np
import soundfile as sf
import math
from .commonFunctions import *
from .fileHandling    import *
from .bitManipulation import *

def decodeMessage(coverPath, messageLength,
                  outputPath=None,
                  startingFrame=0, channels=1, lsbDepth=1):
  print('\n\n____Decoding________________')

  # read audio file
  audio = readAudio(coverPath)

  bitsInChar = 8
  messageLength = messageLength * math.ceil(bitsInChar / lsbDepth)
  print('depth', messageLength)

  channels      = checkSelectedChannels(channels, audio['channels'])
  startingFrame = checkStartingFrame(startingFrame, audio['frames'])
  endingFrame   = checkEndingFrame(startingFrame + messageLength, audio['frames'])

  stegoBits = ''
  for frame in range(startingFrame, endingFrame):
    channel = frame % channels

    # extract bits
    lsb = extractLSBs(audio['data'][frame][channel], lsbDepth, display=False)
    stegoBits += lsb
  
  # convert extracted bits to text and remove null values
  stegoText = bitsToText(stegoBits, display=True).replace('\x00', '')

  print('------------------------------')

  # save to file
  if outputPath != None:
    saveStegoText(outputPath, stegoText)
