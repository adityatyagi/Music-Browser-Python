import sqlite3
try:
    import tkinter
except ImportError:
    import Tkinter as tkinter


conn = sqlite3.connect('music.db')


# Class Scrollbox which is inherited from the inbuilt class of tkinter -> Listbox
class Scrollbox(tkinter.Listbox):
    
    # constructor function
    def __init__(self, window, **kwargs):
        super().__init__(window, **kwargs) # accessing the constructor of the Listbox class
        
        # For the scrollbar
        self.scrollbar = tkinter.Scrollbar(window, orient=tkinter.VERTICAL, command=self.yview)

    
    def grid(self, row, column, sticky="nsw", rowspan=1, columnspan=1, **kwargs):
        super().grid(row=row, column=column, sticky=sticky, rowspan=rowspan, columnspan=columnspan, **kwargs) # the default grid function of the Listbox class
        self.scrollbar.grid(row=row, column=column, sticky='nse', rowspan=rowspan) # grid function of the scrollbar class
        self['yscrollcommand'] = self.scrollbar.set
    


# GET ALBUMS
def get_albums(event):
    lb = event.widget # http://effbot.org/tkinterbook/tkinter-events-and-bindings.htm
    index = lb.curselection()[0] # http://effbot.org/tkinterbook/listbox.htm    -> tells about the selected field by the cursor
    artis_name = lb.get(index), # returns a string

    # get the artist ID from the databse row
    artist_id = conn.execute('SELECT artists._id FROM artists WHERE artists.name=?',artis_name).fetchone() # fetch one id at a time and place it in the artist_.id variable
    alist = [] #empty list to store the artists one by one
        
     # filling the alist
    for row in conn.execute('SELECT albums.name FROM albums WHERE albums.artist=? ORDER BY albums.name', artist_id):
        print(row) #TODO remove this
        alist.append(row[0])
        
    albumLV.set(tuple(alist))
    songLV.set(('Choose an album',))


def get_songs(event):
    lb = event.widget
    index = int(lb.curselection()[0])
    album_name = lb.get(index),

    # get the albumn ID from the database row
    album_id = conn.execute('SELECT albums._id FROM albums WHERE albums.name=?', album_name).fetchone()
    alist = []
    for x in conn.execute('SELECT songs.title FROM songs WHERE songs.album=? ORDER BY songs.track', album_id):
        print(x)
        alist.append(x[0])
    
    songLV.set(tuple(alist))




mainWindow = tkinter.Tk()
mainWindow.title('Music DB Browser')
mainWindow.geometry('1024x768')

# configuring the 4 columns
mainWindow.columnconfigure(0, weight=2)
mainWindow.columnconfigure(1, weight=2)
mainWindow.columnconfigure(2, weight=2)
mainWindow.columnconfigure(3, weight=1) # this column is for the space on the right

# configuring the 4 rows
mainWindow.rowconfigure(0, weight=1)
mainWindow.rowconfigure(1, weight=5)
mainWindow.rowconfigure(2, weight=5)
mainWindow.rowconfigure(3, weight=1)


# ************ LABELS **************
tkinter.Label(mainWindow, text="Artists").grid(row=0, column=0)
tkinter.Label(mainWindow, text="Albums").grid(row=0, column=1)
tkinter.Label(mainWindow, text="Songs").grid(row=0, column=2)



# ************ LISTBOX FOR ARTISTS **************
# HERE WE WILL BE USING THE SCROLLBOX SUBCLASS OF LISTBOX CLASS OF THE TKINTER
artistList = Scrollbox(mainWindow)
artistList.grid(row=1, column=0, sticky='nsew', rowspan=2, padx=(30, 0))
artistList.config(border=2, relief='sunken')

# Populating the artist list
for artist in conn.execute('SELECT artists.name FROM artists ORDER BY artists.name'):
    artistList.insert(tkinter.END, artist[0])

artistList.bind('<<ListboxSelect>>', get_albums)


# ************ LISTBOX FOR ALBUMS **************
albumLV = tkinter.Variable(mainWindow) # whenever there is a activity in this window, the variable changes will reflect in this albumsLV variable
albumLV.set(('Choose an artist',)) # tuple

albumList = Scrollbox(mainWindow, listvariable=albumLV)
albumList.grid(row=1, column=1, sticky='nsew', rowspan=2, padx=(30, 0))
albumList.config(border=2, relief='sunken')

# Populating the albums list
albumList.bind('<<ListboxSelect>>', get_songs)




# ************ LISTBOX FOR SONGS **************
songLV = tkinter.Variable(mainWindow)
songLV.set(('Choose an album',)) # tuple

songList = Scrollbox(mainWindow, listvariable=songLV)
songList.grid(row=1, column=2, sticky='nsew', rowspan=2, padx=(30, 0))
songList.config(border=2, relief='sunken')

# Populating the songs list





# ************ MAINLOOP **************
#testlist = range(0, 100)
#albumLV.set(tuple(testlist)) # tuple() will return a tuple and then it will replace the "Choose a artist" tuple
mainWindow.mainloop()
print('Closing the database connection')
# Closed the database
conn.close()


