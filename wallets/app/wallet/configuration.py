from ..main.database import db
from ..utils import JSONEncoder
import json


class Configuration:
    """
    Module for working with configuration file.
    """

    # Networks defined in https://github.com/ethereum/EIPs/blob/master/EIPS/eip-155.md#specification
    MAIN_NETWORK_ID = 1
    RINKEBY_NETWORK_ID = 4
    AURORA_NETWORK_ID = 1313161555

    # Default configuration yaml file will be created from this dictionary
    initial_config = dict(
        eth_address="",
        public_key="",
        network=AURORA_NETWORK_ID,  # default network where to connect app
        contracts=dict(),
    )

    def __init__(
        self,
        initial_config=initial_config,
    ):

        # default class paths can be override in test within constructor
        self.initial_config = initial_config

        # Variables from configuration file. They will be initialized after load_configuration() call
        self.network = ""
        self.eth_address = ""
        self.public_key = ""
        self.user_id = ""
        self.contracts = dict()

    def is_configuration(self):
        """Checks if exists configuration on default path"""
        check = db.cold_wallets.find_one({"user_id": self.user_id})
        return check is not None

    def load_configuration(self, user_id):
        """Load bot configuration from .yaml file"""
        self.initial_config["user_id"] = user_id
        check = db.cold_wallets.find_one({"user_id": user_id})
        if check is None:
            self.create_empty_configuration(user_id)
            self.load_configuration(user_id)

        else:
            data = json.loads(JSONEncoder().encode(check))
            for key, value in data.items():
                if key != "_id":
                    setattr(self, key, value)
            if self.network == 4:
                self.__update_configuration("network", self.AURORA_NETWORK_ID)
                self.network = self.AURORA_NETWORK_ID
            if "SLBZ" not in self.contracts:
                self.add_contract_token(
                    "SLBZ", "0x6D5bfD02b543e7D49f88Fe78628A42Ac815D46f2"
                )
        return self

    def create_empty_configuration(self, user_id):
        """
        Creates and initialize empty configuration file
        :return: True if config file created successfully
        """
        data = self.initial_config.copy()
        wallet = db.cold_wallets.insert_one(data)

        return True

    def update_eth_address(self, eth_address):
        """
        Update and save eth address to configuration
        :param eth_address: eth address to save
        :return:
        """
        self.eth_address = eth_address
        self.__update_configuration("eth_address", eth_address)

    def update_public_key(self, public_key):
        """
        Update and save public key to configuration
        :param public_key: public key to save
        :return:
        """
        self.public_key = public_key
        self.__update_configuration("public_key", public_key)

    def add_contract_token(self, contract_symbol, contract_address):
        """
        Add ERC20 token to the wallet
        :param contract_symbol: token symbol
        :param contract_address: contract address
        :return:
        """
        self.contracts[contract_symbol] = contract_address
        self.__update_configuration("contracts", self.contracts)

    def remove_contract_token(self, contract_symbol):
        """
        Add ERC20 token to the wallet
        :param contract_symbol: token symbol
        :return:
        """
        if contract_symbol in self.contracts:
            del self.contracts[contract_symbol]
            self.__update_configuration("contracts", self.contracts)

    def __update_configuration(self, parameter_name, parameter_value):
        """
        Updates configuration file.
        :param parameter_name: parameter name to change or append
        :param parameter_value: value to parameter_key
        :return: True if config file updated successfully
        """
        db.cold_wallets.update_one(
            {"user_id": self.initial_config["user_id"]},
            {"$set": {parameter_name: parameter_value}},
        )

        return True
