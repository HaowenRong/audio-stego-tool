import argparse
from .encoder import *
from .decoder import *
from .compare import *

argParser = argparse.ArgumentParser(
  description='Audio Stego Tool'
)

subparsers = argParser.add_subparsers(dest='selection', required=True)

# encoding args
encode = subparsers.add_parser('encode', help='Embed a message into an audio file')
# required args
encode.add_argument('filePath',   type=str)
encode.add_argument('outputPath', type=str)
# optional args
encode.add_argument(
  '--stegoText', '-st',
  type=str,
  default='',
  help='The stego text to encode'
)
encode.add_argument(
  '--stegoPath', '-sp',
  type=str,
  default='',
  help='The path to the stego text file to encode'
)
encode.add_argument(
  '--startFrame', '-sf',
  type=int,
  default=0,
  help='The frame the encoder will start embedding from. (default: 0)'
)
encode.add_argument(
  '--channels', '-ch',
  type=int,
  default=1,
  help='The number of channels that will be used when embedding the message. (default: 1)'
)
encode.add_argument(
  '--depth', '-d',
  type=int,
  default=1,
  help='The number of LSBs to modify for a given frame. (default: 1)'
)
encode.add_argument(
  '--encrypt', '-e',
  type=str,
  default=False,
  help='Encrypt the text. (default: False)'
)
encode.add_argument(
  '--encryptionKey', '-key',
  type=str,
  default=None,
  help='Use own key for encryption. Key will be generated if not provided (default: None)'
)

# decode args
decode = subparsers.add_parser('decode', help='Extract a message from an audio file')
decode.add_argument('filePath',      type=str)
decode.add_argument('messageLength', type=int)
decode.add_argument(
  '--outputPath', '-o',
  type=str,
  default='',
  help='The path to the output text file'
)
decode.add_argument(
  '--startFrame', '-sf',
  type=int,
  default=0,
  help='The frame the decoder will start extracting from (default: 0)'
)
decode.add_argument(
  '--channels', '-ch',
  type=int,
  default=1,
  help='The number of channels that will be used when extracting the message. (default: 1)'
)
decode.add_argument(
  '--depth', '-d',
  type=int,
  default=1,
  help='The number of LSBs to extract for a given frame. (default: 1)'
)
decode.add_argument(
  '--encryptionKey', '-key',
  type=str,
  default=None,
  help='Use key for decryption. Decryption will not be performed if no key. (default: None)'
)

# compare args
compare = subparsers.add_parser('compare', help='Compare audio files with eachother')
compare.add_argument('audioPath1', type=str)
compare.add_argument('audioPath2', type=str)
compare.add_argument('messageLength', type=int)
compare.add_argument(
  '--startFrame', '-sf',
  type=int,
  default=0,
  help='The frame the comparison will start from (default: 0)'
)
compare.add_argument(
  '--channels', '-ch',
  type=int,
  default=1,
  help='The number of channels that will be compared. (default: 1)'
)
compare.add_argument(
  '--depth', '-d',
  type=int,
  default=1,
  help='not yet implemented'
)

args = argParser.parse_args()

if args.selection == 'encode':
  encodeMessage(
    # required params
    args.filePath, args.outputPath,
    # optional params
    args.stegoText, args.stegoPath,
    startingFrame=args.startFrame, channels=args.channels, lsbDepth=args.depth,
    encrypt=args.encrypt, encryptionKey=args.encryptionKey
  )
elif args.selection == 'decode':
  decodeMessage(
    # required params
    args.filePath, args.messageLength,
    # optional params
    outputPath=args.outputPath,
    startingFrame=args.startFrame, channels=args.channels, lsbDepth=args.depth,
    encryptionKey=args.encryptionKey
  )
elif args.selection == 'compare':
  compareAudio(
    args.audioPath1, args.audioPath2, args.messageLength,
    startingFrame=args.startFrame, channels=args.channels, lsbDepth=args.depth)
