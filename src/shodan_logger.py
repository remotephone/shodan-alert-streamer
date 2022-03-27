import logging


logger = logging.getLogger('shodan')
logger.setLevel(logging.INFO)

fileHandler = logging.FileHandler('shodan.log')
fileHandler.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)


logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)

