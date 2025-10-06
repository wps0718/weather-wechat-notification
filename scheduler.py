from apscheduler.schedulers.blocking import BlockingScheduler
from weather_client import WeatherClient
from message_builder import MessageBuilder
from wechat_client import WeChatClient
from config import config
from typing import List, Dict
import logging
import traceback
import time
from html_generator import create_html_page
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class WeatherNotificationScheduler:
    """天气通知定时任务调度器，负责每日自动推送天气信息"""

    def __init__(self):
        """初始化定时任务调度器"""
        self.scheduler = BlockingScheduler(timezone="Asia/Shanghai")
        self.push_time = config.get("scheduler", "push_time", "07:30")
        self.user_list = self._get_user_list()
        self.weather_client = WeatherClient()
        self.wechat_client = WeChatClient()
        logger.info(f"定时任务初始化完成，每日推送时间: {self.push_time}")

    def _get_user_list(self) -> List[Dict[str, str]]:
        """从配置获取用户列表"""
        users = []
        user_str = config.get("users", "user_list", "")
        if not user_str:
            logger.warning("未配置任何用户，将无法发送消息")
            return users
        for user_info in user_str.split(";"):
            user_info = user_info.strip()
            if not user_info: continue
            parts = [part.strip() for part in user_info.split(",")]
            if len(parts) >= 2:
                users.append({"open_id": parts[0], "name": parts[1]})
            else:
                logger.warning(f"用户信息格式不正确: {user_info}，正确格式应为 'openid, 用户名'")
        logger.info(f"共加载 {len(users)} 个用户")
        return users

    def send_weather_notification(self) -> None:
        """发送天气通知给所有用户"""
        try:
            logger.info("开始发送天气通知")
            message_builder = MessageBuilder(self.weather_client)

            if not self.weather_client.fetch_weather_data():
                logger.error("获取天气数据失败，无法继续发送通知。")
                return

            html_data = {
                "greeting": message_builder.get_greeting(),
                "date": time.strftime("%Y年%m月%d日 %A"),
                "temperature": message_builder.get_temperature_tips(),
                "weather_condition": message_builder.get_weather_condition_tips(),
                "wind": message_builder.get_wind_tips(),
                "precipitation": message_builder.get_precipitation_tips(),
                "uv": message_builder.get_uv_tips(),
                "note": "愿你今天有个好心情，一切顺利哦！💖"
            }

            html_output_path = "weather_report.html"
            create_html_page(html_data, html_output_path)

            logger.info("开始将HTML页面推送到GitHub...")
            os.system('git add .')
            os.system(f'git commit -m "Update weather report for {time.strftime("%Y-%m-%d")}"')
            os.system('git push')
            logger.info("推送完成！")

            # !!! --- 请务必替换成你自己的GitHub Pages地址 --- !!!
            github_username = " wps0718"  # <--- 替换
            repo_name = "weather-wechat-notification"              # <--- 替换
            html_url = f"https://{github_username}.github.io/{repo_name}/{html_output_path}"
            logger.info(f"详情页URL: {html_url}")

            for user in self.user_list:
                open_id = user.get("open_id")
                user_name = user.get("name", "亲爱的")
                logger.info(f"为用户 {user_name} (open_id: {open_id}) 构建消息")

                message_data = [
                    {"name": "greeting", "value": f"{user_name}，{html_data['greeting']}"},
                    {"name": "date", "value": html_data['date']},
                    {"name": "temperature", "value": html_data['temperature'].split('\n')[0]},
                    {"name": "weather_condition", "value": html_data['weather_condition'].split('\n')[0]},
                    {"name": "wind", "value": html_data['wind']},
                    {"name": "precipitation", "value": html_data['precipitation']},
                    {"name": "uv", "value": html_data['uv']},
                    {"name": "note", "value": "点击查看今日天气详情与穿搭建议💖"}
                ]

                success = self.wechat_client.send_template_message(open_id, message_data, url=html_url)

                # <--- 关键修改：移除了原来位置错误且多余的if判断 ---

                if success:
                    logger.info(f"向用户 {user_name} 发送消息成功")
                else:
                    logger.error(f"向用户 {user_name} 发送消息失败")
                time.sleep(1)

            logger.info("天气通知发送完成")
        except Exception as e:
            logger.error(f"发送天气通知时发生严重错误: {e}")
            logger.error(traceback.format_exc())

    def start_scheduler(self) -> None:
        """启动定时任务调度器"""
        try:
            hour, minute = self.push_time.split(":")
            self.scheduler.add_job(
                self.send_weather_notification,
                'cron',
                hour=int(hour),
                minute=int(minute)
            )
            logger.info(f"定时任务已启动，将在每日 {self.push_time} 发送天气通知")
            logger.info("按 Ctrl+C 停止调度器")
            self.scheduler.start()
        except ValueError:
            logger.error(f"推送时间格式不正确: {self.push_time}，请使用 HH:MM 格式。")
        except Exception as e:
            logger.error(f"启动定时任务时发生错误: {e}")
            logger.error(traceback.format_exc())


if __name__ == "__main__":
    scheduler = WeatherNotificationScheduler()
    scheduler.start_scheduler()
