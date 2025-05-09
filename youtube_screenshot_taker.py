import subprocess
import os
import re
import argparse
from urllib.parse import quote_plus # For safe filenames

def generate_safe_filename(base_name, timestamp_str, extension="jpg"):
    """Generates a filesystem-safe filename."""
    safe_base = re.sub(r'[^\w\-_.]', '_', base_name)
    safe_timestamp = re.sub(r'[^\w\-_.]', '_', str(timestamp_str))
    return f"{safe_base}_ts_{safe_timestamp}.{extension}"

def take_youtube_screenshots(youtube_url: str, timestamps: list, output_dir: str = "screenshots"):
    """
    Takes screenshots from a YouTube video at specified timestamps.

    Args:
        youtube_url (str): The URL of the YouTube video.
        timestamps (list): A list of timestamps. Each timestamp can be
                           in seconds (int/float) or "HH:MM:SS" string format
                           as understood by FFmpeg's -ss option.
        output_dir (str): The directory where screenshots will be saved.
                           The function will create this directory if it doesn't exist.

    Returns:
        list: A list of file paths to the saved screenshots.
              Returns an empty list if errors occur.
    """
    screenshot_paths = []

    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            print(f"Created output directory: {output_dir}")
        except OSError as e:
            print(f"Error creating output directory {output_dir}: {e}")
            return []

    video_stream_url = ""
    try:
        print(f"Fetching video stream URL for: {youtube_url}")
        yt_dlp_command = ["yt-dlp", "-f", "bestvideo", "-g", "--no-warnings", youtube_url]
        process = subprocess.Popen(yt_dlp_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
        stdout, stderr = process.communicate(timeout=60)

        if process.returncode == 0 and stdout:
            video_stream_url = stdout.strip().split('\n')[0]
            print(f"Successfully fetched stream URL: {video_stream_url}")
        else:
            print(f"Error getting 'bestvideo' stream URL from yt-dlp for {youtube_url}:")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            print("Trying fallback to get any video stream URL (-g only)...")
            yt_dlp_command_fallback = ["yt-dlp", "-g", "--no-warnings", youtube_url]
            process_fallback = subprocess.Popen(yt_dlp_command_fallback, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
            stdout_fallback, stderr_fallback = process_fallback.communicate(timeout=60)

            if process_fallback.returncode == 0 and stdout_fallback:
                video_stream_url = stdout_fallback.strip().split('\n')[0]
                print(f"Successfully fetched fallback stream URL: {video_stream_url}")
            else:
                print(f"Fallback failed to get stream URL from yt-dlp for {youtube_url}:")
                print(f"STDOUT: {stdout_fallback}")
                print(f"STDERR: {stderr_fallback}")
                return []
    except subprocess.TimeoutExpired:
        print(f"yt-dlp command timed out while fetching stream URL for {youtube_url}.")
        return []
    except Exception as e:
        print(f"An exception occurred while running yt-dlp for {youtube_url}: {e}")
        return []

    if not video_stream_url:
        print(f"Could not retrieve a video stream URL for {youtube_url}.")
        return []

    if "v=" in youtube_url:
        url_part_for_filename = quote_plus(youtube_url.split("v=")[-1].split("&")[0])
    else:
        url_part_for_filename = quote_plus(os.path.basename(youtube_url.split("?")[0]))
        if not url_part_for_filename:
            url_part_for_filename = "custom_video_id"

    for ts in timestamps:
        timestamp_str = str(ts).strip()
        if not timestamp_str:
            continue
        base_filename_part = f"video_{url_part_for_filename}"
        output_filename = generate_safe_filename(base_filename_part, timestamp_str)
        output_filepath = os.path.join(output_dir, output_filename)

        try:
            print(f"Attempting to capture frame at timestamp '{timestamp_str}' for {youtube_url}...")
            ffmpeg_command = [
                "ffmpeg",
                "-ss", timestamp_str,
                "-i", video_stream_url,
                "-vframes", "1",
                "-q:v", "2",
                "-y",
                "-loglevel", "error",
                output_filepath
            ]
            process = subprocess.Popen(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
            stdout, stderr = process.communicate(timeout=60)

            if process.returncode == 0:
                if os.path.exists(output_filepath) and os.path.getsize(output_filepath) > 0:
                    screenshot_paths.append(os.path.abspath(output_filepath))
                    print(f"Successfully saved screenshot: {os.path.abspath(output_filepath)}")
                else:
                    print(f"FFmpeg reported success for timestamp {timestamp_str}, but output file {output_filepath} is missing or empty.")
                    print(f"FFmpeg STDOUT: {stdout}")
                    print(f"FFmpeg STDERR: {stderr}")
            else:
                print(f"Error capturing screenshot for timestamp {timestamp_str} on {youtube_url}:")
                print(f"FFmpeg STDOUT: {stdout}")
                print(f"FFmpeg STDERR: {stderr}")
        except subprocess.TimeoutExpired:
            print(f"FFmpeg command timed out for timestamp {timestamp_str} on video {youtube_url}.")
        except Exception as e:
            print(f"An exception occurred while running ffmpeg for timestamp {timestamp_str} on {youtube_url}: {e}")
    return screenshot_paths

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Take screenshots from a YouTube video at specified timestamps.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    # Changed youtube_url from positional to a required flagged argument
    parser.add_argument("-u", "--url", type=str, required=True,
                        help="The URL of the YouTube video. (Short: -u)")

    timestamp_group = parser.add_mutually_exclusive_group(required=True)
    timestamp_group.add_argument("-ts", "--timestamps", type=str, nargs='+',
                                 help="A list of timestamps (e.g., 10 0:45 120.5 '01:02:03').\n"
                                      "Timestamps can be in seconds or HH:MM:SS format. (Short: -ts)")
    timestamp_group.add_argument("-tf", "--timestamps_file", type=str,
                                 help="Path to a file containing timestamps, one timestamp per line.\n"
                                      "Each line can be seconds or HH:MM:SS format. (Short: -tf)")

    parser.add_argument("-o", "--output_dir_base", type=str, default="cli_screenshots",
                        help="Base directory to save screenshots. A subfolder for the video will be created here.\n"
                             "(default: cli_screenshots) (Short: -o)")

    args = parser.parse_args() # youtube_url will now be accessed via args.url

    actual_timestamps = []
    if args.timestamps_file:
        try:
            with open(args.timestamps_file, 'r', encoding='utf-8') as f:
                actual_timestamps = [line.strip() for line in f if line.strip()]
            if not actual_timestamps:
                print(f"Warning: Timestamps file '{args.timestamps_file}' is empty or contains no valid timestamps.")
                parser.exit(1)
        except FileNotFoundError:
            print(f"Error: Timestamps file not found: {args.timestamps_file}")
            parser.exit(1)
        except Exception as e:
            print(f"Error reading timestamps file '{args.timestamps_file}': {e}")
            parser.exit(1)
    elif args.timestamps:
        actual_timestamps = args.timestamps

    if not actual_timestamps:
        print("Error: No timestamps to process. Please provide timestamps via -ts/--timestamps or -tf/--timestamps_file.")
        parser.exit(1)

    # Use args.url for the YouTube URL
    if "v=" in args.url:
        video_id_for_folder = args.url.split("v=")[-1].split("&")[0]
    else:
        temp_id = os.path.basename(args.url.split("?")[0])
        video_id_for_folder = quote_plus(temp_id if temp_id else "unknown_video")

    video_specific_output_dir = os.path.join(args.output_dir_base, f"video_{video_id_for_folder}")

    print(f"\nProcessing YouTube URL: {args.url}") # Changed from args.youtube_url
    if args.timestamps_file:
        print(f"Reading timestamps from file: {args.timestamps_file}")
    print(f"Requested timestamps: {actual_timestamps}")
    print(f"Screenshots will be saved in a subfolder within: {os.path.abspath(args.output_dir_base)}")
    print(f"Specifically, in: {os.path.abspath(video_specific_output_dir)}\n")

    # Pass args.url to the function
    saved_files = take_youtube_screenshots(args.url, actual_timestamps, output_dir=video_specific_output_dir)

    if saved_files:
        print("\n--- Summary ---")
        print("Screenshots saved successfully:")
        for f_path in saved_files:
            print(f"- {f_path}")
    else:
        print("\n--- Summary ---")
        print("No screenshots were saved, or an error occurred. Check the logs above.")

    print("\nScript finished.")