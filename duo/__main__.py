from duo.config.config_runner import ConfigRunner
from duo.controller.product_controller import product_router
from duo.controller.session_controller import session_router
from duo.controller.user_controller import user_router

from fastapi import FastAPI
import uvicorn


def main():

    ConfigRunner.run()

    app = FastAPI()
    app.include_router(user_router)
    app.include_router(session_router)
    app.include_router(product_router)

    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
