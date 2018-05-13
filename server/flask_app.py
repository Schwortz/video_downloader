import downloader
from flask import Flask, request, render_template, send_file, json
import os
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

def test_url(url):
    if not url:
        return False
    return True

def error_json(msg):
    _json = {
        'error':msg,
    }
    return json.dumps(_json)

def get_user_id(user_id):
    return user_id.replace('.','')

@app.route("/get_file")
def get_file():
    user_id = get_user_id(request.remote_addr)
    print('get file %s' % (user_id))
    if user_id not in DOWNLOADS:
        return 'File Not Found'
    yt = DOWNLOADS[user_id]
    fp = yt._filename + '.mp4'
    title = yt.title
    fp = os.path.join(os.getcwd(), fp)
    del DOWNLOADS[user_id]
    return 'get_file'
    return send_file(filename_or_fp=fp, attachment_filename=title, as_attachment=True)

@app.route("/check_progress")
def check_progress():
    print('check_progress')
    user_id = get_user_id(request.remote_addr)
    yt = DOWNLOADS.get(user_id, None)
    if not yt:
        return error_json('No download in progress')
    percent = yt.get_completed_percent()
    is_done = 1 if yt.is_done() else 0
    print('title: %s - progress %d done: %d total bytes: %d' % (yt.title, percent, is_done, yt._total_bytes))
    _json = {
        "percent" : percent,
        "is_done" : is_done
    }
    print(_json)
    return json.dumps(_json)

DOWNLOADS = {}

@app.route("/download_file", methods = ['GET'])
def download_file():
    user_id = get_user_id(request.remote_addr)
    print('ip: %s downloading' % (user_id))
    url = request.args.get('url', None)
    if not test_url(url):
        return error_json('Please Enter A Valid YouTube URL')
    print(url)
    if user_id in DOWNLOADS:
        return error_json('Already downloading')
    yt = downloader.Downloader(url, user_id)
    DOWNLOADS[user_id] = yt
    title = yt.title + '.mp4'
    yt.start()
    fp = '%s.mp4' % (user_id)
    _json = {
        "fp" : fp,
        "title" : title
    }

    return json.dumps(_json)
    

if __name__ == '__main__':
    app.run(debug=True)