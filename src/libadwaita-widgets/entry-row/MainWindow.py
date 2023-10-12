# -*- coding: utf-8 -*-
"""Python e GTK: PyGObject Adw.EntryRow()."""



import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class ExampleWindow(Adw.ApplicationWindow):
    items = ['Title 01', 'Title 02', 'Title 03', 'Title 04', 'Title 05']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(
            title='Python e GTK: PyGObject Adw.EntryRow()',
        )
        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 2), height=int(768 / 2))

        adw_toast_overlay = Adw.ToastOverlay.new()
        self.set_content(content=adw_toast_overlay)

        adw_toolbar_view = Adw.ToolbarView.new()
        adw_toast_overlay.set_child(child=adw_toolbar_view)

        adw_header_bar = Adw.HeaderBar.new()
        adw_toolbar_view.add_top_bar(widget=adw_header_bar)

        menu_button_model = Gio.Menu()
        menu_button_model.append(
            label='Preferences',
            detailed_action='app.preferences',
        )

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        adw_header_bar.pack_end(child=menu_button)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        adw_toolbar_view.set_content(content=vbox)

        self.list_box = Gtk.ListBox.new()
        self.list_box.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        self.list_box.add_css_class(css_class='boxed-list')
        vbox.append(child=self.list_box)

        for item in self.items:
            icon = Gtk.Image.new_from_icon_name(
                icon_name='accessories-text-editor-symbolic'
            )

            adw_entry_row = Adw.EntryRow.new()
            adw_entry_row.set_title(title=item)
            adw_entry_row.add_prefix(widget=icon)
            adw_entry_row.set_show_apply_button(show_apply_button=True)
            adw_entry_row.set_activates_default(activates=True)
            adw_entry_row.connect('apply', self.on_apply_button_pressed)
            self.list_box.append(child=adw_entry_row)

    def on_apply_button_pressed(self, entry_row):
        print(f'Entry value = {entry_row.get_text()}')


class ExampleApplication(Adw.Application):

    def __init__(self):
        super().__init__(application_id='br.com.justcode.PyGObject',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.create_action('quit', self.exit_app, ['<primary>q'])
        self.create_action('preferences', self.on_preferences_action)

    def do_activate(self):
        win = self.props.active_window
        if not win:
            win = ExampleWindow(application=self)
        win.present()

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

    def on_preferences_action(self, action, param):
        print('Action `app.preferences` was active.')

    def exit_app(self, action, param):
        self.quit()

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name=name, parameter_type=None)
        action.connect('activate', callback)
        self.add_action(action=action)
        if shortcuts:
            self.set_accels_for_action(
                detailed_action_name=f'app.{name}',
                accels=shortcuts,
            )


if __name__ == '__main__':
    import sys

    app = ExampleApplication()
    app.run(sys.argv)
