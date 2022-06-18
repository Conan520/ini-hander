import os
import traceback
from typing import Dict

from configupdater import ConfigUpdater
from loguru import logger


class IniHandler:

    def __init__(self, allow_no_value=True, strict: bool = False):
        """
        :param allow_no_value: 表示是否允许为空，true:option对应的值可以为空
        :param strict: 表示强检查，主要用来检查忽略重复的option,防止报错
        """
        self.__config = ConfigUpdater(allow_no_value, strict=strict)
        self.__config.optionxform = str     # 写入保持原样，不然全会变成小写

    def check(self, path, section: str, creatable: bool = False):
        """ 检查路径是否合法，section是否存在，是否可创建
        :param path: 文件路径
        :param section: 检查ini文件中是否有这个section
        :param creatable: 表示section是否可创建，如果为false， section不存在将会报错,为true则会创建
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"{os.path.abspath(path)} not found")
        self.__config.read(path)
        if not self.__config.has_section(section):
            if not creatable:
                raise Exception(f'SectionError, No such a section named {section}')
            self.__config.add_section(section)

    def __write(self, path: str):
        with open(path, "w") as f:
            self.__config.write(f)

    def add_single_value(self, path: str, section: str, option: str, value: str, creatable: bool = False):
        # noinspection PyBroadException
        try:
            self.check(path, section, creatable)
            self.__config.set(section, option, value)
            self.__write(path)
        except Exception:
            traceback.print_exc()
        else:
            logger.info(f"modify {path} successfully")

    def add_multi_values(self, path, section, options_values: Dict[str, str], creatable: bool = False):
        # noinspection PyBroadException
        try:
            self.check(path, section, creatable)
            for option, value in options_values.items():
                self.__config.set(section, option, value)
            self.__write(path)
        except Exception:
            traceback.print_exc()
        else:
            logger.info(f"modify {path} successfully")

    def get_data(self, ini_path):
        return self.__config.read(ini_path)

