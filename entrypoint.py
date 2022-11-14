import config

from main import app

##################################################
# project main entrypoint
##################################################


if __name__ == "__main__":
    # run Flask App
    app.run(debug=True, port=config.server_port, host="0.0.0.0", use_reloader=True)
