import gi
from gi.repository import Gtk
gi.require_version('Gtk', '4.0')

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
  def __init__(self, placeholderText, halign=Gtk.Align.CENTER, styles=[], fields=[]):
    super().__init__()

    self.set_halign(halign)

    self.set_placeholder_text(placeholderText)

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

