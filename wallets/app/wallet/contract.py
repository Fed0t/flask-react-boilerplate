import time
from ..wallet.infura import (
    Infura,
)
from ..wallet.utils import (
    get_abi_json,
)


class Contract:
    """Abstraction over ERC20 tokens"""

    # fitcoin_address = '0x19896cB57Bc5B4cb92dbC7D389DBa6290AF505Ce'
    # binancecoin_address = '0x64BBF67A8251F7482330C33E65b08B835125e018'
    # my_address = '0xc3519C4560BcfE3Ac0b137f1067d1655ed65FEa4'
    # metamask_address = '0xAAD533eb7Fe7F2657960AC7703F87E10c73ae73b'

    def __init__(self, configuration, address):
        """
        Constructor
        :param address: contract address or ESN name
        :type address: string
        """
        self.conf = configuration
        self.address = address

        self.w3 = Infura().get_web3()
        if address == "0x6D5bfD02b543e7D49f88Fe78628A42Ac815D46f2":
            self.contract = self.w3.eth.contract(address=address, abi=get_abi_json())
        else:
            self.contract = self.w3.eth.contract(address=address, abi=get_abi_json())
        self.contract_decimals = self.contract.functions.decimals().call()

    def add_new_contract(self, contract_symbol, contract_address):
        """
        Add ERC20 token to the wallet
        :param contract_symbol: token symbol
        :param contract_address: contract address
        :return:
        """

        self.conf.add_contract_token(contract_symbol, contract_address)

    def get_balance(self, wallet_address):
        """
        Get wallet's ballance of self.contract
        :param wallet_address: this wallet address
        :type wallet_address: string
        :return: balance as decimal number
        """
        return self.contract.functions.balanceOf(wallet_address).call() / (
            10 ** self.contract_decimals
        )

    def get_decimals(self):
        """
        Returns the number of decimals
        :return: integer
        """
        return self.contract_decimals

    def get_erc20_contract(self):
        """
        Returns w3.eth.contract instance
        :return:
        """
        return self.contract
