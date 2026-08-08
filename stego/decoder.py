import numpy     as np
import soundfile as sf
import math
from .commonFunctions import *
from .fileHandling    import *
from .bitManipulation import *
from .encryption      import *

def decodeMessage(audioPath, messageLength,
                  outputPath=None,
                  startingFrame=0, channels=1, lsbDepth=1,
                  encryptionKey=None):
  print('\n\n____Decoding________________')

  decodingInfo = {
    'message':       '',
    'coverFilePath': audioPath,
    'messageLength': messageLength,
    'key':           encryptionKey,
    'startingFrame': startingFrame,
    'channelsUsed':  channels,
    'depth':         lsbDepth
  }

  # read audio file
  try:
    audio = readAudio(audioPath, display=True)
  except Exception as e:
    message = (f'Invalid audio file path: "{audioPath}"')
    decodingInfo['message'] = message
    print(e)
    
    return decodingInfo

  totalFrames = getTotalFrames(messageLength, lsbDepth, encrypted=(True if encryptionKey else False))
  print('totalFrames ------------------------- ', totalFrames)

  channels      = checkSelectedChannels(channels, audio['channels'])
  startingFrame = checkStartingFrame(startingFrame, audio['frames'])
  endingFrame   = checkEndingFrame(startingFrame + totalFrames, audio['frames'])

  # decode bits
  totalBits     = getTotalBits(messageLength, encrypted=encryptionKey)
  collectedBits = []
  remainingBits = totalBits % lsbDepth

  for frame in range(startingFrame, endingFrame):
    channel   = frame % channels
    lastFrame = (frame == endingFrame - 1)

    if lastFrame and remainingBits != 0:
      lsbDepth = remainingBits

    # extract bits
    lsb = extractLSBs(audio['data'][frame][channel], lsbDepth, display=False)
    collectedBits.append(lsb)

  stegoBits = ''.join(collectedBits)

  # convert extracted bits to text and remove null values
  stegoText = bitsToText(stegoBits, display=True).replace('\x00', '')

  if encryptionKey:
    try:
      stegoText = decryptText(stegoText, encryptionKey)
    except Exception as e:
      message = (f'Error decrypting with encryption key: "{encryptionKey}"')
      decodingInfo['message'] = message
      print(e)
      return decodingInfo

  print('------------------------------')

  # save to file
  if outputPath != None:
    saveStegoText(outputPath, stegoText)
  else:
    print(stegoText)
  
  message = (f'Decoded text to "{outputPath}" using properties: \nmessage length: {messageLength} starting frame: {startingFrame}, channels: {channels}, lsb depth: {lsbDepth}')
  if encryptionKey:
    message += (f',\nencryption key: {encryptionKey}')
  decodingInfo['message'] = message

  return decodingInfo