from flask import Flask
import views.home
import views.download
import views.verify

app = Flask(__name__)


@app.route('/')
def index():
    return views.home.handle_home_request()


@app.route('/download/<file_name>')
def download(file_name):
    return views.download.handle_download_request(file_name)


@app.route('/verify/<file_name>')
def verify(file_name):
    return views.verify.handle_verify_request(file_name)


def run():
    app.run()

if __name__ == '__main__':
    run()
