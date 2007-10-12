import gtk

class EntryDialog:
    def enter_callback(self, widget, entry):
        print entry.get_text()
        gtk.main_quit()
    

def add_filters(dialog):
    filter = gtk.FileFilter()
    filter.set_name('Images')
    filter.add_mime_type('image/png')
    filter.add_mime_type('image/jpeg')
    filter.add_mime_type('image/gif')
    filter.add_pattern('*.png')
    filter.add_pattern('*.jpeg')
    filter.add_pattern('*.jpg')
    filter.add_pattern('*.gif')
    filter.add_pattern('*.xpm')
    dialog.add_filter(filter)
    filter = gtk.FileFilter()
    filter.set_name('All files')
    filter.add_pattern('*')
    dialog.add_filter(filter)

def open_file():
    filename = None
    dialog = gtk.FileChooserDialog('Open', None,
        gtk.FILE_CHOOSER_ACTION_OPEN,
        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
         gtk.STOCK_OPEN, gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    add_filters(dialog)
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        filename = dialog.get_filename()
    dialog.destroy()
    return filename
	
def save_file():
    filename = None
    dialog = gtk.FileChooserDialog('Save', None,
        gtk.FILE_CHOOSER_ACTION_SAVE,
        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
         gtk.STOCK_SAVE,  gtk.RESPONSE_OK))
    dialog.set_default_response(gtk.RESPONSE_OK)
    add_filters(dialog)
    response = dialog.run()
    if response == gtk.RESPONSE_OK:
        filename = dialog.get_filename()
    dialog.destroy()
    return filename

def main():
    import sys
    filename = ''
    if '-open' in sys.argv:
        filename = open_file()
    elif '-save' in sys.argv:
        filename = save_file()
    print filename

if __name__ == '__main__': main()
