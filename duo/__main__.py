from duo.config.config_runner import ConfigRunner
from duo.endpoints import app

import uvicorn


def main():
    ConfigRunner.run()

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
