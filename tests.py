import json
import tkinter as tk
from src.widgets import Input, InputsBlock


def test_json():
    conf = None
    with open('view_config.json') as file:
        conf = json.load(file)
    print(conf['files']['icon'])
    print(conf['fonts']['gui'])


def test_inputs():
    root = tk.Tk()
    w = Input(root, 'Label', width=17)
    w.pack(fill=tk.X)
    w = Input(root, 'Label', width=17)
    w.pack(fill=tk.X)
    bl = InputsBlock(root, 17, None, None, {'name': 'Block',
                                            'columns': 2, 'inputs': (('Inp1', None), ('Inp2', None))})
    bl.pack()
    root.mainloop()


def test_model_map():
    from main import TYPE_MAP_FILE
    from src.model import ModelMap

    mm = ModelMap(TYPE_MAP_FILE)

    print(mm.getType(4100, 1900))
    print(mm.getType(7800, 1900))
    print(mm.getType(4100, 3500))


if __name__ == "__main__":
    # test_json()
    # test_inputs()
    test_model_map()
