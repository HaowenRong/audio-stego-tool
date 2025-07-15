import sys
from encoder import *
from decoder import *

np.set_printoptions(threshold=1000)

args    = sys.argv
numArgs = len(args)

option   = args[1]
filePath = args[2]

if option == 'encode' and numArgs == 5:
  stegoText  = args[3]
  outputPath = args[4]
  encodeMessage(filePath, stegoText, outputPath, startingFrame=1)
elif option == 'decode' and numArgs == 4:
  messageLength = args[3]
  decodeMessage(filePath, int(messageLength), startingFrame=1)
else:
  print('Invalid args')
  sys.exit()
