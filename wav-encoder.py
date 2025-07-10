import numpy     as np
import soundfile as sf
from commonFunctions import *

np.set_printoptions(threshold=1000)

def encodeMessage(filePath, stegoText, outputPath):
  print('Encoding')

  # read audio file
  data, channels, samplerate = readAudio(filePath)

  stegoBits = textToBits(stegoText)

  for i, char in enumerate(stegoBits):
    channel = 0
    frame = data[i][channel]

    if char == extractFromFrame(frame):
      continue

    data[i][channel] = modifyFrame(frame, display=True)

  sf.write(outputPath, data, samplerate)
  compareAudio(filePath, outputPath)

  data, channels, samplerate = readAudio('outy.flac')

  for i in range(0, 100):
    frame = data[i][0]
    print(frame)


encodeMessage('input.flac', 'test', 'outy.flac')


