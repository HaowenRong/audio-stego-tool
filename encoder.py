import numpy     as np
import soundfile as sf
from commonFunctions import *

def encodeMessage(inputPath, stegoText, coverPath,
                  startingFrame=0, channels=1, lsbDepth=1):
  print('\n\n____Encoding________________')

  # read audio file
  audio = readAudio(inputPath, display=False)

  stegoBits = textToBits(stegoText)
  channels  = checkSelectedChannels(channels, audio['channels'])
  
  # if using higher bit depths, split bits into chunks
  if lsbDepth > 1:
    stegoBits = splitBits(stegoBits, lsbDepth)

  for i, segment in enumerate(stegoBits, start=startingFrame):
    channel = i % channels
    frame   = audio['data'][i][channel]

    # skip frame if lsb is already the same
    if segment == extractLSBs(frame, lsbDepth, display=False):
      continue
    
    # modify bits
    audio['data'][i][channel] = modifyLSBs(frame, segment, lsbDepth, display=True)

  # write to cover file
  sf.write(coverPath, audio['data'], audio['samplerate'])
  
  # copy metadata
  copyMetadata(inputPath, coverPath, display=True)

  # compare audio properties
  compareAudio(inputPath, coverPath)
