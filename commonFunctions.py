import numpy     as np
import soundfile as sf
import os
from mutagen import File


def textToBits(stegoText, display=False):
  bits = ''.join(format(ord(char), '08b') for char in stegoText)

  if display == True:
    print('\n____Converting text to bits________')
    print('Text ----------------\n', frameValue)
    print('Bits ----------------\n', bin(frameValue))

  return bits

def bitsToText(bits, display=False):
  chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
  text  = ''.join(chr(int(char, 2)) for char in chars)

  if display == True:
    print('\n____Converting bits to text________')
    print('Bits ----------------\n', bits)
    print('Text ----------------\n', text)

  return text

def getStegoText(filePath):
  with open(filePath, 'r', encoding='utf-8') as file:
    return file.read()

def saveStegoText(outputPath, extractedText):
  with open(outputPath, "w", encoding="utf-8") as file:
    file.write(extractedText)



def readAudio(filePath, display=True):
  data, samplerate = sf.read(filePath, dtype='int16')

  info = sf.info(filePath)
  print(info)

  if display == True:
    print('\n' + filePath)
    print('Format     :', info.format)
    print('Shape      :', data.shape)
    print('Frames     :', info.frames)
    print('Samplerate :', info.samplerate)
    print('Bit Depth  :', info.subtype)
    print('duration   :', info._duration_str)
    print('Channels   :', info.channels)

  return data, info.channels, info.samplerate

def viewAudio(filePath, frameRange=(0, 100)):
  data, channels, samplerate = readAudio(filePath)

  startFrame, endFrame = frameRange
  print(data[startFrame:endFrame])

def compareAudio(audioPath1, audioPath2):
  readAudio(audioPath1)
  readAudio(audioPath2)

def modifyFrame(frameValue, display=False):
  if display:
    print('\n____Modifying Frame________')
    print('Original Float :', frameValue)
    print('Original bits  :', bin(frameValue))

  frameValue |= 1

  if display:
    print('Original Float :', frameValue)
    print('Original bits  :', bin(frameValue))
    print('------------------------------')

  return frameValue

def extractFromFrame(frameValue, display=False):
  frameLSB = frameValue & 1
  
  if display:
    print('\n____Extracting From Frame________')
    print('Frame value  :', frameValue)
    print('Frame Binary :', bin(frameValue))
    print('Frame LSB    :', frameLSB)
    print('------------------------------')
  
  return str(frameLSB)

def checkSelectedChannels(channels, totalChannels):
    # make sure selected number of channels does not exceed total channels
  if channels > totalChannels:
    print(f'Selected channels ({channels}) exceeds total channels of selected audio file ({totalChannels}).')
    print(f'Setting channels to audios total. {channels} > {totalChannels}')
    channels = totalChannels
  
  return channels

def checkStartingFrame(frame, totalFrames):
  print(frame, totalFrames)

  if frame >= totalFrames:
    print(f'Selected starting frame ({frame}) exceeds total frames of selected audio file ({totalFrames}).')
    print(f'Setting starting frame to 0. {frame} > {0}')
    frame = totalFrames
  
  return frame


def copyMetadata(inputPath, coverPath, display=False):
  sourceFile = File(inputPath)
  coverFile  = File(coverPath)

  # clear cover file metadata
  coverFile.clear()
  coverFile.clear_pictures()

  # copy tags
  for tag in sourceFile.tags.keys():
    coverFile[tag] = sourceFile[tag]
  
  # copy cover images
  for picture in sourceFile.pictures:
    coverFile.add_picture(picture)

  # save changes
  coverFile.save()
  
  if display == True:
    print('\n____Copying metadata________')
    print(f'{inputPath}  >  {coverPath}')
    print('\nTags----')
    print('Original :', sourceFile.tags.keys())
    print('Cover    :', coverFile.tags.keys())
    print('\nPictures----')
    print('Original :', sourceFile.pictures)
    print('Cover    :', coverFile.pictures)
    print('------------------------------')
