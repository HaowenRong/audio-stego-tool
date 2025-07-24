import numpy     as np
import soundfile as sf
from commonFunctions import *
from fileHandling    import *
from bitManipulation import *

def decodeMessage(coverPath, messageLength,
                  outputPath=None,
                  startingFrame=0, channels=1, lsbDepth=1):
  print('\n\n____Decoding________________')

  # read audio file
  audio = readAudio(coverPath)

  messageLength = messageLength * audio['bitDepth']

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
  stegoText = bitsToText(stegoBits).replace('\x00', '')

  print(stegoBits)
  print(stegoText)
  print('------------------------------')

  # save to file
  if outputPath != None:
    saveStegoText(outputPath, stegoText)
