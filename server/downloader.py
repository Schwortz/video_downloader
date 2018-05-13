from pytube import YouTube
import threading
import time

class Downloader():
    def __init__(self, url, filename):
        self._yt = YouTube(url)
        self._yt.register_on_progress_callback(self.on_progress_parallel)
        self._yt.register_on_complete_callback(self.on_done)
        self.title = self._yt.title
        self._filename = filename
        self._completed_percent = 0
        self._completed_bytes = 0
        self._total_bytes = 0
        self._is_done = 1
        self._thread = None

    def show_progress_bar(self, stream, chunk, file_handle, bytes_remaining):
        self._completed_bytes = self._total_bytes - bytes_remaining
        self._completed_percent = int(100*self._completed_bytes/self._total_bytes)
        if self._completed_percent % 10 == 0:
            print('completed: %d' % (self._completed_percent))

    def on_progress_parallel(self, stream, chunk, buffer, total_chunks):
        completed_chunks = float(len(buffer))
        total = float(total_chunks)
        self._completed_percent = int(100*completed_chunks/total)
        if self._completed_percent % 10 == 0:
            print('completed: %d' % (self._completed_percent))

    def start(self):
        print('start')
        self._is_done = 0
        self._thread = threading.Thread(target=self._download)
        self._thread.setDaemon(True)
        self._thread.start()

    def get_completed_percent(self):
        return self._completed_percent

    def is_done(self):
        return self._is_done

    def on_done(self, stream, file_handle):
        print('Done')
        self._is_done = 1  

    def _download(self):
        yt = self._yt
        print('Downloading %s' % (yt.title))
        stream = yt.streams.filter(mime_type='audio/mp4').first()
        self._total_bytes = stream.filesize
        t = time.time()
        buf = stream.parallel_streaming(filename=self._filename)
        print('buffer took %d' % (time.time() -t))
        # t = time.time()
        # stream.download(filename=self._filename)
        # print('file took %d' % (time.time() -t))

