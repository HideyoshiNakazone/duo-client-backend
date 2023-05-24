from duo.depends.depends_session import get_session_service
from duo.endpoints.session.service.session_service import SessionService

from fastapi_utils.inferring_router import InferringRouter
from fastapi_utils.cbv import cbv
from fastapi import Depends, Request, Response

session_router = InferringRouter()


@cbv(session_router)
class SessionController:
    session_service: SessionService = Depends(get_session_service, use_cache=True)

    @session_router.get("/session", status_code=200)
    def get_session(self, request: Request, response: Response):
        return self.session_service.from_request(request, response) \
            .get_user_info()

    @session_router.delete("/session", status_code=204)
    def remove_session(self, request: Request, response: Response):
        self.session_service.from_request(request, response) \
            .remove_user_info()

    @session_router.get("/session/refresh", status_code=200)
    def refresh_session(self, request: Request, response: Response):
        return self.session_service.from_request(request, response) \
            .refresh_session()
