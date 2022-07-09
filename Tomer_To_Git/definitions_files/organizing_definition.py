import importlib
import os
import pathlib
import yaml
import datetime


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
        path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
        path += "/" + configuration["main_directories", "name@"] + "/" + configuration[
            "main_directories", "ui", "name@"]
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
        path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
        path += "/" + configuration["main_directories", "name@"] + "/" + configuration[
            "main_directories", "py", "name@"]
        GuiFolder.__init__(self, path, configuration)

    def convert_to_folder(self, controller_folder):
        """
        :type controller_folder: GuiFolderController
        :param controller_folder:
        :return:
        """
        for common_name in self.get_common_names():
            if not controller_folder.is_exist(common_name):
                controller_folder.create_file(common_name)


class GuiFolderController(GuiFolder):
    def __init__(self, configuration):
        path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
        path += "/" + configuration["main_directories", "name@"] + "/" + configuration["main_directories", "controller","name@"]
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

    def get_common_names(self):
        ls = []
        for item in os.scandir(self.real_path):
            if item.is_file():
                name = item.name# type:str
                name = name[:name.rfind("_controller")]
                ls.append(name)
        return ls

    def is_exist(self, common_name):
        ls = self.get_common_names()
        return common_name in ls

    def create_file(self, common_name):
        ds = GuiFolderController.DocumentStructure()
        main_directories = self.configuration["main_directories", "name@"]
        definitions = self.configuration["main_directories", "definitions", "name@"]
        screen_definition = self.configuration["main_directories", "definitions", "screen_definition", "name@"]
        screen_definition_classes = self.configuration["main_directories", "definitions", "screen_definition", "classes@"]
        general_screen_functions = self.configuration["main_directories", "definitions", "general_screen_functions", "name@"]
        for class_text in screen_definition_classes:
            ds.add_from([main_directories, definitions, screen_definition], class_text)
        ds.add_import([main_directories, definitions, general_screen_functions], "as gf")
        function_name = self.configuration["main_function", "additional_name","before_module_name","name@"]
        function_name += common_name
        function_name += self.configuration["main_function", "additional_name","after_module_name","name@"]
        arguments = self.configuration["main_function","arguments","list@"]
        description = self.configuration["main_function","description","name@"]
        ds.add_function(function_name=function_name,arguments=arguments,description=description)
        file = open(self.real_path + "/" + common_name + "_controller.py", "w")
        file.write(ds.to_string())
        file.close()
        return ds.to_string()

    class DocumentStructure:
        def __init__(self):
            self.imports = []
            self.froms = []
            self.functions = []

        def add_import(self, import_chain=None, after_text=""):
            self.imports.append(GuiFolderController.DocumentStructure.Import(import_chain,after_text))

        def add_from(self, from_chain=None,import_chain=None,after_text=""):
            self.froms.append(GuiFolderController.DocumentStructure.From(from_chain,import_chain,after_text))

        def add_function(self, function_name,function_as_text="pass", arguments=None, description=""):
            self.functions.append(GuiFolderController.DocumentStructure.Function
                                  (function_name, function_as_text, arguments, description))

        def to_string(self):
            string = ""
            for item in self.imports:
                string += item.to_string() + "\n"
            for item in self.froms:
                string += item.to_string() + "\n"

            string += "\n\n"
            for item in self.functions:
                string += item.to_string() + "\n"
                string += "\n\n"
            return string

        class From:
            def __init__(self, from_chain=None,import_chain=None,after_text=""):
                self.from_chain = from_chain
                self.import_chain = import_chain
                self.after_text = after_text

            def to_string(self):
                string = "from "
                if type(self.from_chain) == list:
                    string += ".".join(self.from_chain)
                else:
                    string += self.from_chain
                string += " import "
                if type(self.import_chain) == list:
                    string += ".".join(self.import_chain)
                else:
                    string += self.import_chain
                if self.after_text != "":
                    string += " " + self.after_text
                return string

        class Import:
            def __init__(self, import_chain=None, after_text=""):
                """
                :type import_path: list
                :param import_path:
                """

                self.import_chain = import_chain
                self.after_text = after_text

            def to_string(self):
                string = "import "
                if type(self.import_chain) == list:
                    string += ".".join(self.import_chain)
                else:
                    string += self.import_chain
                if self.after_text != "":
                    string += " " + self.after_text
                return string

        class Function:
            def __init__(self, function_name,function_as_text, arguments=None, description=""):
                """
                :type function_name: str
                :type arguments: list[str]
                :type description: str
                :type function_as_text: str
                :param function_name:
                :param arguments:
                :param description:
                """
                self.description = description
                self.function_name = function_name
                self.arguments = [] if arguments is None else arguments
                self.function_text = function_as_text

            def maximum_default(self, text, characters_num):
                string = "#"
                text_arr = text.split(" ")
                row_len = 2
                for word in text_arr:
                    if len(word) + row_len + 1 > characters_num:
                        row_len = len(word) + 2
                        string += "\n# " + word
                    else:
                        string += " " + word
                        row_len += len(word) + 1
                return string

            def to_string(self, description_length_line=70):
                string = self.maximum_default(self.description, description_length_line) + "\n"
                string += "def " + self.function_name + "("
                for i, argument in enumerate(self.arguments):
                    if i == 0:
                        string += argument
                    else:
                        string += ", " + argument
                string += "):\n\t"
                string += self.function_text.replace("\n", "\n\t")
                return string


