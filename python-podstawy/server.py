from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()



# to run server on http://localhost:8004: waitress-serve --port=8004 server:app