from gi.repository import Gtk
from .. import components
from stego.decoder import decodeMessage
from stego.fileHandling import renamePath

class DecodePage(Gtk.Box):
  def __init__(self):
    super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=40)
    self.add_css_class('page-container')

    # file selection --------------------------------
    self.fileSection = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, homogeneous=True)
    self.fileSection.set_halign(Gtk.Align.CENTER)
    self.audioSelection = components.FilePickerButton('Select Cover File...',
      styles=['select-file-btn'])

    fieldMsgLength = components.Entry('0',
      styles=['btn', 'entry-field'])
    fieldStFrame = components.Entry('0',
      styles=['btn', 'entry-field'])
    fieldChannel = components.Entry('1',
      styles=['btn', 'entry-field'])
    fieldDepth = components.Entry('1',
      styles=['btn', 'entry-field'])

    fieldKey = components.Entry('...',
      styles=['btn', 'entry-field'],
    actions=[])
    fieldKey.set_width_chars(50)

    self.inputsRow = components.InputRowUniform(
      styles=['entries-container'],
      labels=['Message Length*', 'Starting Frame', 'Channels', 'Depth'],
      fields=[fieldMsgLength, fieldStFrame, fieldChannel, fieldDepth])
    
    self.inputsRow2 = components.InputRow(
      styles=['entries-container'],
      labels=['Encryption Key (Optional)'],
      fields=[fieldKey])

    self.fileSection.append(self.audioSelection)

    dir='audio-files/'
    inputFile='input2-out.flac'
    outputFile='input2-out.txt'
    textFile='stego-texts/stegoText2.py'

    # submit button --------------------------------
    submitButton = components.Button('Decode',
      styles=['btn', 'submit-btn'],
      actions=[
        lambda: print(fieldKey.get_text()),
        lambda: decodeMessage(
          self.audioSelection.label.get_text(),
          int(fieldMsgLength.get_text()),
          outputPath=renamePath(self.audioSelection.label.get_text(), '_extracted', '.txt'),
          startingFrame=int(fieldStFrame.get_text()),
          channels=int(fieldChannel.get_text()),
          lsbDepth=int(fieldDepth.get_text()),
          encryptionKey=str(fieldKey.get_text()))]
        )
    # add elements to page --------------------------------
    self.append(self.fileSection)
    self.append(self.inputsRow)
    self.append(self.inputsRow2)
    self.append(submitButton)
