from gi.repository import Gtk
from .. import components

from stego.encoder import encodeMessage
from stego.fileHandling import getStegoText, renamePath
from stego.fileHandling import readAudio

class EncodePage(Gtk.Box):
  def __init__(self):
    super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=40)
    self.add_css_class('page-container')

    self.audio = None

    def loadAudio(path):
      self.audio = readAudio(path)

    # file selection --------------------------------
    self.fileSection = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, homogeneous=True)
    self.fileSection.set_halign(Gtk.Align.CENTER)

    self.audioSelection = components.FilePickerButton('Select Cover File...',
      styles=['select-file-btn'],
      actions=[lambda: loadAudio(self.audioSelection.label.get_text())])
    self.outputSelection = components.FilePickerButton('Select Stego File...',
      styles=['select-file-btn'])

    self.durationLabel = components.Label(f'Duration: 0s')


    def updateDurationWithParameters():
      components.updateDuration(self.durationLabel, 
                                self.audio,
                                message=getStegoText(self.outputSelection.label.get_text()),
                                startingFrame=(fieldStFrame.get_text()),
                                channels=(fieldChannel.get_text()),
                                lsbDepth=(fieldDepth.get_text()))

    fieldStFrame = components.Entry('Starting frame',
      styles=['btn', 'entry-field'],
      actions=[lambda: updateDurationWithParameters()])
    fieldChannel = components.Entry('Channels',
      styles=['btn', 'entry-field'],
      actions=[lambda: updateDurationWithParameters()])
    fieldDepth = components.Entry('LSB Depth',
      styles=['btn', 'entry-field'],
      actions=[lambda: updateDurationWithParameters()])

    self.inputsRow = components.InputRow(
      styles=['entries-container'],
      labels=['Starting Frame', 'Channels', 'Depth'],
      fields=[fieldStFrame, fieldChannel, fieldDepth])

    self.inputsRow.attach(self.durationLabel, 3,1,1,1)

    self.fileSection.append(self.audioSelection)
    self.fileSection.append(self.outputSelection)

    # submit button --------------------------------
    submitButton = components.Button('Encode',
      styles=['btn', 'submit-btn'],
      actions=[
        lambda: print('Parameters', fieldStFrame.get_text(),
          fieldChannel.get_text(),
          fieldDepth.get_text()),
        lambda: encodeMessage(
        self.audioSelection.label.get_text(),
        getStegoText(self.outputSelection.label.get_text()),
        renamePath(self.audioSelection.label.get_text(), '_cover'),
        startingFrame=int(fieldStFrame.get_text()),
        channels=int(fieldChannel.get_text()),
        lsbDepth=int(fieldDepth.get_text()))]
        )

    # add elements to page --------------------------------
    self.append(self.fileSection)
    self.append(self.inputsRow)
    self.append(submitButton)
