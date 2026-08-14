#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"

dir="../audio-files/"
textFile="stego-texts/stego.txt"

messageLength=$(( $(printf '%s' "$(cat "${dir}${textFile}")" | wc -c | tr -d '[:space:]') + 1 ))

encryptionKey="hHP9G_X4wT_WL4I1M5YOyH7g8pFnA-LwjA_2z0jsu_w="

echo "messageLength: $messageLength"
echo "encryptionKey: $encryptionKey"
echo "--------------------------------"

# basic tests
./use-case.sh --testName "basic" \
  --depth 1 --channels 1 --startingFrame 0 \
  --messageLength "$messageLength"

./use-case.sh --testName "high-capacity" \
  --depth 8 --channels 2 --startingFrame 0 \
  --messageLength "$messageLength"

# encrypted basic
./use-case.sh --testName "encrypted-basic" \
  --depth 1 --channels 1 --startingFrame 0 \
  --encrypt true --encryptionKey "$encryptionKey" \
  --messageLength "$messageLength"

./use-case.sh --testName "encrypted-high-capacity" \
  --depth 8 --channels 2 --startingFrame 0 \
  --encrypt true --encryptionKey "$encryptionKey" \
  --messageLength "$messageLength"


# odd depth tests
./use-case.sh --testName "odd-depth-3" \
  --depth 3 --channels 1 --startingFrame 0 \
  --messageLength "$messageLength"

./use-case.sh --testName "odd-depth-5" \
  --depth 5 --channels 1 --startingFrame 0 \
  --messageLength "$messageLength"

./use-case.sh --testName "odd-depth-7" \
  --depth 7 --channels 1 --startingFrame 0 \
  --messageLength "$messageLength"

# encrypted odd depth
./use-case.sh --testName "encrypted-odd-depth" \
  --depth 5 --channels 1 --startingFrame 0 \
  --encrypt true --encryptionKey "$encryptionKey" \
  --messageLength "$messageLength"


# late offset test
./use-case.sh --testName "late-offset" \
  --depth 1 --channels 1 --startingFrame 200000 \
  --messageLength "$messageLength"

# encrypted late offset
./use-case.sh --testName "encrypted-late-offset" \
  --depth 1 --channels 1 --startingFrame 200000 \
  --encrypt true --encryptionKey "$encryptionKey" \
  --messageLength "$messageLength"


# channel tests
./use-case.sh --testName "mono-channel" \
  --depth 2 --channels 1 --startingFrame 0 \
  --messageLength "$messageLength"

./use-case.sh --testName "dual-channel" \
  --depth 2 --channels 2 --startingFrame 0 \
  --messageLength "$messageLength"


echo "--------------------------------"
echo "All use-cases completed."
