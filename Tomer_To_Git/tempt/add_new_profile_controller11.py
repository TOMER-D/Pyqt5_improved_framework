import os.path

import Tomer_To_Git.Definitions.general_screen_functions as gf
from functools import partial
from DB_objects.details import Details
from DB_objects.db_manager import DataBaseVendor


# install_AddNewProfileWindow - is the main function of this controller
# this function is initialize the screen
# it connect between the buttons to the correct functions and init the screen object
def install_AddNewProfileWindow(installer, main_window):
    print("install AddNewProfileWindow")
    upload_btn = gf.get_object_by_name(main_window, "upload_btn")
    path_box = gf.get_object_by_name(main_window, "path_box")
    func = partial(install_AddNewProfileWindow_upload_btn_func, path_box)
    upload_btn.clicked.connect(func)

    add_btn = gf.get_object_by_name(main_window, "add_btn")
    func = partial(install_AddNewProfileWindow_add_btn_func, main_window)
    add_btn.clicked.connect(func)


def install_AddNewProfileWindow_upload_btn_func(path_box):
    file_path_string = gf.get_path_by_dialog()
    path_box.setText(file_path_string)


def install_AddNewProfileWindow_add_btn_func(main_window):
    name_box = gf.get_object_by_name(main_window, "name_box")
    last_name_box = gf.get_object_by_name(main_window, "last_name_box")
    id_box = gf.get_object_by_name(main_window, "id_box")
    phone_box = gf.get_object_by_name(main_window, "phone_box")
    address_box = gf.get_object_by_name(main_window, "address_box")
    city_box = gf.get_object_by_name(main_window, "city_box")
    path_box = gf.get_object_by_name(main_window, "path_box")
    ls = [name_box.toPlainText(),last_name_box.toPlainText(),id_box.toPlainText(),phone_box.toPlainText(),
          address_box.toPlainText(),city_box.toPlainText()]
    details = Details.from_list(ls)
    print(details)
    path = path_box.toPlainText()
    if not os.path.exists(path):
        print("\nthe path that you choose :\n\"" + path + "\"\nis not exist")
        return
    db = DataBaseVendor(r"../Timit_Database")
    db.add_id(details["id"],"TRAIN",details,path)

