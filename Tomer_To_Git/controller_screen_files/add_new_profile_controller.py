from Tomer_To_Git.definitions_files.screen_definition import MyMainWindow
from Tomer_To_Git.definitions_files.screen_definition import InstallerDefinition
import Tomer_To_Git.definitions_files.general_screen_functions as gf

# this is the main function, the program understand it by the name,
# please do not change the prototype of this function.
def install_add_new_profile_controller(installer, main_window):
	"""
	:type main_window: MyMainWindow
	:type installer: InstallerDefinition
	"""
	print("Install add_new_profile")
	print("#PREVIOUS SCREEN :", main_window["#PREVIOUS SCREEN"])
	