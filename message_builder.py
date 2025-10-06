from typing import Dict, List
from weather_client import WeatherClient
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MessageBuilder:
    """消息构建器，负责根据天气数据生成个性化提示信息"""

    def __init__(self, weather_client: WeatherClient):
        self.weather_client = weather_client

    def get_greeting(self) -> str:
        """根据当前时间生成问候语"""
        hour = datetime.now().hour
        if 5 <= hour < 9:
            return "早上好呀！新的一天开始了，元气满满哦~"
        elif 9 <= hour < 12:
            return "上午好呀！工作学习也要记得适当休息哦~"
        elif 12 <= hour < 18:
            return "下午好呀！注意劳逸结合，保持高效状态~"
        else:
            return "晚上好呀！忙碌了一天，好好放松一下吧~"

    def get_temperature_tips(self) -> str:
        """根据温度范围生成提示"""
        temp_range = self.weather_client.get_temperature_range()
        if temp_range == "未知":
            return "今日温度信息获取失败"

        try:
            min_temp_str, max_temp_str = temp_range.split(" ~ ")
            min_temp = float(min_temp_str.replace("℃", ""))
            max_temp = float(max_temp_str.replace("℃", ""))
        except:
            return f"今日气温: {temp_range}，请注意根据实际情况增减衣物~"

        tip = f"今日气温: {temp_range}\n"
        if max_temp >= 30:
            tip += "天气炎热，注意防暑降温，多补充水分哦~"
        elif max_temp <= 10:
            tip += "天气寒冷，注意保暖，出门记得多穿点~"
        elif (max_temp - min_temp) >= 8:
            tip += "昼夜温差较大，注意适时增减衣物，预防感冒~"
        else:
            tip += "温度适宜，体感舒适，祝你一天好心情~"
        return tip

    def get_precipitation_tips(self) -> str:
        """根据实时降水生成提示"""
        precip = self.weather_client.get_precipitation()
        if precip > 0:
            return f"当前有降水(约{precip}mm)，出门请记得带好雨具哦~"
        return "当前无降水，放心出行~"

    def get_weather_condition_tips(self) -> str:
        """根据天气状况生成提示"""
        condition = self.weather_client.get_weather_condition().lower()
        if condition == "未知":
            return "天气状况信息获取失败"

        tips = []
        if "雨" in condition: tips.append("今天有雨，出门请记得带伞，雨天路滑注意安全。")
        if "雪" in condition: tips.append("今天有雪，注意防寒保暖，雪天路滑，出行请格外小心。")
        if "晴" in condition: tips.append("天气晴朗，阳光明媚，适合户外活动，也要注意防晒哦。")
        if "阴" in condition: tips.append("今天天气阴沉，但别让天气影响心情，要开心呀。")
        if "雾" in condition or "霾" in condition: tips.append("今天有雾或霾，能见度较低，外出请注意安全，可佩戴口罩。")
        if "风" in condition: tips.append("今天风力较大，注意防风，保护好自己不要着凉。")

        return "\n".join(tips) if tips else f"今天天气{condition}，祝你事事顺心~"

    def get_uv_tips(self) -> str:
        """根据紫外线指数生成提示"""
        uv_index = self.weather_client.get_uv_index()
        if uv_index is None:
            return "紫外线指数信息获取失败"

        if uv_index <= 2: return f"紫外线指数: {uv_index} (最弱)，无需特殊防护。"
        if uv_index <= 5: return f"紫外线指数: {uv_index} (中等)，外出建议涂抹防晒霜。"
        if uv_index <= 7: return f"紫外线指数: {uv_index} (强)，请做好防护，如戴帽子、太阳镜。"
        if uv_index <= 10: return f"紫外线指数: {uv_index} (很强)，尽量减少在午间长时间暴露。"
        return f"紫外线指数: {uv_index} (极强)，请尽量避免外出，做好万全防护。"

    def get_wind_tips(self) -> str:
        """根据风力风向生成提示"""
        wind_info = self.weather_client.get_wind_info()
        return f"今日风向风力: {wind_info}"

    def build_personalized_message(self, user_name: str = "亲爱的") -> List[Dict[str, str]]:
        """构建个性化的微信模板消息内容"""
        # 确保在构建消息前，获取最新的天气数据
        if not self.weather_client.fetch_weather_data():
            logger.error("获取最新天气数据失败，无法构建消息")
            return [
                {"name": "greeting", "value": f"{user_name}，早上好！"},
                {"name": "note", "value": "抱歉，今天的天气信息获取失败了，请稍后重试哦~"}
            ]

        try:
            message = [
                {"name": "greeting", "value": f"{user_name}，{self.get_greeting()}"},
                {"name": "date", "value": datetime.now().strftime("%Y年%m月%d日 %A")},
                {"name": "temperature", "value": self.get_temperature_tips()},
                {"name": "weather_condition", "value": self.get_weather_condition_tips()},
                {"name": "wind", "value": self.get_wind_tips()},
                {"name": "precipitation", "value": self.get_precipitation_tips()},
                {"name": "uv", "value": self.get_uv_tips()},
                {"name": "note", "value": "愿你今天有个好心情，一切顺利哦！💖"}
            ]
            logger.info("成功构建个性化消息")
            return message
        except Exception as e:
            logger.error(f"构建消息时发生未知错误: {e}")
            return [
                {"name": "greeting", "value": f"{user_name}，早上好！"},
                {"name": "note", "value": "抱歉，构建天气消息时出现了点小问题，请联系管理员。"}
            ]