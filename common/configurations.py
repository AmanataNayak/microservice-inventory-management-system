import configparser
import os

class Config:
    def __init__(self, filename="url.properties"):
        self.parser = configparser.ConfigParser()
        self.parser.read(os.path.join(os.getcwd(), "common", filename))

    def __getitem__(self, attributes):
        return self.parser[attributes]

config = Config()