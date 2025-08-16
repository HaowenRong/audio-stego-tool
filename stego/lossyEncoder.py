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

  while bs.pos + 32 <= bs.len - 1000:
    print('a -------------------------------- finding sync')
    sb = bs.pos
    print('starting bit:', sb)
    findFirstSync(bs, expectedMpeg, expectedLayer)
    fs = bs.pos - 11
    print('first sync:  ', fs, 'diff =', abs(fs-sb))
    print('b -------------------------------- reading frame')
    frame = readFrame(bs)
    modifiedFrame = modifyFrame(frame)
    frameData.extend(modifiedFrame.tobytes())
    # print(frame.bin)
    print('ending bit:  ', bs.pos)
    print('c -------------------------------- end\n\n')
  
  with open('mp3out.mp3', 'wb') as out:
    out.write(frameData)
