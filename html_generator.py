from typing import Dict


def create_html_page(data: Dict[str, str], output_path: str = "weather_report.html"):
    """
    根据传入的天气数据字典，生成一个HTML页面。

    Args:
        data (Dict[str, str]): 包含天气信息的字典。
        output_path (str): 生成的HTML文件的保存路径。
    """

    # HTML 模板，使用了内联CSS，确保在所有设备上都能良好显示
    html_template = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>今日天气预报</title>
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                background-color: #f4f7f9;
                margin: 0;
                padding: 20px;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 12px;
                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px 20px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
            }}
            .header p {{
                margin: 5px 0 0;
                font-size: 16px;
                opacity: 0.9;
            }}
            .content {{
                padding: 20px 30px 30px;
            }}
            .weather-item {{
                display: flex;
                align-items: center;
                border-bottom: 1px solid #eef2f5;
                padding: 15px 0;
            }}
            .weather-item:last-child {{
                border-bottom: none;
            }}
            .weather-item .label {{
                font-weight: 600;
                color: #555;
                width: 80px;
                flex-shrink: 0;
            }}
            .weather-item .value {{
                flex-grow: 1;
                color: #333;
                line-height: 1.6;
            }}
            .footer {{
                text-align: center;
                padding: 20px;
                font-size: 14px;
                color: #999;
                background-color: #fafafa;
            }}
            .emoji {{
                font-size: 20px;
                margin-right: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{greeting}</h1>
                <p>{date}</p>
            </div>
            <div class="content">
                <div class="weather-item">
                    <span class="label"><span class="emoji">🌡️</span>温度</span>
                    <span class="value">{temperature}</span>
                </div>
                <div class="weather-item">
                    <span class="label"><span class="emoji">☁️</span>天气</span>
                    <span class="value">{weather_condition}</span>
                </div>
                <div class="weather-item">
                    <span class="label"><span class="emoji">🌬️</span>风力</span>
                    <span class="value">{wind}</span>
                </div>
                <div class="weather-item">
                    <span class="label"><span class="emoji">💧</span>降水</span>
                    <span class="value">{precipitation}</span>
                </div>
                <div class="weather-item">
                    <span class="label"><span class="emoji">☀️</span>紫外线</span>
                    <span class="value">{uv}</span>
                </div>
            </div>
            <div class="footer">
                <p>{note}</p>
            </div>
        </div>
    </body>
    </html>
    """

    # 使用 format 方法填充模板
    filled_html = html_template.format(**data)

    # 写入文件
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(filled_html)
        print(f"成功生成HTML页面: {output_path}")
    except IOError as e:
        print(f"写入HTML文件失败: {e}")