#!/bin/bash
set -euo pipefail

# run from root
cd "$(dirname "$0")/.."

# default variables
testName="test"
startingFrame="0"
depth="1"
channels="1"
encrypt="false"
encryptionKey=""
messageLength=""

# parse args
while [ $# -gt 0 ]; do
  case "$1" in
    --testName)      testName="$2";      shift 2 ;;
    --startingFrame) startingFrame="$2"; shift 2 ;;
    --depth)         depth="$2";         shift 2 ;;
    --channels)      channels="$2";      shift 2 ;;
    --encrypt)       encrypt="$2";       shift 2 ;;
    --encryptionKey) encryptionKey="$2"; shift 2 ;;
    --messageLength) messageLength="$2"; shift 2 ;;

    # exit if unknown arg
    *)
      echo "Unknown argument: $1" >&2
      exit 1 ;;
  esac
done

# file variables
dir="audio-files/"
textFile="stego-texts/stego.txt"
expectedOutputsDir="tests/expected-outputs/"

echo "----------------------------------------"
echo "test:          $testName"
echo "depth:         $depth"
echo "channels:      $channels"
echo "startingFrame: $startingFrame"
echo "encrypt:       $encrypt"
echo "messageLength: $messageLength"
echo "----------------------------------------"

testFailed=0

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
    testFailed=1
  fi
}

generatedFiles=()

runCase() {
  local format="$1"
  local inputFile="cover.${format}"
  local outputFile="stego-${testName}.${format}"
  local decodedFile="${dir}${testName}-${format}.txt"
  local expectedOutput="${dir}${textFile}"

  generatedFiles+=("${dir}${outputFile}" "${decodedFile}")

  if [ "$encrypt" = "true" ]; then
    python -m stego.main encode \
      "${dir}${inputFile}" "${dir}${outputFile}" \
      -sp "${dir}${textFile}" \
      -sf "${startingFrame}" -ch "${channels}" -d "${depth}" \
      -e "True" -key "${encryptionKey}"

    python -m stego.main decode \
      "${dir}${outputFile}" "${messageLength}" \
      -sf "${startingFrame}" -ch "${channels}" -d "${depth}" -o "${decodedFile}" \
      -key "${encryptionKey}"
  else
    python -m stego.main encode \
      "${dir}${inputFile}" "${dir}${outputFile}" \
      -sp "${dir}${textFile}" \
      -sf "${startingFrame}" -ch "${channels}" -d "${depth}"

    python -m stego.main decode \
      "${dir}${outputFile}" "${messageLength}" \
      -sf "${startingFrame}" -ch "${channels}" -d "${depth}" -o "${decodedFile}"
  fi

  checkOutput "$format" "$decodedFile" "$expectedOutput"
}

runCase "flac"
runCase "wav"

# cleanup (if tests passed)
if [ "$testFailed" -eq 1 ]; then
  echo "One or more checks failed. Generated files left in place for inspection."
  for f in "${generatedFiles[@]}"; do
    echo "  $f"
  done
  exit 1
else
  for f in "${generatedFiles[@]}"; do
    rm -f "$f"
  done
fi