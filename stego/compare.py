import numpy     as np
import soundfile as sf
from .commonFunctions import *
from .fileHandling    import *

def compareAudio(audioPath1, audioPath2, messageLength,
                 startingFrame=0, channels=1, lsbDepth=1):
  print('\n\n____Comparing________________')

  # read audio file
  audio1 = readAudio(audioPath1, display=False)
  audio2 = readAudio(audioPath2, display=False)

  compareAudioInfo(audioPath1, audioPath2)

  channels      = checkSelectedChannels(channels, audio1['channels'])
  startingFrame = checkStartingFrame(startingFrame, audio1['frames'])
  endingFrame   = checkEndingFrame(startingFrame + messageLength, audio1['frames'])

  for frame in range(startingFrame, endingFrame):
    channel = frame % channels

    just = 16

    print('Frame', frame, ':', audio1['data'][frame][0], '|', audio2['data'][frame][0])
    print(bin(audio1['data'][frame][channel]).rjust(just))
    print(bin(audio2['data'][frame][channel]).rjust(just))
  