import os.path

from Tomer_To_Git.definitions_files.screen_definition import MyMainWindow
from Tomer_To_Git.definitions_files.screen_definition import InstallerDefinition
import Tomer_To_Git.definitions_files.general_screen_functions as gf


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


	