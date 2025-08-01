import io
import ffmpeg
import soundfile as sf
from fileHandling import *

video = "audio-files/vinput1.mkv"

def getCodecInfo(stream, display=False):
  codec      = stream.get('codec_name')
  channels   = stream.get('channels')
  samplerate = stream.get('sample_rate')

  if display:
    print('codec      :', codec)
    print('channels   :', channels)
    print('samplerate :', samplerate)

  return codec, channels, samplerate

def extractAudio(videoPath, codec):
  try:
    out, err = (
      ffmpeg
      .input(video)
      .output('pipe:', format=codec)
      .run(capture_stdout=True, capture_stderr=True)
    )
  except ffmpeg.Error as e:
    print("FFmpeg stderr output:\n", e.stderr.decode())
    raise

  return out


def extractAudioFromVideo(videoPath, selectedStream=0):
  # get all streams
  codecInfo    = ffmpeg.probe(video)
  # filter audio streams
  audioStreams = [stream for stream in codecInfo['streams'] if stream['codec_type'] == 'audio']

  audioStream  = audioStreams[selectedStream]
  codec, channels, samplerate = getCodecInfo(audioStream, display=True)

  audioPath = io.BytesIO(extractAudio(videoPath, codec))
  print(sf.info(audioPath))
  audio = readAudio(audioPath)

extractAudioFromVideo(video)



# for i, stream in enumerate(audio_streams):
#   print(f"Audio Stream {i}:")
#   print(f"  Codec     : {stream.get('codec_name')}")
#   print(f"  Channels  : {stream.get('channels')}")
#   print(f"  Sample rate: {stream.get('sample_rate')}")
#   print(f"  Bit rate  : {stream.get('bits_per_sample', 'N/A')}")
#   print()


"""
try:
  out, err = (
    ffmpeg
    .input(video)
    .output('pipe:', format='flac')
    .run(capture_stdout=True, capture_stderr=True)
  )
except ffmpeg.Error as e:
  print("FFmpeg stderr output:\n", e.stderr.decode())
  raise

audio = sf.read(io.BytesIO(out))
info  = sf.info(io.BytesIO(out))
# audio = readAudio(io.BytesIO(out))
print(info)
"""