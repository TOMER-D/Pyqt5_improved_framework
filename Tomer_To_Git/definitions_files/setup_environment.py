import os
from os.path import exists
import organizing_definition as od


class SetupEnvironment:
    @staticmethod
    def install_pyqt(num):
        os.system("pip install pyqt" + str(num))
        os.system("pip install pyqt" + str(num) + " pyqt" + str(num) + "-tools")

    @staticmethod
    def setup_environment(num):
        od.main()


if __name__ == '__main__':
    se = SetupEnvironment()
    se.install_pyqt(6)
