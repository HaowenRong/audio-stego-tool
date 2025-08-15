# tag functions
def readTags(bs):
  startPos = bs.pos
  
  # check if there are ID3 tags
  indicator = bs.read('bytes:3')

  if indicator != b'ID3':
    print('No ID3v2 tag')
    return
  
  print('ID3v2 tag found')

  # read IDv3 details
  verMajor = bs.read('uint:8')
  verRev   = bs.read('uint:8')
  flags    = bs.read('uint:8')

  # get sizes of the tags
  sizeBytes = [bs.read('uint:8') for _ in range(4)]
  tagsSize  = (sizeBytes[0] << 21) | (sizeBytes[1] << 14) | (sizeBytes[2] << 7) | sizeBytes[3]

  print(f'ID3v2.{verMajor}.{verRev}')
  print(f'Tag size {tagsSize} bytes')

  # read tag data
  tagData = bs.read(f'bytes:{tagsSize}')

  endPos = bs.pos

  # retrieve bit data of the tags and reset position to end of tags
  bs.pos = startPos
  tagDataBits = bs.read(endPos - startPos)
  bs.pos = endPos

  return {
    'version'     : (verMajor, verRev),
    'flags'       : flags,
    'sizeBytes'   : tagsSize,
    'sizeBits'    : tagsSize * 8,
    'data'        : tagData,
    'tagDataBits' : tagDataBits
  }


# frame variables
layerMap = {
  0b01: 'l1',
  0b10: 'l2',
  0b11: 'l3'
}

mpegVerMap = {
  0b11: 'mpeg1',
  0b10: 'mpeg2',
  0b00: 'mpeg2.5',
  0b01: 'reserved'
}

samplerateTable = {
  'mpeg1'  : [44100, 48000, 32000, None],
  'mpeg2'  : [22050, 24000, 16000, None],
  'mpeg2.5': [11025, 12000, 8000,  None]
}

bitrateTable = {
  'mpeg1': {
    'l1': [None,32,64,96,128,160,192,224,256,288,320,352,384,416,448,None],
    'l2': [None,32,48,56,64,80,96,112,128,160,192,224,256,320,384,None],
    'l3': [None,32,40,48,56,64,80,96,112,128,160,192,224,256,320,None]
  },
  'mpeg2': {
    'l1': [None,32,48,56,64,80,96,112,128,144,160,176,192,224,256,None],
    'l2': [None,8,16,24,32,40,48,56,64,80,96,112,128,144,160,None],
    'l3': [None,8,16,24,32,40,48,56,64,80,96,112,128,144,160,None]
  },
  'mpeg2.5': {
    'l1': [None,32,48,56,64,80,96,112,128,144,160,176,192,224,256,None],
    'l2': [None,8,16,24,32,40,48,56,64,80,96,112,128,144,160,None],
    'l3': [None,8,16,24,32,40,48,56,64,80,96,112,128,144,160,None]
  }
}

# frame functions
def findExpectedData(bs):
  sync = 0b11111111111

  while bs.pos + 32 <= bs.len:
    startPos = bs.pos
    # loop until sync pattern is found
    window = bs.peek('uint:11')

    if window == sync:
      bs.pos += 11
      headerData = readHeader(bs)

      # check for a valid header
      if headerData['mpegVerBits'] == 0b01 or \
         headerData['layer']       == 0b00 or \
         headerData['bitrateIndex'] in (0b0000, 0b1111) or \
         headerData['samplerateIndex'] == 0b11:
        bs.pos = startPos + 1
        continue

      print(bs.pos)
      bs.pos = startPos
      return headerData['mpegVerBits'], headerData['layer']

def findFirstSync(bs, expectedMpeg, expectedLayer):
  sync = 0b11111111111

  while bs.pos + 32 <= bs.len:
    startPos = bs.pos

    # loop until sync pattern is found
    window = bs.peek('uint:11')

    if window == sync:
      bs.pos += 11
      headerData = readHeader(bs)

      # check for valid frame header values
      if headerData['mpegVerBits']     == 0b01 or \
         headerData['layer']           == 0b00 or \
         headerData['bitrateIndex']    in (0b0000, 0b1111) or \
         headerData['samplerateIndex'] == 0b11:
        bs.pos = startPos + 1
        continue

      # check if mpeg and layer match expected values
      if headerData['mpegVerBits'] != expectedMpeg or\
         headerData['layer'] != expectedLayer:
        bs.pos = startPos + 1
        continue

      print(bs.pos)
      # if the header is valid exit the loop
      bs.pos = startPos + 11
      return

    bs.pos += 1

  return None

def readHeader(bs):
  headerData = {
    'mpegVerBits'     : bs.read('uint:2'),
    'layer'           : bs.read('uint:2'),
    'protectionBit'   : bs.read(1),
    'bitrateIndex'    : bs.read('uint:4'),
    'samplerateIndex' : bs.read('uint:2'),
    'padding'         : bs.read('uint:1'),
    'privateBit'      : bs.read('uint:1'),
    'channelMode'     : bs.read('uint:2'),
    'modeExtention'   : bs.read('uint:2'),
    'copyrightBit'    : bs.read('uint:1'),
    'originalBit'     : bs.read('uint:1'),
    'emphasis'        : bs.read('uint:2')
  }

  return headerData

def calculateFrameLength(layer, samplerate, bitrate, mpegVer, padding):
  print(f'mpegVer {mpegVer}, Layer: {layer}, Bitrate: {bitrate} kbps, Samplerate: {samplerate} Hz, Padding: {padding}')

  trueBitrate = bitrate * 1000 # convert bytes to bits

  # perform frame length calculation based on layer
  if layer == 'l1':
    frameLength = ((12 * trueBitrate) // samplerate + padding) * 4
  else:
    frameLength = (144 * trueBitrate) // samplerate + padding

  return frameLength * 8

def readFrame(bs):
  headerData = readHeader(bs)

  print(headerData)

  layer      = layerMap.get(headerData['layer'], None)
  mpegVer    = mpegVerMap.get(headerData['mpegVerBits'], None)
  samplerate = samplerateTable[mpegVer][headerData['samplerateIndex']]
  bitrate    = bitrateTable[mpegVer][layer][headerData['bitrateIndex']]

  frameLength = calculateFrameLength(layer, samplerate,
                                     bitrate, mpegVer, headerData['padding'])

  frameLengthBits = frameLength * 8

  frame = bs.read(frameLengthBits)

  print(bs.pos, 'Frame Length:', frameLengthBits)

  return frame