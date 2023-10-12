import subprocess
import streamlink

def download_twitch_stream(twitch_url, output_file):
    stream_urls = streamlink.streams(twitch_url)
    
    if "best" in stream_urls:
        stream_url = stream_urls["best"].url
    else:
        raise ValueError("Could not find a suitable stream quality.")

    subprocess.run(["ffmpeg", "-i", stream_url, "-c", "copy", output_file])

twitch_url = "https://www.twitch.tv/pearbear3000"
output_file = "twitch_stream.ts"
download_twitch_stream(twitch_url, output_file)
