import numpy     as np
import soundfile as sf
from commonFunctions import *

def encodeMessage(filePath, stegoText, outputPath):
  print('Encoding')

  # read audio file
  data, channels, samplerate = readAudio(filePath, display=False)

  stegoBits = textToBits(stegoText)

  for i, char in enumerate(stegoBits):
    channel = 0
    frame = data[i][channel]

    if char == extractFromFrame(frame):
      continue

    data[i][channel] = modifyFrame(frame, display=False)

  sf.write(outputPath, data, samplerate)
  compareAudio(filePath, outputPath)
