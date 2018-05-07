from pytube import YouTube
def show_progress_bar(stream, chunk, file_handle, bytes_remaining):
    completed = int(100*(stream.filesize-bytes_remaining)/stream.filesize)
    print('completed: %d' % (completed))

def main(url):
    yt = YouTube(url)
    yt.register_on_progress_callback(show_progress_bar)
    print('Downloading %s' % (yt.title))
    yt.streams.filter(mime_type='audio/mp4').first().download(filename='my_file')
    return yt.title

if __name__ == '__main__':
    main('https://www.youtube.com/watch?v=bCDIt50hRDs')