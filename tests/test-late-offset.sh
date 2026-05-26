# run from root
cd "$(dirname "$0")/.."

testName="late offset"

# file variables
dir="audio-files/"
textFile="stego-texts/stego.txt"

# flac
inputFile="cover.flac"
outputFile="stego-${testName}.flac"

# params
startingFrame="10000"
depth="8"
channels="2"

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
  "${dir}${outputFile}" 1000 \
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
  "${dir}${outputFile}" 1000 \
  -sf "${startingFrame}" -ch "${channels}" -d "${depth}" -o "${dir}${testName}-wav.txt"


checkOutput() {
    local label="$1"
    local decodedFile="$2"
    local expectedFile="$3"

    if diff -q "$expectedFile" "$decodedFile"; then
      echo "PASS [$label]"
      echo "::notice::✅ ${testName} ${label} test passed"
    else
      echo "FAIL [$label]"
      echo "::error::❌ ${testName} ${label} test failed"
    fi
}

expectedOutputsDir="tests/expected-outputs/"

checkOutput "flac" "${dir}${testName}-flac.txt" "${expectedOutputsDir}${testName}-flac.txt"
checkOutput "wav"  "${dir}${testName}-wav.txt"  "${expectedOutputsDir}${testName}-wav.txt"