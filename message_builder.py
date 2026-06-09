from typing import Dict, List
from weather_client import WeatherClient
from datetime import datetime
import logging
import random

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
        """根据天气状况生成提示，每种天气有3句随机提示语"""
        condition = self.weather_client.get_weather_condition().lower()
        if condition == "未知":
            return "天气状况信息获取失败"

        # 为每种天气定义3句不同的提示语
        weather_tips = {
            "雨": [
                "今天有雨，出门请记得带伞，雨天路滑注意安全。",
                "雨天出行，记得穿防滑鞋，开车减速慢行，注意安全。",
                "雨水滋润万物，但也别忘了保持干爽，带好雨具出门哦。"
            ],
            "雪": [
                "今天有雪，注意防寒保暖，雪天路滑，出行请格外小心。",
                "雪花纷飞的日子，多穿些保暖的衣物，防止感冒。",
                "银装素裹的美景虽美，但路面湿滑，出行需谨慎。"
            ],
            "晴": [
                "天气晴朗，阳光明媚，适合户外活动，也要注意防晒哦。",
                "晴空万里，是出游的好日子，记得涂抹防晒霜保护皮肤。",
                "阳光正好，不妨出门走走，呼吸新鲜空气，放松心情。"
            ],
            "阴": [
                "今天天气阴沉，但别让天气影响心情，要开心呀。",
                "阴天虽然没有阳光，但也不会晒伤，适合轻松出行。",
                "阴天光线柔和，是拍照的好时机，不妨记录美好瞬间。"
            ],
            "雾霾": [
                "今天有雾或霾，能见度较低，外出请注意安全，可佩戴口罩。",
                "雾霾天气，尽量减少户外活动，必须外出时请戴好口罩。",
                "今天空气质量不佳，开车注意减速慢行，保持安全距离。"
            ],
            "风": [
                "今天风力较大，注意防风，保护好自己不要着凉。",
                "大风天气，外出请系好围巾，扣好衣扣，以防感冒。",
                "风大时请关好门窗，外出注意安全，避免在广告牌等物体下逗留。"
            ]
        }

        tips = []
        # 根据天气状况选择对应的随机提示语
        if "雨" in condition: 
            tips.append(random.choice(weather_tips["雨"]))
        if "雪" in condition: 
            tips.append(random.choice(weather_tips["雪"]))
        if "晴" in condition: 
            tips.append(random.choice(weather_tips["晴"]))
        if "阴" in condition: 
            tips.append(random.choice(weather_tips["阴"]))
        if "雾" in condition or "霾" in condition: 
            tips.append(random.choice(weather_tips["雾霾"]))
        if "风" in condition: 
            tips.append(random.choice(weather_tips["风"]))

        return "\n".join(tips) if tips else f"今天天气{condition}，祝你事事顺心~。爱你仪姐，明天见"

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
        
    def get_daily_note(self, name: str = "") -> str:
        """
        根据日期生成每日不同的温馨寄语
        每天一句不重复，用日期(1~31)从31句语料池中选取，
        同一日期的每天固定对应同一句，形成"每日限定"的感觉。
        """
        now = datetime.now()
        day = now.day          # 1~31
        weekday = now.weekday()  # 0=周一, 6=周日

        # 31句每日寄语池（每天不重样）
        daily_notes = [
            "愿你今天有个好心情，一切顺利哦！💖",
            "今天也要做个开心的人，世界也会对你温柔以待🌸",
            "日子平淡，好在有你在身边，今天也要好好过呀✨",
            "新的一天，新的好运正在派送中，请查收🎁",
            "今天也要好好吃饭、好好喝水、好好爱自己哦🥰",
            "不管天气怎样，都要做自己的小太阳☀️",
            "今天的你，比昨天更好，比明天更值得期待🌈",
            "生活明朗，万物可爱，今天也要元气满满💪",
            "把每一天都过得闪闪发光，你就是最棒的🌟",
            "今天又是被世界偏爱的一天，要开心呀🎈",
            "累了就歇歇，想我了就看看天气推送，我一直都在💕",
            "今天的任务：认真做好每件小事，然后好好休息😊",
            "好运正在路上，你先要开心起来，它才能找到你🍀",
            "不管今天遇到什么，记得有我在背后支持你💗",
            "生活可能偶尔不如意，但你的笑容总能治愈一切😄",
            "今天也要像阳光一样，温暖而不炙热，明亮而不刺眼🌻",
            "每一个平凡的日子，都值得被认真对待和珍惜📅",
            "今天的你，一定会被好运和善意包围的🤗",
            "愿你今天所有的小目标都能实现，加油呀🎯",
            "今天是最年轻的一天，当然要开心地过呀🎉",
            "记得多笑笑，你笑起来真的很好看😊",
            "生活也许很忙，但别忘了照顾好自己，你很重要💝",
            "今天的快乐正在派送中，记得保持心情愉快哦📬",
            "愿你的每一天都像今天的天气一样，刚刚好☁️",
            "万物皆可期待，今天也要满怀希望地出发🚀",
            "你是被爱着的，今天也是，每一天都是💗",
            "今天做个简单快乐的人，不想太多，只管开心🥳",
            "今天的运气指数五颗星，快去发现生活中的小确幸⭐",
            "无论今天发生了什么，回家路上记得买点好吃的犒劳自己🍰",
            "你值得拥有这世界上所有美好的东西，包括今天的美好🌷",
            "又过了一天，离我们见面的日子又近了一点🥰",
        ]

        # 用日期选取当天的专属寄语（day 取值范围 1~31）
        note = daily_notes[(day - 1) % len(daily_notes)]

        # 如果有名字，加上称呼
        if name:
            return f"{name}，{note}"
        return note

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
                {"name": "note", "value": self.get_daily_note()}
            ]
            logger.info("成功构建个性化消息")
            return message
        except Exception as e:
            logger.error(f"构建消息时发生未知错误: {e}")
            return [
                {"name": "greeting", "value": f"{user_name}，早上好！"},
                {"name": "note", "value": "抱歉，构建天气消息时出现了点小问题，请联系管理员。"}
            ]
