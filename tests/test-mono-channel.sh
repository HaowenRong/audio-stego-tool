# run from root
cd "$(dirname "$0")/.."

testName="mono"

# file variables
dir="audio-files/"
textFile="stego-texts/stego.txt"

# flac
inputFile="cover.flac"
outputFile="stego-${testName}.flac"

# params
startingFrame="0"
depth="8"
channels="1"

echo "----------------------------------------"
echo "test:          $testName"
echo "depth:         $depth"
echo "channels:      $channels"
echo "startingFrame: $startingFrame"
echo "----------------------------------------"

# encode
python -m stego.main encode \
  "${dir}${inputFile}" "${dir}${textFile}" "${dir}${outputFile}" \
  -sf "${startingFrame}" -ch "${channels}" -d "${depth}" -rf y

# decode
python -m stego.main decode \
  "${dir}${outputFile}" 100 \
  -sf "${startingFrame}" -ch "${channels}" -d "${depth}" -o "${dir}${testName}-flac.txt"

# wav
inputFile="cover.wav"
outputFile="stego-${testName}.wav"

# encode
python -m stego.main encode \
  "${dir}${inputFile}" "${dir}${textFile}" "${dir}${outputFile}" \
  -sf "${startingFrame}" -ch "${channels}" -d "${depth}" -rf y

# decode
python -m stego.main decode \
  "${dir}${outputFile}" 100 \
  -sf "${startingFrame}" -ch "${channels}" -d "${depth}" -o "${dir}${testName}-wav.txt"