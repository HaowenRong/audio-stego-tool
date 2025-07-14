import numpy     as np
import soundfile as sf
from commonFunctions import *
from mutagen import File

def encodeMessage(inputPath, stegoText, coverPath,
                  startingFrame=0, channels=1, lsbDepth=0):
  print('\n\n____Encoding________________')

  # read audio file
  data, totalChannels, samplerate = readAudio(inputPath, display=False)

  stegoBits = textToBits(stegoText)

  # make sure selected number of channels does not exceed total channels
  if channels > totalChannels:
    print(f'Selected channels ({channels}) exceeds total channels of selected audio file ({totalChannels}).')
    print(f'Setting channels to audios total. {channels} > {totalChannels}')
    channels = totalChannels

  for i, char in enumerate(stegoBits, start=startingFrame):
    # select channel to use based on selected number of channels
    channel = i % channels
    frame   = data[i][channel]

    if char == extractFromFrame(frame):
      continue

    data[i][channel] = modifyFrame(frame, display=False)

  # write to cover file
  sf.write(coverPath, data, samplerate)
  
  # copy metadata
  copyMetadata(inputPath, coverPath, display=True)

  # compare audio properties
  compareAudio(inputPath, coverPath)

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
