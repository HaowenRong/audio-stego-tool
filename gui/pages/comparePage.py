from gi.repository import Gtk
import components

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

    self.fileSection.append(self.audioSelection1)
    self.fileSection.append(self.audioSelection2)

    # submit button --------------------------------
    submitButton = components.Button('Compare',
      styles=['btn', 'submit-btn'],
      actions=[])

    # add elements to page --------------------------------
    self.append(self.fileSection)
    self.append(submitButton)
