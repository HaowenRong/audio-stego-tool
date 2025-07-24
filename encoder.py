import numpy     as np
import soundfile as sf
from commonFunctions import *
from metadataFuncs   import *
from fileHandling    import *
from compare         import *
from bitManipulation import *

def encodeMessage(inputPath, stegoText, coverPath,
                  startingFrame=0, channels=1, lsbDepth=1):
  print('\n\n____Encoding________________')

  # read audio file
  audio = readAudio(inputPath, display=True)

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
    audio['data'][i][channel] = modifyLSBs(frame, segment, lsbDepth, display=False)

  # write to cover file
  sf.write(coverPath, audio['data'], audio['samplerate'], subtype=audio['subtype'])
  
  # copy metadata
  # copyMetadata(inputPath, coverPath, display=True)
  copyMetadata(inputPath, coverPath, display=True)

  # compare audio properties
  compareAudioInfo(inputPath, coverPath)
