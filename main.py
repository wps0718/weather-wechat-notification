from scheduler import WeatherNotificationScheduler
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def manual_send():
    """手动发送一次天气通知"""
    try:
        logger.info("开始手动发送天气通知...")
        # 直接复用 WeatherNotificationScheduler 中的发送逻辑，不再重复造轮子
        scheduler_instance = WeatherNotificationScheduler()
        scheduler_instance.send_weather_notification()
        logger.info("手动发送天气通知完成")
    except Exception as e:
        logger.error(f"手动发送时发生错误: {e}")
        import traceback
        logger.error(traceback.format_exc())


def main():
    """主函数，解析命令行参数并执行相应操作"""
    parser = argparse.ArgumentParser(description="天气微信推送系统")
    parser.add_argument(
        "--mode",
        choices=["scheduler", "manual"],
        default="scheduler",
        help="运行模式: scheduler(定时任务模式) 或 manual(手动发送模式)"
    )
    args = parser.parse_args()

    if args.mode == "scheduler":
        scheduler = WeatherNotificationScheduler()
        scheduler.start_scheduler()
    elif args.mode == "manual":
        manual_send()


if __name__ == "__main__":
    main()