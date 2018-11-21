def main():
    from src.model import Model
    from src.view import View
    from src.controler import Controler

    model = Model()
    view = View()
    controler = Controler(view, model)


if __name__ == "__main__":
    main()
