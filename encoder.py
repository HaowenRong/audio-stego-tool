import numpy     as np
import soundfile as sf
from commonFunctions import *

def encodeMessage(inputPath, stegoText, coverPath,
                  startingFrame=0, channels=1, lsbDepth=0):
  print('\n\n____Encoding________________')

  # read audio file
  data, totalChannels, samplerate = readAudio(inputPath, display=False)

  stegoBits = textToBits(stegoText)

  channels  = checkSelectedChannels(channels, totalChannels)

  for i, char in enumerate(stegoBits, start=startingFrame):
    # select channel to use based on selected number of channels
    channel = i % channels
    frame   = data[i][channel]

    if char == extractFromFrame(frame):
      continue

    data[i][channel] = modifyFrame(frame, display=False)

  # write to cover file
  sf.write(coverPath, data, samplerate)
  
  # copy metadata
  copyMetadata(inputPath, coverPath, display=True)

  # compare audio properties
  compareAudio(inputPath, coverPath)
