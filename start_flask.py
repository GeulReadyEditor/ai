from flaskapp import app


if __name__ == '__main__':
    app.run(host= 'localhost',
            port= 2727,
            debug= True)