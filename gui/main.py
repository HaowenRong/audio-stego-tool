import sys, os

import gi
from . import components
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk
from .pages.encodePage  import EncodePage
from .pages.decodePage  import DecodePage
from .pages.comparePage import ComparePage

class MainWindow(Gtk.Window):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

    # functional variables --------------------------------
    self.selection = 'encode'

    self.coverFilePath = ''
    self.StegoFilePath = ''

    # gui --------------------------------
    self.set_title('Audio Stego Tool')

    # styling --------------------------------
    provider = Gtk.CssProvider()
    provider.load_from_path('./gui/styles/root.css')

    css = Gtk.CssProvider()
    css.load_from_path('./gui/styles/styling.css')

    Gtk.StyleContext.add_provider_for_display(
      Gdk.Display.get_default(),
      provider,
      Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    Gtk.StyleContext.add_provider_for_display(
      Gdk.Display.get_default(),
      css,
      Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    # main container --------------------------------
    self.page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=40)
    self.page.add_css_class('page')

    # navi bar --------------------------------
    self.naviBar = Gtk.Grid()
    self.naviBar.set_column_spacing(20)
    self.naviBar.add_css_class('navi-bar')

    self.title = components.Label('Audio Stego Tool', styles=['title'])

    self.spacer = Gtk.Box()
    self.spacer.set_hexpand(True)

    self.options = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
    self.options.add_css_class('navi-options-container')
    self.options.set_halign(Gtk.Align.CENTER)

    self.btnEncode  = components.Button('Encode',
      styles =['btn', 'selection-btn', 'selection-btn-highlighted'],
      actions=[lambda: self.highlightSelection('encode'),
               lambda: self.stack.set_visible_child_name('encode')])
    self.btnDecode  = components.Button('Decode',
      styles =['btn', 'selection-btn'],
      actions=[lambda: self.highlightSelection('decode'),
               lambda: self.stack.set_visible_child_name('decode')])
    self.btnCompare = components.Button('Compare',
      styles =['btn', 'selection-btn'],
      actions=[lambda: self.highlightSelection('compare'),
               lambda: self.stack.set_visible_child_name('compare')])

    self.selectionButtons = {
      'encode':  self.btnEncode,
      'decode':  self.btnDecode,
      'compare': self.btnCompare
    }

    # attach elements together
    self.options.append(self.btnEncode)
    self.options.append(self.btnDecode)
    self.options.append(self.btnCompare)

    self.naviBar.attach(self.title,   0, 0, 1, 1)
    self.naviBar.attach(self.spacer,  1, 0, 1, 1)
    self.naviBar.attach(self.options, 2, 0, 1, 1)

    
    # page stack
    self.stack = Gtk.Stack()
    self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
    self.stack.set_transition_duration(300)

    self.stack.add_titled(EncodePage(),  'encode',  'Encode')
    self.stack.add_titled(DecodePage(),  'decode',  'Decode')
    self.stack.add_titled(ComparePage(), 'compare', 'Compare')
    
    
    # add elements to main page
    self.page.append(self.naviBar)
    self.page.append(self.stack)

    # add main container with all widgets --------------------------------
    self.set_child(self.page)
    
  def highlightSelection(self, newSelection):
    # update selection
    if newSelection == self.selection:
      return
    self.selection = newSelection

    # update ui elements
    for key, button in self.selectionButtons.items():
      button.remove_css_class('selection-btn-highlighted')
      if newSelection == key:
        button.add_css_class('selection-btn-highlighted')


class App(Gtk.Application):
  def __init__(self):
    super().__init__(application_id='StegoApp')

  def do_activate(self):
    win = MainWindow(application=self)
    win.present()

  def do_startup(self):
    Gtk.Application.do_startup(self)


app = App()
app.run()
