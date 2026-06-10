import pytest
import numpy as np
from numpy.testing import assert_array_equal

from stego.commonFunctions import *
from stego.bitManipulation import *

# textToBits
@pytest.mark.parametrize("stegoText, display, expected", [
  ('a', False, '01100001'),
  ('A', False, '01000001'),
  ('This is a test', False, '0101010001101000011010010111001100100000011010010111001100100000011000010010000001110100011001010111001101110100'),
  ('1', False, '00110001'),
  ('123456789', False, '001100010011001000110011001101000011010100110110001101110011100000111001')
])

def test_textToBits(stegoText, display, expected):
  assert textToBits(stegoText, display) == expected

# bitsToText
@pytest.mark.parametrize("bits, display, expected", [
  ('01100001', False, 'a'),
  ('01000001', False, 'A'),
  ('0101010001101000011010010111001100100000011010010111001100100000011000010010000001110100011001010111001101110100', False, 'This is a test'),
  ('00110001', False, '1'),
  ('001100010011001000110011001101000011010100110110001101110011100000111001', False, '123456789')
])

def test_bitsToText(bits, display, expected):
  assert bitsToText(bits, display) == expected

# modifyFrame
@pytest.mark.parametrize("frameValue, display, expected", [
  (0b01100001, False, 0b01100001),
  (0b01100000, False, 0b01100001)
])

def test_modifyFrame(frameValue, display, expected):
  assert modifyFrame(frameValue, display) == expected

# extractFromFrame
@pytest.mark.parametrize("frameValue, display, expected", [
  (0b01100001, False, '1'),
  (0b01100000, False, '0')
])

def test_extractFromFrame(frameValue, display, expected):
  assert extractFromFrame(frameValue, display) == expected

# extractFromFrame
@pytest.mark.parametrize("frameValue, depth, display, expected", [
  (0b01100101, 1, False, '1'),
  (0b01100101, 2, False, '01'),
  (0b01100101, 3, False, '101'),
  (0b01100101, 4, False, '0101'),
  (0b01100101, 5, False, '00101'),
  (0b01100101, 6, False, '100101'),
  (0b01100101, 7, False, '1100101'),
  (0b01100101, 8, False, '01100101'),

  (0b01010101, 1, False, '1'),
  (0b01010101, 2, False, '01'),
  (0b01010101, 3, False, '101'),
  (0b01010101, 4, False, '0101'),
  (0b01010101, 5, False, '10101'),
  (0b01010101, 6, False, '010101'),
  (0b01010101, 7, False, '1010101'),
  (0b01010101, 8, False, '01010101')
])

def test_extractLSBs(frameValue, depth, display, expected):
  assert extractLSBs(frameValue, depth, display) == expected

# splitBits
@pytest.mark.parametrize("bits, depth, expected", [
  ('01000011011010000110010101100101011100110110010100001010', 1, np.array(['0', '1', '0', '0', '0', '0', '1', '1', '0', '1', '1', '0', '1', '0', '0', '0', '0', '1', '1', '0', '0', '1', '0', '1', '0', '1', '1', '0', '0', '1', '0', '1', '0', '1', '1', '1', '0', '0', '1', '1', '0', '1', '1', '0', '0', '1', '0', '1', '0', '0', '0', '0', '1', '0', '1', '0'])),
  ('01000011011010000110010101100101011100110110010100001010', 2, np.array(['01', '00', '00', '11', '01', '10', '10', '00', '01', '10', '01', '01', '01', '10', '01', '01', '01', '11', '00', '11', '01', '10', '01', '01', '00', '00', '10', '10'])),
  ('01000011011010000110010101100101011100110110010100001010', 3, np.array(['010', '000', '110', '110', '100', '001', '100', '101', '011', '001', '010', '111', '001', '101', '100', '101', '000', '010', '10'])),
  ('01000011011010000110010101100101011100110110010100001010', 4, np.array(['0100', '0011', '0110', '1000', '0110', '0101', '0110', '0101', '0111', '0011', '0110', '0101', '0000', '1010'])),
  ('01000011011010000110010101100101011100110110010100001010', 5, np.array(['01000', '01101', '10100', '00110', '01010', '11001', '01011', '10011', '01100', '10100', '00101', '0'])),
  ('01000011011010000110010101100101011100110110010100001010', 6, np.array(['010000', '110110', '100001', '100101', '011001', '010111', '001101', '100101', '000010', '10'])),
  ('01000011011010000110010101100101011100110110010100001010', 7, np.array(['0100001', '1011010', '0001100', '1010110', '0101011', '1001101', '1001010', '0001010'])),
  ('01000011011010000110010101100101011100110110010100001010', 8, np.array(['01000011', '01101000', '01100101', '01100101', '01110011', '01100101', '00001010']))
])

def test_splitBits(bits, depth, expected):
    splitBitArr = splitBits(bits, depth)
    assert_array_equal(splitBitArr, expected)

# modifyLSBs
@pytest.mark.parametrize("frameValue, lsbArray, depth, display, expected", [
  (0b01010100, '1', 1, False, '0b01010101'),
  (0b01010110, '1', 1, False, '0b01010111'),
  (0b01010101, '11', 2, False, '0b01010111'),
  (0b01010111, '10', 2, False, '0b01010110'),
  (0b01010101, '111', 3, False, '0b01010111'),
  (0b01010111, '101', 3, False, '0b01010101'),
  (0b01010101, '1111', 4, False, '0b01011111'),
  (0b01010111, '1010', 4, False, '0b01011010'),
  (0b01010101, '11111', 5, False, '0b01011111'),
  (0b01010111, '10101', 5, False, '0b01010101'),
  (0b01010101, '111111', 6, False, '0b01111111'),
  (0b01010111, '101010', 6, False, '0b01101010'),
  (0b01010101, '1111111', 7, False, '0b01111111'),
  (0b01010111, '0101010', 7, False, '0b00101010'),
  (0b01010101, '11111111', 8, False, '0b11111111'),
  (0b01010111, '10101010', 8, False, '0b10101010')
])

def test_modifyLSBs(frameValue, lsbArray, depth, display, expected):
  assert modifyLSBs(frameValue, lsbArray, depth, display) == int(expected, 2)