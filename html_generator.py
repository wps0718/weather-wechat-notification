from typing import Dict, Any, List


def _generate_alerts_html(alerts: List[str]) -> str:
    """如果存在预警信息，则生成HTML模块"""
    if not alerts:
        return ""

    items_html = "".join([f"<li>{alert}</li>" for alert in alerts])
    return f"""
    <div class="alerts-card">
        <div class="alerts-header">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
            <span>今日特别提醒</span>
        </div>
        <ul>{items_html}</ul>
    </div>
    """


def create_html_page(data: Dict[str, Any], output_path: str = "weather_report.html"):
    """
    根据传入的天气数据字典，生成一个经过深度优化的、具备动态主题和智能预警的HTML页面。
    """
    # 动态生成预警模块的HTML
    alerts_html = _generate_alerts_html(data.get("alerts", []))

    html_template = """
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <meta name="theme-color" content="{theme_color}">
        <title>今日天气提醒</title>
        <style>
            :root {{
                --text-color: #333;
                --secondary-text-color: #555;
                --background-color: #f4f6f8;
                --card-background: #ffffff;
                --border-color: #e9ecef;
                --shadow-color: rgba(0, 0, 0, 0.08);

                /* 主题色变量 */
                --theme-primary: #007bff;
                --theme-gradient-start: #89f7fe;
                --theme-gradient-end: #66a6ff;
            }}
            /* --- 动态主题定义 --- */
            .theme-sunny {{ --theme-primary: #ffc107; --theme-gradient-start: #ffd54f; --theme-gradient-end: #ffb74d; }}
            .theme-rainy {{ --theme-primary: #17a2b8; --theme-gradient-start: #81d4fa; --theme-gradient-end: #4dd0e1; }}
            .theme-cloudy {{ --theme-primary: #6c757d; --theme-gradient-start: #b0bec5; --theme-gradient-end: #90a4ae; }}
            .theme-snowy {{ --theme-primary: #e0f7fa; --theme-gradient-start: #ffffff; --theme-gradient-end: #e0f2f1; --text-color: #263238; --secondary-text-color: #546e7a;}}
            .theme-foggy {{ --theme-primary: #9e9e9e; --theme-gradient-start: #cfd8dc; --theme-gradient-end: #b0bec5; }}
            .theme-default {{ --theme-primary: #007bff; --theme-gradient-start: #89f7fe; --theme-gradient-end: #66a6ff; }}

            @keyframes fadeIn {{ from {{ opacity: 0; transform: translateY(15px); }} to {{ opacity: 1; transform: translateY(0); }} }}
            body {{
                margin: 0;
                padding: 20px;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
                background-color: var(--background-color);
                color: var(--text-color);
                line-height: 1.6;
                -webkit-font-smoothing: antialiased;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                animation: fadeIn 0.8s ease-out;
            }}
            .header {{
                background: linear-gradient(120deg, var(--theme-gradient-start) 0%, var(--theme-gradient-end) 100%);
                color: white;
                padding: 30px 25px;
                border-radius: 20px;
                box-shadow: 0 8px 30px var(--shadow-color);
                text-align: center;
                margin-bottom: 20px;
            }}
            .header h1 {{ margin: 0; font-size: 24px; font-weight: 600; text-shadow: 1px 1px 2px rgba(0,0,0,0.1); }}
            .header p {{ margin: 8px 0 0; font-size: 16px; opacity: 0.9; }}

            /* --- 智能预警模块样式 --- */
            .alerts-card {{
                background-color: var(--card-background);
                border-left: 5px solid var(--theme-primary);
                border-radius: 12px;
                padding: 15px 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 15px var(--shadow-color);
            }}
            .alerts-header {{ display: flex; align-items: center; font-size: 16px; font-weight: 600; color: var(--theme-primary); }}
            .alerts-header svg {{ margin-right: 10px; }}
            .alerts-card ul {{ padding-left: 20px; margin: 10px 0 0; font-size: 14px; color: var(--secondary-text-color); }}
            .alerts-card li {{ margin-bottom: 5px; }}
            .alerts-card li:last-child {{ margin-bottom: 0; }}

            .content-card {{
                background-color: var(--card-background);
                border-radius: 20px;
                box-shadow: 0 4px 15px var(--shadow-color);
                overflow: hidden;
            }}
            .main-info {{
                text-align: center;
                padding: 25px;
                border-bottom: 1px solid var(--border-color);
            }}
            .main-info .temperature {{ font-size: 48px; font-weight: 700; color: var(--text-color); line-height: 1; }}
            .main-info .condition {{ font-size: 18px; color: var(--secondary-text-color); margin-top: 8px; }}
            .main-info .condition-tip {{ font-size: 14px; color: var(--secondary-text-color); margin-top: 12px; max-width: 80%; margin-left: auto; margin-right: auto; }}

            .details-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1px; background-color: var(--border-color); }}
            .weather-item {{ background-color: var(--card-background); padding: 18px; display: flex; flex-direction: column; align-items: center; text-align: center; }}
            .weather-item .label {{ font-weight: 500; color: var(--secondary-text-color); font-size: 14px; margin-bottom: 8px; }}
            .weather-item .value {{ font-weight: 600; font-size: 16px; color: var(--text-color); }}
            .weather-item .tip {{ display: none; /* Tips are now in main sections */ }}
            .footer {{ text-align: center; padding: 30px 20px; font-size: 14px; color: #aaa; }}
        </style>
    </head>
    <body class="theme-{theme}">
        <div class="container">
            <div class="header">
                <h1>{greeting}</h1>
                <p>{date}</p>
            </div>

            {alerts_html}

            <div class="content-card">
                <div class="main-info">
                    <div class="temperature">{temperature_value}</div>
                    <div class="condition">{weather_condition_value}</div>
                    <p class="condition-tip">{weather_condition_tip}</p>
                </div>
                <div class="details-grid">
                    <div class="weather-item">
                        <span class="label">🌬️ 风力风向</span>
                        <span class="value">{wind_value}</span>
                    </div>
                    <div class="weather-item">
                        <span class="label">💧 降水情况</span>
                        <span class="value">{precipitation_value}</span>
                    </div>
                    <div class="weather-item">
                        <span class="label">☀️ 紫外线</span>
                        <span class="value">{uv_value}</span>
                    </div>
                    <div class="weather-item">
                        <span class="label">🌡️ 体感提示</span>
                        <span class="value">{temperature_tip}</span>
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

    # 动态设置 theme-color
    theme_colors = {
        "sunny": "#ffb74d", "rainy": "#4dd0e1", "cloudy": "#90a4ae",
        "snowy": "#e0f2f1", "foggy": "#b0bec5", "default": "#66a6ff"
    }
    theme_color = theme_colors.get(data.get("theme", "default"))

    try:
        # 使用 format 方法填充模板
        filled_html = html_template.format(
            theme_color=theme_color,
            alerts_html=alerts_html,
            **data
        )
        # 写入文件
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(filled_html)
        print(f"成功生成优化版HTML页面: {output_path}")
    except KeyError as e:
        print(f"生成HTML失败：数据字典中缺少键 {e}。")
    except Exception as e:
        print(f"生成或写入HTML文件时发生未知错误: {e}")