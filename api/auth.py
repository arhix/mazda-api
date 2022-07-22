from typing import Optional
from apiflask import HTTPTokenAuth
from jose import JWTError, jwt

from schemas import MazdaAuth


class JWTAuth(HTTPTokenAuth):
    def __init__(self,
                 secret_key,
                 scheme: str = 'Bearer',
                 realm: Optional[str] = None,
                 header: Optional[str] = None,
                 description: Optional[str] = None
                 ) -> None:
        super().__init__(scheme=scheme, realm=realm, header=header, description=description)
        self.secret_key = secret_key
        self.verify_token_callback = self.__verify

    def __verify(self, token) -> MazdaAuth:
        try:
            data = self.decode(token)
        except JWTError:
            return False
        return MazdaAuth().load(data)

    def decode(self, data: MazdaAuth) -> str:
        return jwt.decode(data, self.secret_key, algorithms='HS256')

    def encode(self, data: MazdaAuth) -> str:
        # TODO: add expiration date
        return jwt.encode(data, self.secret_key, algorithm='HS256')
