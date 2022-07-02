import importlib
import os
import yaml


class GuiFolder:
    def __init__(self, path, configuration):
        self.configuration = configuration
        self.real_path = os.path.realpath(path)
        self.name = str(self.real_path).split(os.sep)[-1]
        if not os.path.exists(self.real_path):
            os.mkdir(self.real_path)

    def get_common_names(self):
        ls = []
        for item in os.scandir(self.real_path):
            if item.is_file():
                name = item.name # type:str
                name = name[:name.rfind(".")]
                ls.append(name)
        return ls

    def get_file_names(self):
        return [item.name for item in os.scandir(self.real_path) if item.is_file()]

    def get_file_paths(self):
        return [item.path for item in os.scandir(self.real_path) if item.is_file()]

    def get_dirs_names(self):
        return [item.name for item in os.scandir(self.real_path) if item.is_dir()]

    def _get_module(self, module_name):
        files_names = self.get_file_names()
        files_path = self.get_file_paths()
        for i in range(len(files_names)):
            if files_names[i] == module_name:
                spec = importlib.util.spec_from_file_location(files_names[i], files_path[i])
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                return module

    def __str__(self):
        return self.real_path


class GuiFolderUi(GuiFolder):
    def __init__(self, configuration):
        path = "../" + configuration["main_directories", "ui"]
        GuiFolder.__init__(self, path, configuration)

    def convert_to_folder(self, py_folder):
        for file_name in self.get_ui_file_names(False):
            py_new_path = str(py_folder) + os.sep + file_name + ".py"
            file_path = self.real_path + os.sep + file_name + ".ui"
            os.system("pyuic5 -x " + str(file_path) + " -o " + str(py_new_path))

    def get_ui_file_names(self, suffix=True):
        ls = []
        for file_name in self.get_file_names():
            if file_name[(len(file_name)-2):].upper() == "UI":
                if suffix:
                    ls.append(file_name)
                else:
                    ls.append(file_name[:-3])
        return ls


class GuiFolderPy(GuiFolder):
    def __init__(self, configuration):
        path = "../" + configuration["main_directories", "py"]
        GuiFolder.__init__(self, path, configuration)

    def convert_to_folder(self, controller_folder):
        """
        :type controller_folder: GuiFolderController
        :param controller_folder:
        :return:
        """
        pass


class GuiFolderController(GuiFolder):
    def __init__(self, configuration):
        path = "../" + configuration["main_directories", "controller"]
        GuiFolder.__init__(self, path, configuration)

    def main_function_name(self, module_name):
        before_string = self.configuration["main_function", "name", "before_module_name"]
        after_string = self.configuration["main_function", "name", "after_module_name"]
        return before_string + module_name + after_string

    def get_function(self, module_name, function_name):
        module = self._get_module(module_name)
        return getattr(module, str(function_name))

    def get_main_function(self, module_name):
        module = self._get_module(module_name)
        if module_name[len(module_name)-2:].upper() == "PY":
            function_name = self.main_function_name(module_name)
            return getattr(module, str(function_name))

    def create_main_functions_dict(self, suffix=False):
        files = self.get_file_names()
        ls = dict([])
        for file in files:
            if suffix:
                ls[file] = self.get_main_function(file)
            else:
                ls[file[:-3]] = self.get_main_function(file)
        return ls

    def create_file(self, common_name):
        controller_structure = ""
        print(config)
        ls = config["controller_structure","imports","from","DEFINITIONS_FILES","SCREEN_DEFINITION"]
        for item in ls:
            controller_structure += "from " + config["gui_root_dir_name"]
            controller_structure += "." + config["main_directories", "definitions_files"]
            controller_structure += "." + config["SCREEN_DEFINITION"] + " import " + item + "\n"
        additional_import = config["controller_structure","imports","import","DEFINITIONS_FILES"]
        controller_structure += "import " + config["gui_root_dir_name"] + "." + config["main_directories", "DEFINITIONS"] + \
                                "." + additional_import + "\n"

        print(controller_structure)

class GuiFolderImages(GuiFolder):
    def __init__(self, configuration):
        path = "../" + configuration["main_directories", "images"]
        GuiFolder.__init__(self, path, configuration)

    def create_folders(self, gui_folder):
        """
        :type gui_folder: GuiFolder
        :param gui_folder:
        :return:
        """
        names = gui_folder.get_common_names()
        for name in names:
            name = name + "_images"
            if name not in self.get_dirs_names():
                os.mkdir(os.path.join(self.real_path, name))


# this is an object that analyzed the data in the yaml, its goal is to give us the
# details in the most organized way.
# there are 2 sign in the yaml that we supposed to understand - the # and the $.
# the # is the way to change the *key* to value of the original word.
# the $ is the way to change the *key and the value* of the original word.
# both signs use of the words that define above.


class Configuration:
    # this configuration is not sensitive to letter type for keys
    def __init__(self, file_path):
        self.__file_path = file_path
        filename = open(self.__file_path, "r")
        self.__main_dict = dict()
        self.__first_column = dict()
        docs = yaml.load_all(filename, Loader=yaml.Loader)
        for doc in docs:
            self.__main_dict.update(self.__create_dict(doc))
        filename.close()

    def __create_dict(self, dic):
        my_dict = dict([])
        for k, v in dic.items():
            arr = k.split("#")
            if len(arr) > 1:
                arr = arr[:-1]
                k = self[arr]
            arr = k.split('$')
            if len(arr) > 1:
                arr = arr[:-1]
                v = self[arr]
                k = arr[-1]
            if type(v) == dict:
                v = self.__create_dict(v)
            my_dict[k.strip().upper()] = v
        return my_dict

    def refresh(self):
        self.__init__(self.__file_path)

    def __set_dictionary(self):
        pass

    def __getitem__(self, items):
        search = self.__main_dict
        if len(items) == 1 and type(search[items]) == str:
            return search[items]
        for item in items:
            item = item.strip().upper()
            search = search[item]
        return search

    def __str__(self):
        return self.__inter_dict(self.__main_dict, 0)

    def __inter_dict(self, dic, tab_count):
        string = "\n"
        for k, v in dic.items():
            string += "\t"*tab_count + k + ": "
            if type(v) == dict:
                string += self.__inter_dict(v, tab_count+1)
            else:
                string += str(v)
                string += "\n"
        return string


if __name__ == '__main__':
    config = Configuration("definition.yaml")
    controller_folder = GuiFolderController(config)
    ui_folder = GuiFolderUi(config)
    py_folder = GuiFolderPy(config)
    images_folder = GuiFolderImages(config)
    ui_folder.convert_to_folder(py_folder)
    py_folder.convert_to_folder(controller_folder)
    controller_folder.create_file("message")
    images_folder.create_folders(py_folder)
    # print(ui_folder.get_common_names())


