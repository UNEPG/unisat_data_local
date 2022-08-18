import os
import logging


def install_pkg(pkg_name: str):
    installed_flag = False
    num = int(1)
    while installed_flag is False:
        logging.info("Installing %s, trying %dth time" % (pkg_name, num))
        num += 1
        if num > 10:
            logging.error("Installation failed")
            break
        try:
            exec('import %s' % pkg_name)
            installed_flag = True
        except ImportError:
            os.system('pip3 install -U %s' % pkg_name)
