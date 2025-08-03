from gi.repository import Gtk
from .. import components

from stego.encoder import encodeMessage

class EncodePage(Gtk.Box):
  def __init__(self):
    super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=40)
    self.add_css_class('page-container')

    # file selection --------------------------------
    self.fileSection = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, homogeneous=True)
    self.fileSection.set_halign(Gtk.Align.CENTER)

    self.audioSelection = components.Button('Select Cover File...',
      styles=['select-file-btn'])
    self.outputSelection = components.Button('Select Stego File...',
      styles=['select-file-btn'])

    fieldStFrame = components.Entry('Starting frame',
      styles=['btn', 'entry-field'])
    fieldChannel = components.Entry('Channels',
      styles=['btn', 'entry-field'])
    fieldDepth = components.Entry('LSB Depth',
      styles=['btn', 'entry-field'])

    self.inputsRow = components.InputRow(
      styles=['entries-container'],
      labels=['Starting Frame', 'Channels', 'Depth'],
      fields=[fieldStFrame, fieldChannel, fieldDepth])

    self.fileSection.append(self.audioSelection)
    self.fileSection.append(self.outputSelection)

    dir='audio-files/'
    inputFile='input2.flac'
    outputFile='input2-out.flac'
    textFile='stego-texts/stegoText2.py'

    # submit button --------------------------------
    submitButton = components.Button('Encode',
      styles=['btn', 'submit-btn'],
      actions=[lambda: encodeMessage(
        f'{dir}{inputFile}',
        f'{dir}{textFile}',
        f'{dir}{outputFile}',
        startingFrame=int(fieldStFrame.get_text()),
        channels=int(fieldChannel.get_text()),
        lsbDepth=int(fieldDepth.get_text()))])

    # add elements to page --------------------------------
    self.append(self.fileSection)
    self.append(self.inputsRow)
    self.append(submitButton)
