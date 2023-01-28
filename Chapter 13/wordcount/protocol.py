# -*- coding: utf-8 -*-
import os
import asyncio
import pickle
import typing as T
from abc import abstractmethod, ABC

FileWithId = T.Optional[T.Tuple[int, str]]

PORT = 8888
HOST = "localhost"
TEMP_DIR = "temp"
END_MSG = b"EOF"
RESULT_FILENAME = "result.json"


class Protocol(asyncio.Protocol, ABC):
    def __init__(self) -> None:
        super().__init__()
        self.buffer = b""
        self.transport: T.Optional[asyncio.BaseTransport] = None

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        self.transport = transport
        print("Connection made.")

    def data_received(self, data: bytes) -> None:
        self.buffer = self.buffer + data # accumulate message parts
        if END_MSG in self.buffer:       # message complete
            if b":" not in data:
                command = self.buffer.split(END_MSG, 1)[0]
                self.process_command(command)
            else:
                command, data = self.buffer.split(b":", 1)
                data = data.split(END_MSG, 1)[0]
                data = pickle.loads(data)
                self.process_command(command, data)

    def send_command(self, command, data: FileWithId = None) -> None:
        if data:
            pdata = pickle.dumps(data)
            self.transport.write(command + b":" + pdata + END_MSG)
        else:
            self.transport.write(command + END_MSG)

    def get_temp_dir(self) -> str:
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, TEMP_DIR)

    def get_result_filename(self) -> str:
        dirname = os.path.dirname(__file__)
        return os.path.join(dirname, RESULT_FILENAME)

    @abstractmethod
    def process_command(self, command: bytes, data: FileWithId = None) -> None:
        pass
