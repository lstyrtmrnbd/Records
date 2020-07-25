#!/usr/bin/env python
from tkinter import *
from tkinter import ttk
import pandas as pd
import numpy as np


def main():   
        
        root = Tk()
        root.geometry('410x90')
        root.title("Record Cataloguer")

        artist = StringVar()
        album = StringVar()
        category = StringVar()
        check_value = IntVar()

        def get_and_add():
                add_to_file(artist.get(),album.get(),category.get())
                
        mainframe = ttk.Frame(root)
        artist_entry = ttk.Entry(mainframe, textvariable=artist)
        artist_label = ttk.Label(mainframe, text="Artist")
        album_entry = ttk.Entry(mainframe, textvariable=album)
        album_label = ttk.Label(mainframe, text="Album Title")

        category_entry = ttk.Combobox(mainframe, width=7, textvariable=category, state='readonly')
        
        def toggle():
                # disable/enable combobox
                if check_value.get() == 1:
                        category_entry.state(('disabled',))
                        artist_entry.state(('disabled',))
                        category.set('VA Compilation')
                        artist.set('Various Artists')
                elif check_value.get() == 0:
                        category_entry.state(('!disabled',))
                        artist_entry.state(('!disabled',))

        check_VA = ttk.Checkbutton(mainframe, text="VA release?", variable=check_value, command=toggle)
        
        category_label = ttk.Label(mainframe, text="Category")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        mainframe.columnconfigure(0, weight=1)
        mainframe.rowconfigure(0, weight=1)
        artist_label.grid(column=1, row=1, sticky=(W, E))        
        artist_entry.grid(column=2, row=1, sticky=(W, E))
        album_label.grid(column=1, row=2, sticky=(W, E))
        album_entry.grid(column=2, row=2, sticky=(W, E))
        category_label.grid(column=1, row=3, sticky=(W, E))
        category_entry.grid(column=2, row=3, sticky=(W, E))
        category_entry['values'] = ('LP - General', 'LP - Jazz', 'Collection', 'EP - 7"', 'EP - 10"', 'EP - 12"', 'Single - 7"', 'Single - 10"', 'Single 12"', 'VA Compilation')
        category_entry.bind("<<ComboboxSelected>>")
        check_VA.grid(column=3, row=1, sticky=(W, E))
        button = ttk.Button(text ="Catalog", command = get_and_add)
        button.grid(column=1, row=10, sticky=(W, E, S))

        root.mainloop()



def add_to_file(artist, album, category):
        df = pd.read_csv('Records.csv')
        # if category not in df.columns:
        #         raise RuntimeError('Invalid category')

        # Convert CSV file to a dictionary that maps categories to dictionaries
        # mapping indeces to cell names. If there is nothing in the cell, it will
        # be either '' or NaN.
        data = df.to_dict()

        print('Loaded data')
        
        # Determine whether we need to append a new row, or whether we can just
        # fill in a new colum in an existing row.
        if len(data[category]) == 0:
                need_to_append = True
        else:                       
                num_rows = max(data[category].keys())
                last_value = data[category][num_rows - 1]
                if last_value == '' or (isinstance(last_value, float) and
                                        np.isnan(last_value)):
                        need_to_append = False
                else:
                        need_to_append = True

        print('need_to_append =', need_to_append)
        
        # Do different behaviour based on whether appending a row or whether editing
        # and existing rowe
        if need_to_append:
                for cur_category in data.keys():
                        num_rows = max(data[cur_category].keys())
                        if category == cur_category:                        
                                data[cur_category][num_rows] = f'{artist} - {album}'
                        else:
                                data[cur_category][num_rows] = ''
        else:
                num_rows = max(data[category].keys())
                for index in range(num_rows):
                        cur_value = data[category][index]
                        if cur_value == '' or (isinstance(cur_value, float) and
                                               np.isnan(cur_value)):
                                data[category][index] = f'{artist} - {album}'
                                break

        # sorting function which deprioritizes NaN
        def keyfun(e):
                if isinstance(e, float):
                        return 'zzzzz'
                else:
                        return str.lower(e)

        # go through data and sort each category
        for key in data.keys():
                vals = []
                for index in range(max(data[key].keys())):
                        vals.append(data[key][index])
                vals.sort(key=keyfun)
                for index in range(len(vals)):
                        data[key][index] = vals[index]
                        
        # Write to output file
        df_out = pd.DataFrame().from_dict(data)
        df_out.to_csv('Records.csv', index=False)

        print('Wrote output file')


if __name__=="__main__":

        # add_to_file('The Ramones', 'Rocket to Russia', 'Collection')
        # add_to_file('Reagan Youth', 'A Collection of Pop Classics', 'Collection')
        main()
