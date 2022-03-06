from cli import init_db
from cli import app

import sys

def start():
    app.run("0.0.0.0", debug=True, port=7000)

def init():
    init_db(app)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "start":
            start()
        elif command == "init":
            init()
    else:
        print("usage:\n\n\trun.py [ start | init ]")