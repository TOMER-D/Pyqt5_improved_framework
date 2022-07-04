import os.path

from Tomer_To_Git.py_screen_files.add_new_profile import Ui_AddNewProfileWindow
from Tomer_To_Git.definitions_files.screen_definition import MyMainWindow
from Tomer_To_Git.definitions_files.screen_definition import InstallerDefinition
import Tomer_To_Git.definitions_files.general_screen_functions as gf
from functools import partial


# this is the main function, the program understand it by the name,
# please do not change the prototype of this function.
def install_main_menu_controller(installer, main_window):
	"""
	:type main_window: MyMainWindow
	:type installer: InstallerDefinition
	"""
	print("Install main_menu")
	path = "picture1.jpg"
	main_window.set_background(path)
	print(main_window.get_pictures_path())
	enter_profiles = main_window.get_object_by_name("enter_profiles")
	func = partial(btn_function, installer)
	enter_profiles.clicked.connect(func)
	print(main_window.get_pictures_path())


def btn_function(installer):
	"""
	:type installer: InstallerDefinition
	:param installer:
	:return:
	"""
	installer.open_window(Ui_AddNewProfileWindow)


	