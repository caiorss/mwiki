from mdwiki.server import *

if __name__ == '__main__':
    print(" [TRACE] Server started Ok.")
    run(host='0.0.0.0', port=8060, debug=True)
