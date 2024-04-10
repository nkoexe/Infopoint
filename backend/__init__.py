import logging

logging.basicConfig(level=logging.INFO)

logging.getLogger("geventwebsocket.handler").setLevel(logging.WARNING)

from app import app, socketio


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, log_output=False)
