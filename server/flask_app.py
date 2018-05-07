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

@app.route("/get_file")
def get_file():
    fp = os.path.join(os.getcwd(), request.args.get('fp'))
    title = request.args.get('title')
    return send_file(filename_or_fp=fp, attachment_filename=title, as_attachment=True)

@app.route("/download_file", methods = ['GET'])
def download_file():
    url = request.args.get('url', None)
    if not test_url(url):
        return 'Please Enter A Valid YouTube URL'
    print(url)
    title = downloader.main(url) + '.mp4'
    title = 'test_file.mp4'
    fp = 'my_file.mp4'
    _json = {
        "fp" : fp,
        "title" : title
    }
    return json.dumps(_json)
    

if __name__ == '__main__':
    app.run(debug=True)