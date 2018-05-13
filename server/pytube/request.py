# -*- coding: utf-8 -*-
"""Implements a simple wrapper around urlopen."""
from pytube.compat import urlopen, requests
import threading

def test():
    return True

def get(
    url=None, headers=False,
    streaming=False, chunk_size=8 * 1024,
):
    """Send an http GET request.

    :param str url:
        The URL to perform the GET request for.
    :param bool headers:
        Only return the http headers.
    :param bool streaming:
        Returns the response body in chunks via a generator.
    :param int chunk_size:
        The size in bytes of each chunk.
    """
    response = urlopen(url)
    if streaming:
        return stream_response(response, chunk_size)
    elif headers:
        # https://github.com/nficano/pytube/issues/160
        return {k.lower(): v for k, v in response.info().items()}
    return (
        response
        .read()
        .decode('utf-8')
    )


def get_parallel(url, on_progress):
    response = urlopen(url)
    return parallel_response(response, on_progress)


def download(url, start_index, num_of_threads, chunk_size, total_size, on_progress, buffer, lock):
    start_range = start_index * chunk_size
    last_byte = total_size - 1
    jump_size = num_of_threads * chunk_size
    chunks = int((float(total_size) / float(chunk_size)+1))
    curr_index = start_index
    all_data_len = 0
    # print(url)
    while start_range < total_size:
        end_range = min(start_range+chunk_size-1, last_byte)
        headers = {
            'range': 'bytes=%s-%s' % (start_range, end_range)
        }
        response = requests.get(url, headers=headers)
        data = response.content
        lock.acquire()
        # print('start %s - end %s' % (start_range, end_range))
        buffer[curr_index] = data
        all_data_len += len(data)
        on_progress(data, buffer, chunks)
        lock.release()
        start_range += jump_size
        curr_index += num_of_threads
    # print('all data len %s' % (all_data_len))


def parallel_response(response, on_progress, chunk_size=8 * 1024):
    size = response.length
    num_of_threads = 10
    url = response.geturl()
    threads = [None] * num_of_threads
    buffer_dict = {}
    lock = threading.Lock()
    for i in range(0, num_of_threads):
        args = (url, i, num_of_threads, chunk_size,
                size, on_progress, buffer_dict, lock)
        threads[i] = threading.Thread(target=download, args=args)
        threads[i].start()
    for i in range(0, num_of_threads):
        threads[i].join()
    return buffer_dict


def stream_response(response, chunk_size=8 * 1024):
    """Read the response in chunks."""
    while True:
        buf = response.read(chunk_size)
        if not buf:
            break
        yield buf
