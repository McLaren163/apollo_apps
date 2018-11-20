def main():
    import json
    import os

    config = None

    configFileName = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(configFileName) as file:
        config = json.loads(file.read())

    print(config)
    print(type(config))
    print(config['main']['font'])


if __name__ == "__main__":
    main()
