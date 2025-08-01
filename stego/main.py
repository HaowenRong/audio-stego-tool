import argparse
from encoder import *
from decoder import *
from compare import *

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
  '--readFile', '-rf',
  type=str,
  default='n',
  help='Read message from a text file. (default: N)'
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
decode.add_argument(
  '--output', '-o',
  type=str,
  default=None,
  help='Output the extracted text into a file.'
)
decode.add_argument(
  '--depth', '-d',
  type=int,
  default=1,
  help='The number of LSBs to extract for a given frame. (default: 1)'
)

# compare args
compare = subparsers.add_parser('compare', help='')
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
  if args.readFile.lower() == 'y':
    stegoText = getStegoText(args.stegoText)
  else:
    stegoText = args.stegoText
  encodeMessage(
    # required params
    args.filePath, stegoText, args.outputPath,
    # optional params
    startingFrame=args.startFrame, channels=args.channels, lsbDepth=args.depth
    )
elif args.selection == 'decode':
  decodeMessage(
    # required params
    args.filePath, args.messageLength,
    # optional params
    outputPath=args.output, startingFrame=args.startFrame, channels=args.channels,
    lsbDepth=args.depth
    )
elif args.selection == 'compare':
  compareAudio(
    args.audioPath1, args.audioPath2, args.messageLength,
    startingFrame=args.startFrame, channels=args.channels, lsbDepth=args.depth)
