import sqlite3
try:
    import tkinter
except ImportError:
    import Tkinter as tkinter


conn = sqlite3.connect('music.db')
cursor = conn.cursor()
for i in cursor.execute('SELECT * from albums'):
    print(i)
cursor.close()
conn.close()