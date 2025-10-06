import configparser
from typing import Dict, Optional


class Config:
    """配置文件处理类，负责读取和解析配置信息"""

    def __init__(self, config_path: str = "config.ini"):
        """
        初始化配置解析器并加载配置文件

        Args:
            config_path: 配置文件路径，默认为 "config.ini"
        """
        self.config = configparser.ConfigParser()
        self.config.read(config_path, encoding="utf-8")

    def get(self, section: str, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        获取指定配置项的原始字符串值

        Args:
            section: 配置节名称
            key: 配置项名称
            default: 当配置项不存在时返回的默认值

        Returns:
            配置项的字符串值或默认值
        """
        return self.config.get(section, key, fallback=default)

    def get_int(self, section: str, key: str, default: Optional[int] = None) -> Optional[int]:
        """获取整数类型的配置值"""
        value = self.get(section, key)
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default

    def get_boolean(self, section: str, key: str, default: Optional[bool] = None) -> Optional[bool]:
        """获取布尔类型的配置值"""
        return self.config.getboolean(section, key, fallback=default)

    def get_section(self, section: str) -> Dict[str, str]:
        """
        获取整个配置节的内容

        Args:
            section: 配置节名称

        Returns:
            配置节的所有配置项组成的字典
        """
        if self.config.has_section(section):
            return dict(self.config.items(section))
        return {}


# 单例模式的配置实例
config = Config()