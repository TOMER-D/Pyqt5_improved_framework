from functools import partial

from Tomer_To_Git.py_screen_files.profiles import Ui_ProfilesWindow
from Tomer_To_Git.py_screen_files.speaker_distribution import Ui_SpeakerDistributionWindow
import Tomer_To_Git.Definitions.general_screen_functions as gf



def install_MainWindow(installer, main_window):
    """
    :type installer: InstallerDefinition
    :param installer:
    :param main_window:
    :return:
    """

    print("install MainWindow")
    main_window.setStyleSheet(
        "#" + str(
            main_window.objectName()) + " { border-image: url(../GUI/images/background.png) 0 0 0 0 stretch stretch; }")

    # connect the btn of "profiles" to open the profiles window
    enter_profiles = gf.get_object_by_name(main_window, "enter_profiles")
    func = partial(install_MainWindow_enter_profiles_func, installer)
    enter_profiles.clicked.connect(func)

    # connect the btn of "upload record" to import file from the computer
    # and insert the path to the "path box"
    upload_record = gf.get_object_by_name(main_window, "upload_record")
    path_box = gf.get_object_by_name(main_window, "path_box")
    func = partial(install_MainWindow_upload_record_func, path_box=path_box, installer=installer)
    upload_record.clicked.connect(func)

    # connect the btn of "identify" to open and use the speaker distribution
    identify_btn = gf.get_object_by_name(main_window, "identify_btn")
    func = partial(install_MainWindow_identify_btn_func, installer)
    identify_btn.clicked.connect(func)


def install_MainWindow_enter_profiles_func(installer):
    """
    :type installer: InstallerDefinition
    :param installer:
    :return:
    """
    installer.open_window(Ui_ProfilesWindow)


def install_MainWindow_identify_btn_func(installer):
    """
    :type installer: InstallerDefinition
    :param installer:
    :return:
    """
    installer.open_window(Ui_SpeakerDistributionWindow)


def install_MainWindow_upload_record_func(path_box, installer):
    """
    :type installer: InstallerDefinition
    :param path_box:
    :param installer:
    :return:
    """
    file_path_string = gf.get_path_by_dialog()
    path_box.setText(file_path_string)




