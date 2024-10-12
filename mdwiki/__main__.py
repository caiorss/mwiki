from mdwiki.server import app

if __name__ == '__main__':
    print(" [TRACE] Server started Ok.")
    app.run(host='0.0.0.0', port=8010, debug=True)
