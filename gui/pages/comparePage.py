from gi.repository import Gtk
from .. import components

from stego.compare import compareAudio

class ComparePage(Gtk.Box):
  def __init__(self):
    super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=40)
    self.add_css_class('page-container')

    # file selection --------------------------------
    self.fileSection = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, homogeneous=True)
    self.fileSection.set_halign(Gtk.Align.CENTER)

    self.audioSelection1 = components.Button('Select Audio File 1...',
      styles=['select-file-btn'])
    self.audioSelection2 = components.Button('Select Audio File 2...',
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

    self.fileSection.append(self.audioSelection1)
    self.fileSection.append(self.audioSelection2)

    dir='audio-files/'
    inputFile1='input2.flac'
    inputFile2='input2-out.flac'

    # submit button --------------------------------
    submitButton = components.Button('Compare',
      styles=['btn', 'submit-btn'],
      actions=[])
    
    submitButton = components.Button('Compare',
      styles=['btn', 'submit-btn'],
      actions=[lambda: compareAudio(
        f'{dir}{inputFile}',
        getStegoText(f'{dir}{textFile}'),
        f'{dir}{outputFile}',
        startingFrame=int(fieldStFrame.get_text()),
        channels=int(fieldChannel.get_text()),
        lsbDepth=int(fieldDepth.get_text()))],
        )
    
    submitButton = components.Button('Compare',
      styles=['btn', 'submit-btn'],
      actions=[lambda: compareAudio(
        f'{dir}{inputFile1}',
        f'{dir}{inputFile2}',
        int(fieldMsgLength.get_text()),
        startingFrame=int(fieldStFrame.get_text()),
        channels=int(fieldChannel.get_text()),
        lsbDepth=int(fieldDepth.get_text()))])

    # add elements to page --------------------------------
    self.append(self.fileSection)
    self.append(self.inputsRow)
    self.append(submitButton)
