import json


def test_json():
    conf = None
    with open('view_config.json') as file:
        conf = json.load(file)
    print(conf['files']['icon'])


if __name__ == "__main__":
    test_json()
