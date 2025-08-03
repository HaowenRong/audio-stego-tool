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

    # submit button --------------------------------
    submitButton = components.Button('Decode',
      styles=['btn', 'submit-btn'],
      actions=[])

    # add elements to page --------------------------------
    self.append(self.fileSection)
    self.append(self.inputsRow)
    self.append(submitButton)
