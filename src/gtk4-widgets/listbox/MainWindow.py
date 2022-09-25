# -*- coding: utf-8 -*-
"""Python e GTK 4: PyGObject Gtk.ListBox()."""

import gi

gi.require_version(namespace='Gtk', version='4.0')
gi.require_version(namespace='Adw', version='1')

from gi.repository import Adw, Gio, Gtk

Adw.init()


class ExampleWindow(Gtk.ApplicationWindow):
    # Dados que serão inseridos nas linhas do listbox_2
    itens = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.set_title(title='Python e GTK 4: PyGObject Gtk.ListBox()')
        self.set_default_size(width=int(1366 / 2), height=int(768 / 2))
        self.set_size_request(width=int(1366 / 2), height=int(768 / 2))

        headerbar = Gtk.HeaderBar.new()
        self.set_titlebar(titlebar=headerbar)

        menu_button_model = Gio.Menu()
        menu_button_model.append('Preferências', 'app.preferences')

        menu_button = Gtk.MenuButton.new()
        menu_button.set_icon_name(icon_name='open-menu-symbolic')
        menu_button.set_menu_model(menu_model=menu_button_model)
        headerbar.pack_end(child=menu_button)

        vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox.set_homogeneous(homogeneous=True)
        vbox.set_margin_top(margin=12)
        vbox.set_margin_end(margin=12)
        vbox.set_margin_bottom(margin=12)
        vbox.set_margin_start(margin=12)
        self.set_child(child=vbox)

        listbox_1 = Gtk.ListBox.new()
        listbox_1.set_selection_mode(mode=Gtk.SelectionMode.NONE)
        vbox.append(child=listbox_1)

        # Loop para criar os widgets.
        for n in range(1, 4):
            row = Gtk.ListBoxRow.new()
            row.set_selectable(selectable=False)

            hbox = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            # Adicionando container na linha
            row.set_child(child=hbox)

            label = Gtk.Label.new(str=f'Linha {n}')
            label.set_margin_top(margin=6)
            label.set_margin_end(margin=6)
            label.set_margin_bottom(margin=6)
            label.set_margin_start(margin=6)
            label.set_xalign(xalign=0)
            label.set_hexpand(expand=True)
            hbox.append(child=label)

            switch = Gtk.Switch.new()
            switch.set_margin_top(margin=6)
            switch.set_margin_end(margin=6)
            switch.set_margin_bottom(margin=6)
            switch.set_margin_start(margin=6)
            hbox.append(child=switch)

            listbox_1.append(child=row)

        # Criando um segundo ListBox
        listbox_2 = Gtk.ListBox.new()

        # Definindo um sinal (evento).
        listbox_2.connect('row-activated', self._on_row_clicked)
        vbox.append(child=listbox_2)

        # Loop para criar as linhas.
        for item in self.itens:
            label = Gtk.Label.new(str=item)
            label.set_margin_top(6)
            label.set_margin_bottom(6)
            listbox_2.append(child=label)

    def _on_row_clicked(self, listbox, listboxrow):
        print(f'Clicou no {self.itens[listboxrow.get_index()]}')


class ExampleApplication(Adw.Application):

    def __init__(self):
        super().__init__(application_id='br.com.justcode.Example',
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
        print('Ação app.preferences foi ativa.')

    def exit_app(self, action, param):
        self.quit()

    def create_action(self, name, callback, shortcuts=None):
        action = Gio.SimpleAction.new(name, None)
        action.connect('activate', callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f'app.{name}', shortcuts)


if __name__ == '__main__':
    import sys

    app = ExampleApplication()
    app.run(sys.argv)
