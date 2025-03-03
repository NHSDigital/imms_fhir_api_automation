import configparser

def getConfigParser():
    configUrl = configparser.ConfigParser()
    configUrl.read('utilities\properties.ini')
    return configUrl