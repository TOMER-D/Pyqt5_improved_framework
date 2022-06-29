import os

from PyQt5.QtWidgets import QMainWindow
import importlib.util


# this object aim is to route the screen object to the correct install file.
# and save all the screen that open, for protecting the screens from the garbage collector
# - because of those reasons the screen has to open from special method that existing in the object.
# - and called "open_window"

class InstallerDefinition:
    def __init__(self,multi_windows=True, parallel_screens=True):
        # "screens_to_init_function" - it's a dictionary that connect between the screen to specific init function
        self.multi_windows = multi_windows
        self.parallel_screens = parallel_screens
        self.__screens = []
        self.screens_manager = ScreensManager()

        controllers_path = [controller_file.path for controller_file in os.scandir("./controller_screen_files") if controller_file.is_file()]
        controllers_names = [controller_file.name[:-3] for controller_file in os.scandir("./controller_screen_files") if controller_file.is_file()]
        files_names = [controller_file.name[:-14] for controller_file in os.scandir("./controller_screen_files") if controller_file.is_file()]

        self.__name_main_functions = dict([])
        for i in range(len(controllers_path)):
            spec = importlib.util.spec_from_file_location(controllers_names[i], controllers_path[i])
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            self.__name_main_functions[files_names[i]] = getattr(module,"install_" + str(files_names[i]) + "_controller")

    def __install_definition(self, main_window, ui_object, multi_windows, parallel_screens):
        """
        :param multi_windows:
        :type main_window: MyMainWindow
        :param main_window:
        :return:
        """
        file_name = str(ui_object.__module__).split(".")[-1]
        self.__screens.append(main_window)
        self.screens_manager.add_screen(main_window.local_name(), main_window, multi_windows, parallel_screens)
        func = self.__name_main_functions[file_name]
        #func = self.__screens_to_init_function[main_window.objectName()]
        func(self, main_window)

    def open_window(self, ui_object, multi_windows=None, parallel_screens=None):
        if parallel_screens is None:
            parallel_screens = self.parallel_screens
        if multi_windows is None:
            multi_windows = self.multi_windows
        main_window_name = self.screens_manager.get_new_name(ui_object, multi_windows)
        if not multi_windows:
            if self.screens_manager.screen_order.is_exist(main_window_name):
                main_window = self.screens_manager[main_window_name]["#SCREEN OBJECT"]  # type: MyMainWindow
                main_window.activateWindow()
                return
        Window = MyMainWindow(main_window_name, self.screens_manager)
        ui = ui_object()
        ui.setupUi(Window)
        self.__install_definition(Window, ui_object, multi_windows, parallel_screens)
        if len(self.screens_manager.screen_order) > 1:
            prev_window_name = self.screens_manager.screen_order.order_list[-2]
            prev_parallel_screen = self.screens_manager[prev_window_name]["#PARALLEL SCREENS"]
            if not prev_parallel_screen:
                current_window = self.screens_manager[prev_window_name]["#SCREEN OBJECT"]
                current_window.hide()
        print("'" + str(main_window_name) + "'", "is opening")
        Window.show()

    def __str__(self):
        return str(self.screens_manager)

    def get_data(self, screen_name, key):
        return self.screens_manager[screen_name][key]

    def set_data(self, screen_name, key, value):
        self.screens_manager[screen_name][key] = value

class MyMainWindow(QMainWindow):
    def __init__(self, LocalName, screens_manager):
        """
        :type screens_manager: ScreensManager
        :param LocalName:
        :param screens_manager:
        """
        QMainWindow.__init__(self)
        self.__LocalName = LocalName
        self.__screens_manager = screens_manager
        self.__end_functions = []

    # use partial from functools
    def add_end_function(self, func):
        self.__end_functions.append(func)

    def closeEvent(self, event):
        for func in self.__end_functions:
            func()
        self.__screens_manager.delete_screen(self.local_name())
        print("'" + str(self.__LocalName) + "'", "is closing")
        event.accept()

    def get_object_by_name(self, object_name):
        for child in self.centralWidget().children():
            if child.objectName() == object_name:
                return child
        raise Exception("there isn't an object called '" + str(object_name) + "' in " + str(self.__LocalName))

    def local_name(self):
        return self.__LocalName


