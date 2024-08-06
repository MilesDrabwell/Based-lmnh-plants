from datetime import datetime


def read_txt():
    with open("json_example.txt", "r") as f:
        return f.read()


jsons = read_txt()
print(jsons)
