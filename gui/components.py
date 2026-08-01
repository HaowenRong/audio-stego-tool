import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Pango
from stego.commonFunctions import calcCapacity, calcDuration

class Label(Gtk.Label):
  def __init__(self, label, halign=Gtk.Align.CENTER, styles=[]):
    super().__init__(label=label)

    self.set_halign(halign)

    # apply css
    for style in styles:
      self.add_css_class(style)

class Button(Gtk.Button):
  def __init__(self, label, halign=Gtk.Align.CENTER, styles=[], actions=[]):
    super().__init__(label=label)

    self.set_halign(halign)

    # apply css
    for style in styles:
      self.add_css_class(style)

    # connect button functionality
    def performActions(self):
      for action in actions:
        action()

    self.connect('clicked', performActions)

class Entry(Gtk.Entry):
  def __init__(self, placeholderText, halign=Gtk.Align.CENTER, styles=[], fields=[], actions=[]):
    super().__init__()

    self.set_halign(halign)

    self.set_placeholder_text(placeholderText)

    # apply css
    for style in styles:
      self.add_css_class(style)
    
    # connect button functionality
    def performActions(self):
      for action in actions:
        action()

    self.connect('changed', performActions)

class Switch(Gtk.Switch):
  def __init__(self, placeholderText, halign=Gtk.Align.CENTER, styles=[], fields=[], actions=[]):
    super().__init__()

    self.set_vexpand(False)
    self.set_valign(Gtk.Align.CENTER)  # Or Gtk.Align.START / Gtk.Align.END

    # apply css
    for style in styles:
      self.add_css_class(style)

class SpinButton(Gtk.SpinButton):
  def __init__(self, halign=Gtk.Align.CENTER, styles=[], fields=[]):
    super().__init__()

    self.set_halign(halign)

    # apply css
    for style in styles:
      self.add_css_class(style)

class InputRow(Gtk.Grid):
  def __init__(self, halign=Gtk.Align.CENTER, styles=[], labels=[], fields=[]):
    super().__init__()

    self.set_halign(halign)
    self.set_row_spacing(4)
    self.set_column_spacing(8)

    # apply css
    for style in styles:
      self.add_css_class(style)

    # create and add labels
    for i, (text, field) in enumerate(zip(labels, fields)):
      label = Gtk.Label(label=text)
      label.set_halign(Gtk.Align.START)
      label.set_valign(Gtk.Align.CENTER)
      label.add_css_class('entry-label')
      self.attach(label, i, 0, 1, 1)
      self.attach(field, i, 1, 1, 1)

class InputRowUniform(Gtk.Grid):
  def __init__(self, halign=Gtk.Align.CENTER, styles=[], labels=[], fields=[]):
    super().__init__()

    self.set_halign(halign)
    self.set_row_spacing(4)
    self.set_column_spacing(8)

    # apply css
    for style in styles:
      self.add_css_class(style)

    # create and add labels
    for i, (text, field) in enumerate(zip(labels, fields)):
      field.set_size_request(200, -1)
      label = Gtk.Label(label=text)
      label.set_halign(Gtk.Align.START)
      label.set_valign(Gtk.Align.CENTER)
      label.add_css_class('entry-label')
      self.attach(label, i, 0, 1, 1)
      self.attach(field, i, 1, 1, 1)

class outputBox(Gtk.Label):
  def __init__(self, label, halign=Gtk.Align.CENTER, styles=[]):
    super().__init__(label=label)

    self.set_halign(halign)

    # apply css
    for style in styles:
      self.add_css_class(style)

class FilePickerButton(Gtk.Button):
  def __init__(self, label, halign=Gtk.Align.CENTER, styles=[], actions=[]):
    super().__init__()

    self.label = Gtk.Label(label=label)
    self.label.set_wrap(True)
    self.label.set_wrap_mode(Pango.WrapMode.WORD_CHAR)
    self.label.set_width_chars(34)
    self.label.set_max_width_chars(34)

    self.actions = actions

    self.set_child(self.label)

    # apply css
    for style in styles:
      self.add_css_class(style)

    self.connect('clicked', self.selectFile)

  def selectFile(self, button):
    dialog = Gtk.FileDialog.new()
    dialog.set_title("Select a file")
    dialog.set_modal(True)

    dialog.open(
      parent=self.get_root(),
      cancellable=None,
      callback=self.selectedFile,
      user_data=dialog
    )

  def selectedFile(self, dialogObj, result, dialog):
    try:
      file = dialog.open_finish(result)
    except GLib.Error:
      print("Closed")
      return

    if file:
      filepath = file.get_path()
      print("Selected File:", filepath)

      self.label.set_label(filepath)

      # connect button functionality
      for action in self.actions:
        action()

def updateCapacity(capacityLabel, filePath, startingFrame, channels, lsbDepth):

  newLabel = f'Capacity: {calcCapacity(filePath, startingFrame, channels, lsbDepth) * 8} bytes'

  print(newLabel)
  capacityLabel.set_label(newLabel)

def updateDuration(durationLabel, audio, message, startingFrame, channels, lsbDepth):
  # print(audio)
  # print(message)
  message = ''.join(f'{ord(c):08b}' for c in message)
  newLabel = f'Duration: {calcDuration(audio, message, startingFrame, channels, lsbDepth)}s'

  # print(newLabel)
  durationLabel.set_label(newLabel)