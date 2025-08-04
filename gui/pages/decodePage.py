from gi.repository import Gtk
from .. import components
from stego.decoder import decodeMessage

class DecodePage(Gtk.Box):
  def __init__(self):
    super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=40)
    self.add_css_class('page-container')

    # file selection --------------------------------
    self.fileSection = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, homogeneous=True)
    self.fileSection.set_halign(Gtk.Align.CENTER)
    self.audioSelection = components.Button('Select Cover File...',
      styles=['select-file-btn'])

    fieldMsgLength = components.Entry('Message Length',
      styles=['btn', 'entry-field'])
    fieldStFrame = components.Entry('Starting Frame',
      styles=['btn', 'entry-field'])
    fieldChannel = components.Entry('Channels',
      styles=['btn', 'entry-field'])
    fieldDepth = components.Entry('LSB Depth',
      styles=['btn', 'entry-field'])

    self.inputsRow = components.InputRow(
      styles=['entries-container'],
      labels=['Message Length', 'Starting Frame', 'Channels', 'Depth'],
      fields=[fieldMsgLength, fieldStFrame, fieldChannel, fieldDepth])

    self.fileSection.append(self.audioSelection)

    dir='audio-files/'
    inputFile='input2-out.flac'
    outputFile='input2-out.txt'
    textFile='stego-texts/stegoText2.py'

    # submit button --------------------------------
    submitButton = components.Button('Decode',
      styles=['btn', 'submit-btn'],
      actions=[lambda: decodeMessage(
        f'{dir}{inputFile}',
        int(fieldMsgLength.get_text()),
        outputPath=f'{dir}{outputFile}',
        startingFrame=int(fieldStFrame.get_text()),
        channels=int(fieldChannel.get_text()),
        lsbDepth=int(fieldDepth.get_text()))])
    # add elements to page --------------------------------
    self.append(self.fileSection)
    self.append(self.inputsRow)
    self.append(submitButton)
