# YouTube Screenshot Taker

A command-line tool to take high-quality screenshots from any YouTube video at specified timestamps. It uses `yt-dlp` to fetch the video stream and `ffmpeg` to extract frames.

## Features

- Capture screenshots from YouTube videos at any timestamp (seconds or `HH:MM:SS` format).
- Supports multiple timestamps per run.
- Output screenshots are saved with safe, descriptive filenames.
- Handles both direct timestamp input and timestamp files.
- Automatically organizes screenshots into per-video folders.

## Requirements

- Python 3.7+
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) (Python package)
- [ffmpeg](https://ffmpeg.org/) (must be installed and available in your system PATH)

Install Python dependencies:
```bash
pip install -r requirements.txt
```

Install ffmpeg (if not already installed):

- **Ubuntu/Debian:** `sudo apt-get install ffmpeg`
- **Windows:** [Download from ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

## Usage

```bash
python youtube_screenshot_taker.py -u <YOUTUBE_URL> -ts <TIMESTAMP1> <TIMESTAMP2> ...
```

Or, using a file with timestamps (one per line):

```bash
python youtube_screenshot_taker.py -u <YOUTUBE_URL> -tf <TIMESTAMPS_FILE>
```

### Arguments

- `-u`, `--url` **(required)**: The URL of the YouTube video.
- `-ts`, `--timestamps`: List of timestamps (e.g., `10 0:45 120.5 01:02:03`). Can be in seconds or `HH:MM:SS` format.
- `-tf`, `--timestamps_file`: Path to a file containing timestamps, one per line.
- `-o`, `--output_dir_base`: Base directory to save screenshots (default: `cli_screenshots`). A subfolder for each video will be created.

### Example

```bash
python youtube_screenshot_taker.py -u "https://www.youtube.com/watch?v=ZhlM4ntQBGI" -ts 10 0:45 120.5 "01:02:03"
```

Or with a file:
```
# timestamps.txt
10
0:45
120.5
01:02:03
```
```bash
python youtube_screenshot_taker.py -u "https://www.youtube.com/watch?v=ZhlM4ntQBGI" -tf timestamps.txt
```

## Output

Screenshots are saved in a subfolder of the output directory, named after the video ID. Filenames include the video ID and timestamp, e.g.:

```
cli_screenshots/video_ZhlM4ntQBGI/video_ZhlM4ntQBGI_ts_03_15.jpg
```

## Troubleshooting

- Ensure `yt-dlp` and `ffmpeg` are installed and accessible from your command line.
- If you encounter errors, check the printed logs for details.

## License

MIT License 