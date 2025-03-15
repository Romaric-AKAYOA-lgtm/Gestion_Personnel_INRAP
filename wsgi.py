import importlib
application = importlib.import_module('app').__path__()

from waitress import serve

if __name__ == "__main__":
    serve(application, host='0.0.0.0', port=8000)
