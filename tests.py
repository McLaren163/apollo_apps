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


if __name__ == "__main__":
    # test_json()
    test_inputs()
