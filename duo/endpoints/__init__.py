from duo.endpoints.product.controller.product_controller import product_router
from duo.endpoints.session.controller.session_controller import session_router
from duo.endpoints.user.controller.user_controller import user_router

from fastapi import FastAPI


app = FastAPI()

app.include_router(user_router)
app.include_router(session_router)
app.include_router(product_router)