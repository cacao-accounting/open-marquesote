# open-marquesote
Minimal PyQtWebEngine web browser useful to serve python web apps in desktop.

![Preview](https://raw.githubusercontent.com/cacao-accounting/open-marquesote/main/preview.JPG)

Live sample can be found at [Cacao Accounting Desktop](https://github.com/cacao-accounting/cacao-accounting-desktop/blob/master/cacao_desktop.py),
just replace the app to be served with your own project, please note that we recomend the [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/arguments.html#arguments) WSGI server
since it is croos plataform, [Gunicorn](https://gunicorn.org/) olny runs in Unix.

## Example

```python
# example.py
import subprocess
import time
from sys import argv, executable
from flask import Flask
from PyQt5.QtWidgets import QApplication
from open_marquesote import MainWindow
from waitress import serve

flaskapp = Flask(__name__)


@flaskapp.route("/")
def app():
    return "A python web app running like desktop app."


def server():
    try:
        serve(flaskapp, threads=2, port=9889)
    except OSError:
        # If the server was started before and is still running there will be a OSError: [Errno 98] Address already in use
        # Since the server is already up and running we pass this error.
        pass


def browser():
    time.sleep(5)  # Give 5 seconds to the WSGI server to start.
    browser = QApplication(argv)
    window = MainWindow(url="http://127.0.0.1:9889/", appname="Python web in Desktop")
    browser.exec_()


def run():
    subprocess.Popen(
        [executable, "-c", "import example; example.server()"],
        stderr=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
    )
    subprocess.Popen([executable, "-c", "import example; example.browser()"])


if __name__ == "__main__":
    run()
```

```bash
pip install -r requirements.txt
pip install flask
python example
```
![Preview](https://raw.githubusercontent.com/cacao-accounting/open-marquesote/main/example.JPG)


## License

Copyright 2017 Martin Fitzpatrick
Copyright 2020 William Moreno Reyes

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
THE USE OR OTHER DEALINGS IN THE SOFTWARE.
