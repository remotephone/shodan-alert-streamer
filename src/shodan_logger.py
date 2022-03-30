import logging


formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


logger = logging.getLogger("shodan")
logger.setLevel(logging.INFO)

fileHandler = logging.FileHandler("shodan.log")
fileHandler.setLevel(logging.INFO)
fileHandler.setFormatter(formatter)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)
consoleHandler.setFormatter(formatter)


logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)
