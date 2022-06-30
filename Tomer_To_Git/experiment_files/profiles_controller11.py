from PyQt5.QtWidgets import QTableWidgetItem
import Tomer_To_Git.definitions_files.general_screen_functions as gf
from Tomer_To_Git.py_screen_files.add_new_profile import Ui_AddNewProfileWindow
from functools import partial
from DB_objects.db_manager import DataBaseVendor



def install_ProfilesWindow(installer, main_window):
    """
    :type installer: Tomer_To_Git.screen_definition.InstallerDefinition
    :param installer:
    :param main_window:
    :return:
    """

    print("install ProfilesWindow")
    # open the screen of "add new profile"
    add_new_profile_btn = gf.get_object_by_name(main_window, "addNewProfileBtn")
    func = partial(install_ProfilesWindow_add_new_profile_btn_func, installer)
    add_new_profile_btn.clicked.connect(func)

    # initialize the table according to the database
    table = gf.get_object_by_name(main_window, "tableWidget")
    table.setColumnCount(6)
    table.setHorizontalHeaderLabels(["name", "last_name", "id",
                                     "phone","address","city"])
    db = DataBaseVendor(r"../Timit_Database")
    ids = db.get_ids("TRAIN")
    table.setRowCount(len(ids))
    y_index = 0
    for id in ids:
        details = db.get_details(id, "TRAIN")
        ls = details.to_list()
        x_index = 0
        for item in ls:
            item = QTableWidgetItem(item)
            table.setItem(y_index,x_index,item)
            x_index += 1
        y_index += 1
    # example of inserting data to the table
    """
    name = "bla"
    code = "1582"
    item_name = QTableWidgetItem(name)
    item_code = QTableWidgetItem(code)
    # inserting like (y, x) coordinate, we can iterate the database
    table.setItem(0, 0, item_name)
    table.setItem(0, 1, item_code)
    """





def install_ProfilesWindow_add_new_profile_btn_func(installer):
    installer.open_window(Ui_AddNewProfileWindow)

