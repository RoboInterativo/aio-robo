import pathlib
import yaml
from yaml import load, dump
from yaml import Loader, Dumper

base_dir = pathlib.Path(__file__).parent.parent
config_path = base_dir / '../robo.yaml'


def get_config(path):
    stream = open(path, 'r')
    return load(stream, Loader=Loader) 


config = get_config(config_path)
