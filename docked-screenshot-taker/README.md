# MCP YouTube Screenshot Taker Server

This is an MCP server exposing a YouTube screenshot tool using FastMCP. It allows you to take screenshots from a YouTube video at specified timestamps via MCP.

## Running with Docker

1. **Build the Docker image:**

   ```sh
   docker build -t mcp-screenshot-taker .
   ```

2. **Run the server (stdio transport):**

   ```sh
   docker run --rm mcp-screenshot-taker
   ```

   By default, the server runs with stdio transport. For SSE, you can modify the code or entrypoint.

3. **Run the server (SSE transport, optional):**

   If you want to use SSE, edit `server.py` to set `transport = "sse"` and run:

   ```sh
   docker run --rm -p 8050:8050 mcp-screenshot-taker
   ```

## Requirements
- Python 3.10+
- [fastmcp](https://pypi.org/project/fastmcp/)
- [yt-dlp](https://pypi.org/project/yt-dlp/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [ffmpeg](https://ffmpeg.org/) (installed in the Docker image)

---

See `server.py` for the server implementation. 