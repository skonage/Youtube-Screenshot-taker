from mcp.server.fastmcp import FastMCP
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from youtube_screenshot_taker import take_youtube_screenshots

mcp = FastMCP(
    name="YouTube Screenshot Taker",
    host="0.0.0.0",
    port=8050,
)

@mcp.tool()
def youtube_screenshot_tool(youtube_url: str, timestamps: list, output_dir: str = "screenshots") -> list:
    """Take screenshots from a YouTube video at specified timestamps.
    Args:
        youtube_url (str): The URL of the YouTube video.
        timestamps (list): List of timestamps (seconds or HH:MM:SS format).
        output_dir (str): Directory to save screenshots (default: 'screenshots').
    Returns:
        list: List of file paths to saved screenshots.
    """
    return take_youtube_screenshots(youtube_url, timestamps, output_dir)

if __name__ == "__main__":
    mcp.run(transport="stdio") 