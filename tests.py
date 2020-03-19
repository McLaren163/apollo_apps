import os
import sys
import json
import tkinter as tk


def test_json():
    conf = None
    with open('view_config.json') as file:
        conf = json.load(file)
    print(conf['files']['icon'])
    print(conf['fonts']['gui'])


def test_model_map():
    from main import TYPE_MAP_FILE
    from src.model import ModelMap

    mm = ModelMap(TYPE_MAP_FILE)

    print(mm.getType(4100, 1900))
    print(mm.getType(7800, 1900))
    print(mm.getType(4100, 3500))


def callback(event):
    print(event)


def test_events():
    root = tk.Tk()
    entry = tk.Entry(root)
    entry.bind('<Return>', callback)
    entry.bind('<FocusOut>', callback)
    entry.pack()
    tk.Entry(root).pack()
    root.mainloop()

def test_cwd():
    print(os.getcwd())
    print(sys.argv[0])

    CWD = os.path.abspath(os.path.dirname(__file__))
    os.chdir(CWD)
    print(os.getcwd())

def test_sketches():
    sketches = (
        {'a': [2,],
        'b': [3,],
        'filename': 'name1'},
        {'a': [4,],
        'b': [5,],
        'filename': 'name2'}
    )
    filter_ = {
        'a': 2,
        'b': 5
    }
    path = 'dir'
    from src.sketches import Sketches
    sk = Sketches(sketches, path)
    p = sk.get_filepath(filter_)
    print(p)

if __name__ == "__main__":
    # test_json()
    # test_inputs()
    # test_model_map()
    # test_events()
    # test_cwd()
    test_sketches()