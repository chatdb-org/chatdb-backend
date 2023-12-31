""" This module is the entry point of the application. """

# pylint: disable=import-error
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import router


class ChatDB(FastAPI):
    """ This class is the entry point of the application. """
    def __init__(self):
        super().__init__()
        self.include_router(router)
        self.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )
