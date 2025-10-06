import requests
import json
from typing import Dict, List, Optional
from config import config
import logging
import time

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class WeChatClient:
    """微信公众号客户端，负责调用微信API发送模板消息"""

    def __init__(self):
        """初始化微信客户端，从配置获取API信息"""
        self.wechat_config = config.get_section("wechat")
        self.app_id = self.wechat_config.get("app_id")
        self.app_secret = self.wechat_config.get("app_secret")
        self.template_id = self.wechat_config.get("template_id")
        self.access_token = None
        self.token_expire_time = 0

        if not all([self.app_id, self.app_secret, self.template_id]):
            raise ValueError("微信API配置不完整，请检查config.ini中的wechat部分")

        self.access_token_url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.app_id}&secret={self.app_secret}"
        self.send_template_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}"

    def get_access_token(self) -> Optional[str]:
        """获取微信API调用凭证access_token"""
        current_time = time.time()
        if self.access_token and current_time < self.token_expire_time - 200:
            logger.info("使用缓存的access_token")
            return self.access_token

        try:
            logger.info("开始获取新的access_token")
            response = requests.get(self.access_token_url, timeout=10)
            response.raise_for_status()
            result = response.json()

            if "access_token" in result and "expires_in" in result:
                self.access_token = result["access_token"]
                self.token_expire_time = current_time + result["expires_in"]
                logger.info(f"成功获取access_token，将在{result['expires_in']}秒后过期")
                return self.access_token
            else:
                logger.error(f"获取access_token失败: {result.get('errmsg', '未知错误')}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"获取access_token网络请求失败: {str(e)}")
            return None

    def send_template_message(self, open_id: str, data: List[Dict[str, str]], url: Optional[str] = None) -> bool:
        """
        发送微信模板消息

        Args:
            open_id: 接收消息的用户openid
            data: 消息数据
            url: (可选) 用户点击模板消息后跳转的URL
        """
        if not open_id:
            logger.error("open_id不能为空")
            return False
        if not data or not isinstance(data, list):
            logger.error("消息数据格式不正确")
            return False

        access_token = self.get_access_token()
        if not access_token:
            logger.error("获取access_token失败，无法发送消息")
            return False

        template_data = {}
        for item in data:
            name = item.get("name")
            value = item.get("value", "")
            color = item.get("color", "#173177")
            if name:
                template_data[name] = {"value": value, "color": color}

        request_data = {
            "touser": open_id,
            "template_id": self.template_id,
            "data": template_data
        }

        if url:
            request_data["url"] = url

        try:
            api_url = self.send_template_url.format(access_token)
            response = requests.post(
                api_url,
                data=json.dumps(request_data, ensure_ascii=False).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            if result.get("errcode") == 0:
                logger.info(f"成功向open_id: {open_id}发送模板消息")
                return True
            else:
                logger.error(f"发送模板消息失败: {result.get('errmsg', '未知错误')}，错误代码: {result.get('errcode')}")
                return False
        except requests.exceptions.RequestException as e:
            logger.error(f"发送模板消息网络请求失败: {str(e)}")
            return False

    # <--- 以下是关键修改 ---
    def send_to_users(self, user_list: List[Dict[str, str]], data: List[Dict[str, str]], url: Optional[str] = None) -> \
    Dict[str, bool]:
        """
        向多个用户发送模板消息

        Args:
            user_list: 用户列表
            data: 消息数据
            url: (可选) 统一的跳转链接
        """
        results = {}
        for user in user_list:
            open_id = user.get("open_id")
            if not open_id:
                logger.warning("跳过没有open_id的用户")
                continue

            # 将 url 传递给 send_template_message
            success = self.send_template_message(open_id, data, url=url)
            results[open_id] = success
            time.sleep(0.5)
        return results