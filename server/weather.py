# 导入必要的类型提示，Any 用于表示任意类型
from typing import Any
# 导入 httpx 库，用于异步 HTTP 请求
import httpx
# 从 mcp.server.fastmcp 模块导入 FastMCP 类
from mcp.server.fastmcp import FastMCP

# 初始化 FastMCP 服务器实例，命名为 "weather"
mcp = FastMCP("weather")

# 常量定义
# 美国国家气象局 (NWS) API 的基础 URL
NWS_API_BASE = "https://api.weather.gov"
# API 请求中使用的用户代理字符串
USER_AGENT = "weather-app/1.0"


# 定义一个异步函数，用于向 NWS API 发出请求
async def make_nws_request(url: str) -> dict[str, Any] | None:
    """向 NWS API 发出请求，并进行适当的错误处理。"""
    # 设置请求头
    headers = {
        "User-Agent": USER_AGENT,  # 指定用户代理
        "Accept": "application/geo+json"  # 指定接受的数据格式为 geo+json
    }
    # 使用 httpx.AsyncClient 创建异步 HTTP 客户端
    async with httpx.AsyncClient() as client:
        try:
            # 发送 GET 请求，设置超时时间为 30 秒
            response = await client.get(url, headers=headers, timeout=30.0)
            # 如果请求失败（状态码不是 2xx），则抛出异常
            response.raise_for_status()
            # 返回 JSON 格式的响应数据
            return response.json()
        except Exception:
            # 如果发生任何异常，则返回 None
            return None

# 定义一个函数，用于格式化警报信息
def format_alert(feature: dict) -> str:
    """将警报特征（feature）格式化为易于阅读的字符串。"""
    # 获取警报的属性信息
    props = feature["properties"]
    # 返回格式化后的警报字符串
    return f"""
事件: {props.get('event', '未知')}
区域: {props.get('areaDesc', '未知')}
严重性: {props.get('severity', '未知')}
描述: {props.get('description', '无描述信息')}
指示: {props.get('instruction', '无具体指示')}
"""


# 使用 mcp.tool() 装饰器注册一个工具函数
@mcp.tool()
async def get_alerts(state: str) -> str:
    """获取美国指定州的天气警报。

    参数:
        state: 两个字母的美国州代码 (例如 CA, NY)
    """
    # 构建获取警报的 API URL
    url = f"{NWS_API_BASE}/alerts/active/area/{state}"
    # 发出 API 请求获取数据
    data = await make_nws_request(url)

    # 如果数据为空或数据中不包含 "features" 键
    if not data or "features" not in data:
        return "无法获取警报或未找到警报。"

    # 如果 "features" 列表为空，表示没有活动的警报
    if not data["features"]:
        return "该州目前没有活动警报。"

    # 遍历所有警报特征，并使用 format_alert 函数进行格式化
    alerts = [format_alert(feature) for feature in data["features"]]
    # 使用 "---" 分隔符连接所有格式化后的警报字符串
    return "\n---\n".join(alerts)

# 使用 mcp.tool() 装饰器注册另一个工具函数
@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """获取指定地点的天气预报。

    参数:
        latitude: 地点的纬度
        longitude: 地点的经度
    """
    # 首先，获取预报网格点的 API URL
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    # 发出 API 请求获取网格点数据
    points_data = await make_nws_request(points_url)

    # 如果网格点数据为空
    if not points_data:
        return "无法获取该地点的预报数据。"

    # 从网格点响应中获取预报的 URL
    forecast_url = points_data["properties"]["forecast"]
    # 发出 API 请求获取详细的预报数据
    forecast_data = await make_nws_request(forecast_url)

    # 如果详细预报数据为空
    if not forecast_data:
        return "无法获取详细预报。"

    # 获取预报周期数据
    periods = forecast_data["properties"]["periods"]
    forecasts = []
    # 遍历接下来的 5 个预报周期（或所有可用周期，如果少于5个）
    for period in periods[:5]:  # 只显示接下来的5个周期
        # 格式化每个周期的预报信息
        forecast = f"""
{period['name']}:
温度: {period['temperature']}°{period['temperatureUnit']}
风向风速: {period['windSpeed']} {period['windDirection']}
预报: {period['detailedForecast']}
"""
        forecasts.append(forecast)

    # 使用 "---" 分隔符连接所有格式化后的预报字符串
    return "\n---\n".join(forecasts)


# 当脚本作为主程序运行时执行
if __name__ == "__main__":
    # 初始化并运行服务器
    print('服务启动') # 打印启动信息
    # 运行 MCP 服务器，使用标准输入输出 (stdio) 作为传输方式
    mcp.run(transport='stdio')