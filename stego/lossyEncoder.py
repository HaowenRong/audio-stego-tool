from bitstring import ConstBitStream

from .mp3Functions import *

def lossyEncoder(file):
  expectedMpeg  = ''
  expectedLayer = ''

  frameData = bytearray()

  bs = ConstBitStream(filename=file)

  tagData = readTags(bs)
  frameData.extend(tagData['tagDataBits'].tobytes())

  expectedMpeg, expectedLayer = findExpectedData(bs)
  print(expectedMpeg, expectedLayer)

  for i in range(1):
    print('a -------------------------------- finding sync')
    findFirstSync(bs, expectedMpeg, expectedLayer)
    print('b -------------------------------- reading frame')
    frame = readFrame(bs)
    # print(frame.bin)
    print('c -------------------------------- end')
  
  with open('mp3out.mp3', 'wb') as out:
    out.write(frameData)

