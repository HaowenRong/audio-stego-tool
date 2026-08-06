import os
import soundfile as sf
from pathlib import Path

def getStegoText(filePath):
  with open(filePath, 'r', encoding='utf-8') as file:
    return file.read()

def saveStegoText(outputPath, extractedText):
  with open(outputPath, "w", encoding="utf-8") as file:
    file.write(extractedText)

bitDepthDict = {
  'PCM_U8': 8,
  'PCM_16': 16,
  'PCM_24': 24,
  'PCM_32': 32,
}

def readAudio(filePath, display=True):
  data, samplerate = sf.read(filePath, dtype='int16')

  info = sf.info(filePath)

  bitDepth = bitDepthDict.get(info.subtype, 8)

  if display == True:
    print('\n')
    print(filePath)
    print('Format     :', info.format)
    print('Shape      :', data.shape)
    print('Frames     :', info.frames)
    print('Samplerate :', info.samplerate)
    print('Bit Depth  :', info.subtype)
    print('duration   :', info._duration_str)
    print('Channels   :', info.channels)

  return {
    'data': data,
    'samplerate': samplerate,
    'channels': info.channels,
    'frames': info.frames,
    'bitDepth': bitDepth,
    'subtype': info.subtype
  }

def renamePath(filePath, performedAction, suffix=''):
  print(performedAction)
  basePath = Path(filePath)
  
  if suffix != '':
    suffixToAppend = suffix
  else:
    suffixToAppend = basePath.suffix

  modifiedFileName = basePath.stem + performedAction + suffixToAppend
  return basePath.parent / modifiedFileName

def viewAudio(filePath, frameRange=(0, 100)):
  data, channels, samplerate = readAudio(filePath)

  startFrame, endFrame = frameRange
  print(data[startFrame:endFrame])

def compareAudioInfo(audioPath1, audioPath2):
  readAudio(audioPath1)
  readAudio(audioPath2)
