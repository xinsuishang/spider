import logging
import os

from config import PROJECT, ROOT


class Log():

    def info(filename, message):
        path = os.path.join(ROOT, 'log', PROJECT)
        try:
            os.makedirs(path)
        except FileExistsError:
            pass
        path = os.path.join(path, filename + '.log')
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', 
                            filename=path)
        logging.info("%s : %s" %(filename, message))


if __name__ == "__main__":
    Log.info('test', 'this is test')
