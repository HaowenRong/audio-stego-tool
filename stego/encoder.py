import numpy     as np
import soundfile as sf
from .commonFunctions import *
from .metadataFuncs   import *
from .fileHandling    import *
from .compare         import *
from .bitManipulation import *
from .encryption      import *

def encodeMessage(inputPath, coverPath,
                  stegoText='', stegoPath='',
                  startingFrame=0, channels=1, lsbDepth=1,
                  encrypt=False, encryptionKey=None):

  print('\n\n____Encoding________________')

  encodingInfo = {
    'message':       '',
    'coverFilePath': coverPath,
    'key':           encryptionKey,
    'startingFrame': startingFrame,
    'channelsUsed':  channels,
    'depth':         lsbDepth
  }

  # read audio file
  try:
    audio = readAudio(inputPath, display=True)
  except Exception as e:
    message = (f'Invalid audio file path: "{inputPath}"')
    encodingInfo['message'] = message
    print(e)
    return encodingInfo
  
  # read stego text
  if stegoPath != '':
    try:
      stegoText = getStegoText(stego)
    except Exception as e:
      message = (f'Invalid stego file path: "{stego}"')
      encodingInfo['message'] = message
      print(e)
      return encodingInfo

  # encryption
  if encrypt == 'True':
    print('encrypting??')
    if not encryptionKey:
      encryptionKey = generateKey().decode()
      encodingInfo['key'] = encryptionKey

    stegoText = encryptText(stegoText, encryptionKey)

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

  message = (f'Embedded file created at "{coverPath}" with properties: \nstarting frame: {startingFrame}, channels: {channels}, lsb depth: {lsbDepth}')
  if encrypt == 'True':
    message += (f',\nencryption key: {encryptionKey}')
  encodingInfo['message'] = message

  print(encodingInfo)

  return encodingInfo