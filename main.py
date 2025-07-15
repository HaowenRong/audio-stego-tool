import argparse
from encoder import *
from decoder import *

argParser = argparse.ArgumentParser(
  description='Audio Stego Tool'
)

subparsers = argParser.add_subparsers(dest='selection', required=True)

# encoding args
encode = subparsers.add_parser('encode', help='Embed a message into an audio file')
# required args
encode.add_argument('filePath',   type=str)
encode.add_argument('stegoText',  type=str)
encode.add_argument('outputPath', type=str)
# optional args
encode.add_argument(
  '--startFrame', '-sf',
  type=int,
  default=0,
  help='The frame the encoder will start embedding from (default: 0)'
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
  help='not yet implemented'
)

# decode args
decode = subparsers.add_parser('decode', help='Extract a message from an audio file')
decode.add_argument('filePath',      type=str)
decode.add_argument('messageLength', type=int)
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

args = argParser.parse_args()

if args.selection == 'encode':
  encodeMessage(
    # required params
    args.filePath, args.stegoText, args.outputPath,
    # optional params
    startingFrame=1, channels=args.channels, lsbDepth=args.depth
    )
elif args.selection == 'decode':
  decodeMessage(
    # required params
    args.filePath, args.messageLength,
    # optional params
    startingFrame=1, channels=args.channels
    )
