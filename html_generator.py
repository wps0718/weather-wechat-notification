from typing import Dict


def create_html_page(data: Dict[str, str], output_path: str = "weather_report.html"):
    """
    根据传入的天气数据字典，生成一个优化版的HTML页面。

    Args:
        data (Dict[str, str]): 包含天气信息的字典，注意数据结构已更新。
        output_path (str): 生成的HTML文件的保存路径。
    """

    # 经过优化的HTML模板
    html_template = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <!-- 关键优化：为移动端浏览器顶部UI栏设置主题色 -->
        <meta name="theme-color" content="#66a6ff">
        <title>今日天气提醒</title>
        <style>
            /* CSS 变量，方便统一修改主题 */
            :root {{
                --primary-color: #007bff;
                --text-color: #333;
                --secondary-text-color: #6c757d;
                --background-color: #f8f9fa;
                --card-background: #ffffff;
                --border-color: #e9ecef;
            }}

            body {{
                margin: 0;
                padding: 20px;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
                background-color: var(--background-color);
                color: var(--text-color);
                line-height: 1.6;
            }}

            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: var(--card-background);
                border-radius: 16px;
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
                overflow: hidden;
                border: 1px solid var(--border-color);
            }}

            /* 视觉刷新：采用更现代、更清爽的渐变色 */
            .header {{
                background: linear-gradient(120deg, #89f7fe 0%, #66a6ff 100%);
                color: white;
                padding: 40px 20px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 26px;
                font-weight: 600;
            }}
            .header p {{
                margin: 8px 0 0;
                font-size: 16px;
                opacity: 0.9;
            }}

            .content {{
                padding: 15px 25px 25px;
            }}

            .weather-item {{
                display: flex;
                align-items: flex-start; /* 顶部对齐，更整洁 */
                padding: 18px 0;
                border-bottom: 1px solid var(--border-color);
            }}
            .weather-item:last-child {{
                border-bottom: none;
            }}

            .weather-item .label {{
                font-weight: 500;
                color: var(--text-color);
                width: 90px;
                flex-shrink: 0;
                display: flex;
                align-items: center;
            }}
            .weather-item .emoji {{
                font-size: 22px;
                margin-right: 12px;
                line-height: 1;
            }}

            /* 信息层级优化：将数据和提示拆分 */
            .weather-item .details {{
                flex-grow: 1;
            }}
            .weather-item .value {{
                font-weight: 600;
                font-size: 16px;
                display: block; /* 确保值和提示分行 */
            }}
            .weather-item .tip {{
                font-size: 14px;
                color: var(--secondary-text-color);
                margin-top: 4px;
                display: block;
            }}

            .footer {{
                text-align: center;
                padding: 20px;
                font-size: 14px;
                color: var(--secondary-text-color);
                background-color: #fdfdfd;
                border-top: 1px solid var(--border-color);
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
                    <div class="details">
                        <span class="value">{temperature_value}</span>
                        <span class="tip">{temperature_tip}</span>
                    </div>
                </div>
                <div class="weather-item">
                    <span class="label"><span class="emoji">☁️</span>天气</span>
                    <div class="details">
                        <span class="value">{weather_condition_value}</span>
                        <span class="tip">{weather_condition_tip}</span>
                    </div>
                </div>
                <div class="weather-item">
                    <span class="label"><span class="emoji">🌬️</span>风力</span>
                    <div class="details">
                        <span class="value">{wind_value}</span>
                        <span class="tip">{wind_tip}</span>
                    </div>
                </div>
                <div class="weather-item">
                    <span class="label"><span class="emoji">💧</span>降水</span>
                    <div class="details">
                        <span class="value">{precipitation_value}</span>
                        <span class="tip">{precipitation_tip}</span>
                    </div>
                </div>
                <div class="weather-item">
                    <span class="label"><span class="emoji">☀️</span>紫外线</span>
                    <div class="details">
                        <span class="value">{uv_value}</span>
                        <span class="tip">{uv_tip}</span>
                    </div>
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
    try:
        filled_html = html_template.format(**data)
        # 写入文件
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(filled_html)
        print(f"成功生成HTML页面: {output_path}")
    except KeyError as e:
        print(f"生成HTML失败：数据字典中缺少键 {e}。请检查 scheduler.py 中的数据准备部分。")
    except Exception as e:
        print(f"生成或写入HTML文件时发生未知错误: {e}")
