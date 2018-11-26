def main():
    from src.model import Model
    from src.view import View
    from src.controler import Controler

    model = Model()
    view = View(300, 300)
    Controler(view, model)
    view.mainloop()


if __name__ == "__main__":
    main()
