
import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk

class MainWindow(Gtk.Window):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.set_title('Audio Stego Tool')
    self.set_default_size(600, 200)

    provider = Gtk.CssProvider()
    provider.load_from_path('./root.css')

    css = Gtk.CssProvider()
    css.load_from_path('./styling.css')

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

    self.title = Gtk.Label(label='Audio Stego Tool')
    self.title.add_css_class('title')

    self.spacer = Gtk.Box()
    self.spacer.set_hexpand(True)

    self.options = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
    self.options.add_css_class('navi-options-container')
    self.options.set_halign(Gtk.Align.CENTER)

    self.btnEncode = Gtk.Button(label='Encode')
    self.btnEncode.add_css_class('btn')
    self.btnEncode.add_css_class('selection-button')

    self.btnDecode = Gtk.Button(label='Decode')
    self.btnDecode.add_css_class('btn')
    self.btnDecode.add_css_class('selection-button')

    self.btnCompare = Gtk.Button(label='Compare')
    self.btnCompare.add_css_class('btn')
    self.btnCompare.add_css_class('selection-button')

    self.options.append(self.btnEncode)
    self.options.append(self.btnDecode)
    self.options.append(self.btnCompare)

    self.naviBar.attach(self.title,   0, 0, 1, 1)
    self.naviBar.attach(self.spacer,  1, 0, 1, 1)
    self.naviBar.attach(self.options, 2, 0, 1, 1)
    

    # file selection --------------------------------
    self.fileSection = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10, homogeneous=True)
    self.fileSection.set_halign(Gtk.Align.CENTER)
    self.audioSelection  = Gtk.Button(label='Select Cover File...')
    self.audioSelection.add_css_class('select-file-btn')
    self.outputSelection = Gtk.Button(label='Select Stego File...')
    self.outputSelection.add_css_class('select-file-btn')

    self.fileSection.append(self.audioSelection)
    self.fileSection.append(self.outputSelection)

    # submit button --------------------------------
    self.btnSubmit = Gtk.Button(label='Encode / Decode')
    self.btnSubmit.set_halign(Gtk.Align.CENTER)
    self.btnSubmit.add_css_class('btn')
    self.btnSubmit.add_css_class('submit-btn')

    # add elements to page --------------------------------
    self.page.append(self.naviBar)
    self.page.append(self.fileSection)
    self.page.append(self.btnSubmit)


    # add main container with all widgets --------------------------------
    self.set_child(self.page)


class MyApp(Gtk.Application):
  def __init__(self):
    super().__init__(application_id='com.example.GtkApp')

  def do_activate(self):
    win = MainWindow(application=self)
    win.present()

  def do_startup(self):
    Gtk.Application.do_startup(self)


app = MyApp()
app.run()
