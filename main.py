import sys
from encoder import *
from decoder import *

args = sys.argv

print(len(args))
if len(args) != 5:
  print('Invalid args')
  sys.exit()

option     = args[1]
filePath   = args[2]
stegoText  = args[3]
outputPath = args[4]

if option == 'encode':
  encodeMessage(filePath, stegoText, outputPath)
elif option == 'decode':
  decodeMessage(filePath, stegoText)
else:
  print('Invalid option')