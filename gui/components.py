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
