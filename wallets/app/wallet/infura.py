from web3 import (
    Web3,
    HTTPProvider,
)
from ..wallet.exceptions import InfuraErrorException


class Infura:
    """Abstraction over Infura node connection."""

    def __init__(self):
        self.w3 = Web3(HTTPProvider("https://mainnet.aurora.dev/"))

    def get_web3(self):
        if not self.w3.isConnected():
            raise InfuraErrorException()

        return self.w3
