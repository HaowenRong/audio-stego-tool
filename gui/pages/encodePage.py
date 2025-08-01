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

    self.fileSection.append(self.audioSelection)
    self.fileSection.append(self.outputSelection)

    # submit button --------------------------------
    submitButton = components.Button('Encode',
      styles=['btn', 'submit-btn'],
      actions=[])

    # add elements to page --------------------------------
    self.append(self.fileSection)
    self.append(submitButton)
