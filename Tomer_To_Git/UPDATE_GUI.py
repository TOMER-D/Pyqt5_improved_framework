import os

def main():
    ui_screen_files_path = os.path.realpath("ui_screen_files")
    controller_screen_files_path = os.path.realpath("controller_screen_files")
    py_screen_files_path = os.path.realpath("py_screen_files")
    main_directory_gui_name = os.path.realpath("/").split(os.sep)[-1]
    print(main_directory_gui_name)

    ui_files = [item.name for item in os.scandir(ui_screen_files_path) if
                item.path[-2:].upper().strip() == "UI" and item.is_file()]
    controller_files = [item.name for item in os.scandir(controller_screen_files_path) if
                        item.path[-2:].upper().strip() == "PY" and item.is_file()]
    window_files = [item.name for item in os.scandir(py_screen_files_path) if
                    item.path[-2:].upper().strip() == "PY" and item.is_file()]

    print(ui_files)
    print(controller_files)
    print(window_files)

    for ui_file in ui_files:
        exist = False
        file_name = ui_file[:-3]
        for controller_file in controller_files:
            if file_name + "_controller" == controller_file[:-3]:
                exist = True
                break
        if exist:
            continue
        full_path = os.path.join(controller_screen_files_path, file_name + "_controller.py")
        new_file = open(full_path, "w")
        imports_string = "from " + str(main_directory_gui_name) + ".screen_definition import MyMainWindow\n"
        imports_string += "from " + str(main_directory_gui_name) + ".screen_definition import InstallerDefinition\n"
        imports_string += "import " + str(main_directory_gui_name) + ".general_screen_functions as gf\n"
        main_function = "\n# this is the main function, the program understand it by the name,"
        main_function += "\n# please do not change the prototype of this function."
        main_function += "\ndef install_" + file_name + "_controller(installer, main_window):\n"
        description_string = '\t"""\n'
        description_string += '\t:type main_window: MyMainWindow\n'
        description_string += '\t:type installer: InstallerDefinition\n'
        description_string += '\t"""\n'
        main_function_action = '\tprint("Install ' + file_name + '")\n\t'
        new_file.write(imports_string + main_function + description_string + main_function_action)
        new_file.close()

    for ui_file in ui_files:
        exist = False
        file_name = ui_file[:-3]
        for window_file in window_files:
            if file_name == window_file[:-3]:
                exist = True
                break
        if exist:
            continue
        ui_path = os.path.join(ui_screen_files_path, ui_file)
        py_new_path = os.path.join(py_screen_files_path, str(file_name) + ".py")
        os.system("pyuic5 -x " + str(ui_path) + " -o " + str(py_new_path))


if __name__ == '__main__':
    main()