class GuiFolderImages(GuiFolder):
    def __init__(self, configuration):
        path = str(pathlib.Path(__file__).parent.parent.parent.resolve())
        path += "/" + configuration["main_directories", "name@"] + "/" + configuration[
            "main_directories", "images", "name@"]
        GuiFolder.__init__(self, path, configuration)

    def get_common_names(self):
        ls = []
        for item in os.scandir(self.real_path):
            if item.is_dir():
                name = item.name  # type:str
                name = name[:name.rfind("_images")]
                ls.append(name)
        return ls

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
            if type(v) == dict:
                v = self.__create_dict(v)
            my_dict[k.strip().upper()] = v
        return my_dict

    def refresh(self):
        self.__init__(self.__file_path)

    def __getitem__(self, items):
        search = self.__main_dict
        if type(items) == str:
            return search[items]
        for item in items:
            item = item.strip().upper()
            search = search[item]
            if type(search) == str:
                break
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


class Comments:
    def __init__(self):
        self.__string = ""
        self.__line = ""
        self.__start_comment_time = None
        self.__last_comment_time = None

    def add_comment(self, comment):
        time = datetime.datetime.now()
        if self.__start_comment_time is None:
            self.__start_comment_time = time
        self.__line = comment + " --time--> " + str(time.strftime("%H:%M:%S"))
        print(self.__line)
        self.__string += self.__line + "\n"
        self.__last_comment_time = datetime.datetime.now()

    def get_last_comment(self):
        return self.__line

    def get_whole_comments(self):
        return self.__string

    def first_to_last_time(self):
        string = "first comment time : " + str(self.__start_comment_time.strftime("%H:%M:%S")) + "\n"
        string += "last comment time : " + str(self.__last_comment_time.strftime("%H:%M:%S")) + "\n"
        string += "diff time : " + str(self.__last_comment_time - self.__start_comment_time)
        return string


def main():

    comments = Comments()
    comments.add_comment("start updating")
    comments.add_comment("get definitions")

    config_path = str(pathlib.Path(__file__).parent.resolve()) + "/" + "definition.yaml"
    config = Configuration(config_path)
    controller_folder = GuiFolderController(config)
    ui_folder = GuiFolderUi(config)
    py_folder = GuiFolderPy(config)
    images_folder = GuiFolderImages(config)

    comments.add_comment("files and dirs creation")

    ui_folder.convert_to_folder(py_folder)
    py_folder.convert_to_folder(controller_folder)
    images_folder.create_folders(py_folder)

    comments.add_comment("finish updating")
    print(comments.first_to_last_time())



