# ☀️ 天气微信推送通知

> 每天定时给女朋友推送天气信息和温馨寄语，并通过 GitHub Pages 展示精美的毛玻璃风格天气页面。

---

## 🌟 功能

- **每日定时推送** — 每天早上 07:30（北京时间），通过微信公众号模板消息推送今日天气
- **精美天气页面** — 毛玻璃（Glassmorphism）风格 HTML 页面，随天气自动切换主题色
  - ☀️ 晴天 / 🌧️ 雨天 / ☁️ 阴天 / ❄️ 雪天 / 🌫️ 雾天
- **紫外线进度条** — 可视化展示紫外线强度等级
- **智能预警提醒** — 降水、强紫外线、温差大时自动高亮提醒
- **每日不重复寄语** — 31 句专属暖心寄语每天轮换，带称呼（如"仪姐"）
- **GitHub Actions 自动运行** — 无需自己部署服务器

## 🏗️ 项目结构

```
weather-wechat-notification/
├── .github/workflows/daily_weather_push.yml   # GitHub Actions 定时任务配置
├── config.py             # 配置解析器，读取 config.ini
├── weather_client.py     # 和风天气 API 客户端（实时天气 + 3天预报）
├── message_builder.py    # 消息构建器（问候语、天气提示、每日寄语）
├── html_generator.py     # 毛玻璃风格 HTML 页面生成器
├── wechat_client.py      # 微信公众号模板消息推送客户端
├── scheduler.py          # 定时调度器（组装全流程并执行）
├── main.py               # 主入口（支持手动 / 定时两种模式）
├── weather_report.html   # 生成的天气页面示例
├── requirements.txt      # Python 依赖
├── config.ini            # 配置文件（已 .gitignore，不上传到 GitHub）
└── README.md             # 本文件
```

## 🔁 数据流程

```
和风天气 API ──→ WeatherClient ──→ MessageBuilder ──→ html_generator.py → HTML页面
                                                         ↓
                                                     git push → GitHub Pages
                                                         ↓
微信公众号模板消息 ←── WeChatClient ←── 附带 Pages 链接推送给用户
```

## ⚙️ 配置

需要创建 `config.ini` 文件（不提交到仓库），内容如下：

```ini
[wechat]
app_id = 你的微信公众号AppID
app_secret = 你的微信公众号AppSecret
template_id = 你的模板消息ID

[weather_api]
key = 和风天气API Key
location = 城市ID（如 101010100 为北京）

[scheduler]
push_time = 07:30

[users]
user_list = openid1, 昵称1; openid2, 昵称2
```

### GitHub Secrets 配置

本项目通过 GitHub Actions 运行，需在仓库的 **Settings → Secrets and variables → Actions** 中添加以下 Secrets：

| Secret 名称 | 说明 |
|-------------|------|
| `app_id` | 微信公众号 AppID |
| `app_secret` | 微信公众号 AppSecret |
| `template_id` | 微信模板消息 ID |
| `key` | 和风天气 API Key |
| `location` | 城市 ID |
| `push_time` | 推送时间（如 `07:30`） |
| `user_list` | 用户列表（`openid, 昵称`，多个用户用 `;` 分隔） |

## 🚀 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 创建 config.ini（参考上方配置说明）
# 手动发送一次
python main.py --mode manual

# 启动定时调度（每天指定时间自动发送）
python main.py --mode scheduler
```

## ☁️ GitHub Actions 定时任务

每天早上 `UTC 23:30`（北京时间 **07:30**）自动执行：

1. 拉取代码
2. 从 Secrets 动态生成 `config.ini`
3. 获取天气数据 → 生成 HTML 页面
4. 通过微信公众号推送模板消息给用户
5. 将 HTML 页面提交回仓库，触发 GitHub Pages 更新

### 手动触发

仓库页面 → **Actions** → **Daily Weather Push** → **Run workflow** → 选择 `main` → **Run**

## 🎨 设计亮点

- **毛玻璃（Glassmorphism）卡片** — 半透明背景 + `backdrop-filter: blur()` 实现磨砂玻璃质感
- **动态天气主题** — 6 套主题色根据天气自动切换
- **紫外线进度条** — 绿 → 黄 → 橙 → 红 渐变色条，直观展示 UV 等级
- **背景光晕** — 主题色模糊光晕作为背景装饰
- **入场动画** — 页面加载时柔和 fadeIn 动画
- **移动端优先** — 以 375px 为设计基准，完美适配微信内置浏览器
- **浏览器兼容降级** — 不支持 `backdrop-filter` 时自动回退半透明纯色背景

## 📦 依赖

- `requests` — HTTP 请求库
- `apscheduler` — 定时任务调度
- `configparser` — 配置文件解析（Python 内置）

## 📄 许可证

MIT
