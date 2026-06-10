import numpy as np

## modify last bit to 1
def modifyFrame(frameValue, display=False):
  if display:
    print('\n____Modifying Frame________')
    print('Original Float :', frameValue)
    print('Original bits  :', bin(frameValue))

  frameValue |= 1

  if display:
    print('Modified Float :', frameValue)
    print('Modified bits  :', bin(frameValue))
    print('------------------------------')

  return frameValue

## extract last bit from frame
def extractFromFrame(frameValue, display=False):
  frameLSB = frameValue & 1
  
  if display:
    print('\n____Extracting From Frame________')
    print('Frame value  :', frameValue)
    print('Frame Binary :', bin(frameValue))
    print('Frame LSB    :', frameLSB)
    print('------------------------------')
  
  return str(frameLSB)

# Multi bit functions
## extract lsb from binary
def extractLSBs(frameValue, depth, display=False):
  mask      = (1 << depth) - 1
  frameLSBs = frameValue & mask

  if display:
    print('\n____Extracting LSBs From Frame________')
    print('Depth        :', depth)
    print('Frame value  :', frameValue)
    print('Frame Binary :', bin(frameValue))
    print('Frame LSBs   :', bin(frameLSBs))
    print('------------------------------')

  return format(frameLSBs, f'0{depth}b')

## split binary into chunks
def splitBits(bits, depth):
  chunks = []

  i = 0
  while i < len(bits):
    chunk = bits[i:i + depth]
    chunks.append(chunk)
    
    i += depth

  return np.array(chunks)

## embed into lsb
def modifyLSBs(frameValue, lsbArray, depth, display=False):
  clearMask = ~((1 << depth) - 1)
  lsbMask   =  (1  << depth) - 1

  lsbArray = int(lsbArray, 2)

  modifiedBin = (frameValue & clearMask) | (lsbArray & lsbMask)

  if display:
    print('\n____Modifiying LSBs From Frame________')
    print('Depth        :', depth)
    print('Frame value  :', bin(frameValue))
    print('LSB array    :', bin(lsbArray))
    print('Modified bin :', bin(modifiedBin))
    print('------------------------------')

  return modifiedBin