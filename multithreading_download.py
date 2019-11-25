import threading

exit_flag = 0


class ThreadingDownload(threading.Thread):
    def __init__(self, directory_name, download_link, root_path, photo_id=None):
        threading.Thread.__init__(self)
        self.directory_name = directory_name
        self.download_link = download_link
        self.root_path = root_path
        self.photo_id = photo_id

    def run(self):
        import time
        import calendar
        import requests
        if self.photo_id is None:
            self.photo_id = calendar.timegm(time.gmtime())

        path = f"{self.root_path}{self.directory_name}/wallpaper{self.photo_id}.jpg"
        r = requests.get(url=self.download_link, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
