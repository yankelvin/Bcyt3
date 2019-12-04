from youtube_dl import YoutubeDL


class Mp3Downloader:
    def __init__(self):
        self.set_options()
        self.count_downloads = 0
        self.urls = []

    def set_options(self):
        self.ydl_options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

    def download(self, url):
        with YoutubeDL(self.ydl_options) as ydl:
            self.urls.append(url)
            ydl.download([self.urls[self.count_downloads]])
            self.count_downloads += 1


# Download test
# downloader = Mp3Downloader()
# downloader.download("https://www.youtube.com/watch?v=PXf4rkguwDI")
# downloader.download("https://www.youtube.com/watch?v=OKvCV8MFIaw")
# downloader.download("https://www.youtube.com/watch?v=7QU1nvuxaMA")
