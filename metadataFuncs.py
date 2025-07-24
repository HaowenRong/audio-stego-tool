from pathlib import Path

from mutagen      import File
from mutagen.wave import WAVE
from mutagen.mp3  import MP3
from mutagen.id3  import ID3

def copyWavMetadata(inputPath, coverPath):
  sourceFile = WAVE(inputPath)
  coverFile  = WAVE(coverPath)

  coverFile.tags = sourceFile.tags

  coverFile.save()

  return coverFile.tags, sourceFile.tags

def copyFlacMetadata(inputPath, coverPath):
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

  return coverFile.tags, sourceFile.tags

def copyMp3Metadata(inputPath, coverPath):
  sourceFile = MP3(inputPath)
  coverFile  = MP3(coverPath)

  coverFile.clear()
  coverFile.tags = sourceFile.tags
  coverFile.save()

def copyMetadata(inputPath, coverPath, display=False):
  format = (Path(inputPath).suffix).lower()

  if   format == '.wav':
    sourceData, coverData = copyWavMetadata(inputPath, coverPath)
  elif format == '.flac':
    sourceData, coverData = copyFlacMetadata(inputPath, coverPath)
  elif format == '.mp3':
    copyMp3Metadata(inputPath, coverPath)
    return

  if display == True:
    print('\n____Copying metadata________')
    print(f'{inputPath}  >  {coverPath}')
    print('\nTags----')
    print('Original :', sourceData)
    print()
    print('Cover    :', coverData)
    # print('\nPictures----')
    # print('Original :', sourceData)
    # print('Cover    :', coverData)
    print('------------------------------')
