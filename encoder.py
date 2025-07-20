import numpy     as np
import soundfile as sf
from commonFunctions import *

def encodeMessage(inputPath, stegoText, coverPath,
                  startingFrame=0, channels=1, lsbDepth=1):
  print('\n\n____Encoding________________')

  # read audio file
  data, totalChannels, samplerate = readAudio(inputPath, display=False)

  stegoBits = textToBits(stegoText)
  channels  = checkSelectedChannels(channels, totalChannels)

  if lsbDepth == 1:

    print(stegoBits)

    for i, char in enumerate(stegoBits, start=startingFrame):
      # select channel to use based on selected number of channels
      channel = i % channels
      frame   = data[i][channel]

      if char == extractFromFrame(frame, display=False):
        continue
      
      # data[i][channel] = modifyFrame(frame, display=True)

      data[i][channel] = modifyLSBs(frame, char, 1, display=True)
  elif lsbDepth > 1:
    stegoChunks = splitBits(stegoBits, lsbDepth)
    print(stegoChunks)

    for i, chunk in enumerate(stegoChunks, start=startingFrame):
      channel = i % channels
      frame   = data[i][channel]
      print(frame, chunk, lsbDepth)

      data[i][channel] = modifyLSBs(frame, chunk, lsbDepth, display=True)

  # write to cover file
  sf.write(coverPath, data, samplerate)
  
  # copy metadata
  copyMetadata(inputPath, coverPath, display=True)

  # compare audio properties
  compareAudio(inputPath, coverPath)