class ScreensManager:
    def __init__(self):
        self.current_screen = None
        self.general_dict = dict([])
        self._screens_dict = dict([])
        self.screen_order = ScreensManager.ScreensOrder()

    def add_screen(self, screen_name, screen_object, multi_windows, parallel_screens, sensitive_to_letter_types=False):
        self.current_screen = screen_name
        screen_definition = ScreensManager.ScreenDict(sensitive_to_letter_types)
        self.screen_order.append(screen_name,screen_object)
        screen_definition["#SCREEN NAME"] = screen_name
        screen_definition["#SCREEN OBJECT"] = screen_object
        screen_definition["#PREVIOUS SCREEN"] = (self.screen_order[-2][0] if len(self.screen_order) > 1 else None)
        screen_definition["#MULTI WINDOWS"] = multi_windows
        screen_definition["#PARALLEL SCREENS"] = parallel_screens
        self._screens_dict[screen_name] = screen_definition

    def get_new_name(self, obj, multi_windows):
        object_name = str(obj)
        object_name = object_name[8:-2]
        if not multi_windows:
            return object_name
        ls = list(self._screens_dict.keys()) # type: list[str]
        max_index = 0
        for item in ls:
            if item[:len(object_name)] == object_name:
                name = item.split(".")[-1]
                index = int(name.split("#")[-1])
                if index > max_index:
                    max_index = index
        return object_name + "#" + str(max_index+1)

    def delete_screen(self, screen_name):
        if len(self.screen_order) > 1:
            prev_name = self.screen_order.order_list[-2]
            parallel_screen = self._screens_dict[prev_name]["#PARALLEL SCREENS"]
            if not parallel_screen:
                prev_screen = self._screens_dict[prev_name]["#SCREEN OBJECT"]
                prev_screen.show()
        self.screen_order.delete_screen(screen_name)
        del self._screens_dict[screen_name]

    def __getitem__(self, item):
        if len(self._screens_dict) == 0:
            return None
        return self._screens_dict[item]

    def __str__(self):
        string = str(self.general_dict)
        string += "\n" + str(self._screens_dict)
        string += "\n" + str(self.screen_order)
        string += "\n"
        return string

    def __repr__(self):
        return self.__str__()

    class ScreensOrder:
        def __init__(self):
            self.order_list = []
            self.name_to_object = dict([])

        def append(self, window_name, main_window):
            self.name_to_object[window_name] = main_window
            self.order_list.append(window_name)

        def delete_screen(self, screen_name):
            self.order_list.remove(screen_name)
            del self.name_to_object[screen_name]

        def pop(self, index):
            window_name = self.order_list.pop(index)
            obj = self.name_to_object[window_name]
            del self.name_to_object[window_name]
            return window_name, obj

        def is_exist(self, window_name):
            return window_name in self.order_list

        def __len__(self):
            return len(self.order_list)

        def __getitem__(self, index):
            window_name = self.order_list[index]
            obj = self.name_to_object[window_name]
            return window_name, obj

        def __str__(self):
            string = self.order_list.__str__() + "\n"
            string += "count = " + str(len(self.order_list))
            string += "\n"
            return string

    class ScreenDict:
        def __init__(self, sensitive_to_letter_types=False):
            """
            :type sensitive_to_letter_types:bool
            :type screen_name: str
            :param screen_name:
            :param sensitive_to_letter_types:
            """
            self.sensitive_to_letter_types = sensitive_to_letter_types
            self.values_dict = dict([])

        def __key_transform(self, key):
            if not self.sensitive_to_letter_types:
                return key.upper().strip()

        def change_anyway(self, key, value):
            key = self.__key_transform(key)
            self.values_dict[key] = value

        def __setitem__(self, key, value):
            key = self.__key_transform(key)
            if key[0] == "#":
                if key in self.values_dict:
                    raise Exception("There is not an option to change value for :'"
                                    + key + "', because it defined as unchangeable")
            self.values_dict[key] = value

        def __getitem__(self, item):
            key = self.__key_transform(item)
            return self.values_dict[key]

        def __str__(self):
            string = "sensitive to letter types : " + str(self.sensitive_to_letter_types) + "\n"
            for key, value in enumerate(self.values_dict.items()):
                string += "key :'" + str(key) + "', value = '" + str(value) + "'\n"
            return string

if __name__ == '__main__':
    for i, val in enumerate(os.scandir("../controller_screen_files")):
        print("i :", i, ", val :", val)
