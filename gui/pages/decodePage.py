from gi.repository import Gtk

class DecodePage(Gtk.Box):
  def __init__(self):
    super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=40)
    self.add_css_class('page-container')

    # file selection --------------------------------
    self.fileSection = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, homogeneous=True)
    self.fileSection.set_halign(Gtk.Align.CENTER)
    self.audioSelection  = Gtk.Button(label='Select Cover File...')
    self.audioSelection.add_css_class('select-file-btn')

    self.fileSection.append(self.audioSelection)

    # submit button --------------------------------
    self.btnSubmit = Gtk.Button(label='Decode')
    self.btnSubmit.set_halign(Gtk.Align.CENTER)
    self.btnSubmit.add_css_class('btn')
    self.btnSubmit.add_css_class('submit-btn')

    # add elements to page --------------------------------
    self.append(self.fileSection)
    self.append(self.btnSubmit)
