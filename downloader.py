import yt_dlp
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor

class VideoDownloader:
    def __init__(self):
        self.download_path = "downloads"
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
            
    def _download_sync(self, url: str):
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(self.download_path, '%(title).50s_%(id)s.%(ext)s'),
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'max_filesize': 50 * 1024 * 1024, # 50MB limit for Telegram
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            # Ensure the filename has the correct extension if merged
            if not os.path.exists(filename) and os.path.exists(filename + ".mp4"):
                filename += ".mp4"
            return filename

    async def download_video(self, url: str):
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            try:
                filename = await loop.run_in_executor(pool, self._download_sync, url)
                return filename
            except Exception as e:
                print(f"Download error: {e}")
                return None

downloader = VideoDownloader()
