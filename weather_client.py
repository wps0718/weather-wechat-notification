import requests
from config import config
import logging
from typing import Optional, List, Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class WeatherClient:
    """和风天气API客户端，用于获取和解析天气数据"""

    def __init__(self):
        """初始化客户端，从配置文件加载API参数"""
        self.api_key = config.get('weather_api', 'key')
        self.location = config.get('weather_api', 'location')
        self.url_now = config.get('weather_api', 'url')
        self.url_forecast = config.get('weather_api', 'url_forecast')

        self.realtime_weather: Optional[Dict[str, Any]] = None
        self.forecast_weather: Optional[List[Dict[str, Any]]] = None

    def fetch_weather_data(self) -> bool:
        """
        从和风天气API获取最新的实时和预报数据

        Returns:
            bool: 数据获取成功返回 True，否则返回 False
        """
        try:
            # 1. 获取实时天气
            params_now = {'key': self.api_key, 'location': self.location}
            response_now = requests.get(self.url_now, params=params_now, timeout=10)
            response_now.raise_for_status()
            result_now = response_now.json()

            if result_now.get('code') != '200':
                logger.error(f"实时天气API请求失败: {result_now.get('msg', '未知错误')}")
                return False
            self.realtime_weather = result_now.get('now', {})

            # 2. 获取3天预报
            params_forecast = {'key': self.api_key, 'location': self.location}
            response_forecast = requests.get(self.url_forecast, params=params_forecast, timeout=10)
            response_forecast.raise_for_status()
            result_forecast = response_forecast.json()

            if result_forecast.get('code') != '200':
                logger.error(f"天气预报API请求失败: {result_forecast.get('msg', '未知错误')}")
                return False
            self.forecast_weather = result_forecast.get('daily', [])

            logger.info("天气数据获取成功")
            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"获取天气数据时网络请求失败: {e}")
            self.realtime_weather = None
            self.forecast_weather = None
            return False
        except Exception as e:
            logger.error(f"获取天气数据时发生未知错误: {e}")
            self.realtime_weather = None
            self.forecast_weather = None
            return False

    def get_temperature_range(self) -> str:
        """获取今天的温度范围"""
        if not self.forecast_weather:
            return "未知"
        today = self.forecast_weather[0]
        return f"{today.get('tempMin', '?')}℃ ~ {today.get('tempMax', '?')}℃"

    def get_weather_condition(self) -> str:
        """获取天气状况"""
        if not self.realtime_weather:
            return "未知"
        return self.realtime_weather.get('text', "未知")

    def get_wind_info(self) -> str:
        """获取风力风向"""
        if not self.realtime_weather:
            return "未知"
        wind_dir = self.realtime_weather.get('windDir', "未知")
        wind_scale = self.realtime_weather.get('windScale', "未知")
        return f"{wind_dir} {wind_scale}级"

    def get_uv_index(self) -> Optional[int]:
        """获取紫外线指数数值"""
        if not self.forecast_weather:
            return None
        today = self.forecast_weather[0]
        uv_index_str = today.get('uvIndex')
        if uv_index_str:
            try:
                return int(uv_index_str)
            except (ValueError, TypeError):
                return None
        return None

    def get_precipitation(self) -> float:
        """获取实时降水量"""
        if not self.realtime_weather:
            return 0.0
        precip_str = self.realtime_weather.get('precip', "0.0")
        try:
            return float(precip_str)
        except (ValueError, TypeError):
            return 0.0