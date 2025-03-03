import configparser

def getConfigParser():
    config = configparser.ConfigParser()
    config.read('utilities/properties.ini')
    return config