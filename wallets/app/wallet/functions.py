from ..wallet.configuration import (
    Configuration,
)
from web3.exceptions import (
    InvalidAddress,
)
from ..wallet.exceptions import (
    InfuraErrorException,
    InvalidPasswordException,
    InsufficientFundsException,
    InvalidValueException,
    InvalidPasswordException,
    InfuraErrorException,
    ERC20NotExistsException,
    InsufficientERC20FundsException,
)
from ..wallet.api import (
    WalletAPI,
)


def get_api():
    return WalletAPI()


def remove_token(symbol, user_id):
    """Add new ERC20 contract."""
    configuration = Configuration().load_configuration(user_id)
    api = get_api()
    error = None

    # fitcoin_address = '0x19896cB57Bc5B4cb92dbC7D389DBa6290AF505Ce'
    try:
        api.remove_contract(configuration, symbol)
        return "New coin was added! %s %s" % (symbol), True
    except InvalidAddress:
        error = "Invalid address or wallet does not exist!"
    except InfuraErrorException:
        error = "Wallet is not connected to Ethereum network!"

    return error, False


def add_token(contract, symbol, user_id):
    """Add new ERC20 contract."""
    configuration = Configuration().load_configuration(user_id)
    api = get_api()
    error = None

    # fitcoin_address = '0x19896cB57Bc5B4cb92dbC7D389DBa6290AF505Ce'
    try:
        api.add_contract(configuration, symbol, contract)
        return "New coin was added! %s %s" % (symbol, contract), True
    except InvalidAddress:
        error = "Invalid address or wallet does not exist!"
    except InfuraErrorException:
        error = "Wallet is not connected to Ethereum network!"

    return error, False


def get_balance(token=None, user_id=None):
    """Get address balance."""
    configuration = Configuration().load_configuration(user_id)
    api = get_api()
    eth_balance = None
    token_balance = None
    try:
        if token is None:
            eth_balance, address = api.get_balance(configuration)
            return eth_balance, address
        else:
            token_balance, address = api.get_balance(configuration, token)
            return token_balance, address
    except InvalidAddress:
        error = "Invalid address or wallet does not exist!"
    except InfuraErrorException:
        error = "Wallet is not connected to Ethereum network!"
    except ERC20NotExistsException:
        error = "This token is not added to the wallet!"

    return error, False


def get_wallet(user_id):
    """Get wallet account from encrypted keystore."""
    configuration = Configuration().load_configuration(user_id)
    api = get_api()

    address, pub_key = api.get_wallet(configuration)

    return {"address": address, "pKey": pub_key}


def list_tokens(user_id):
    """List all added tokens."""
    configuration = Configuration().load_configuration(user_id)
    api = get_api()

    return api.list_tokens(configuration)


def network(user_id):
    """Get connected network (Mainnet, Ropsten) defined in EIP155."""
    configuration = Configuration().load_configuration(user_id)
    api = get_api()
    chain_id = api.get_network(configuration)
    if chain_id == 1:
        return "You are connected to the Mainnet network!"
    if chain_id == 3:
        return "You are connected to the Testnet network!"


def new_wallet(user_id, passphrase):
    """Creates new wallet and store encrypted keystore file."""
    # password = getpass.getpass(
    #     "Passphrase from keystore: "
    # )  # Prompt the user for a password of keystore file

    configuration = Configuration().load_configuration(user_id)

    api = get_api()
    wallet = api.new_wallet(configuration, passphrase)

    return {
        "address": wallet.get_address(),
        "pKey": wallet.get_public_key(),
        "mnemonic": wallet.get_mnemonic(),
    }


def load_wallet(user_id, private_key, passphrase):
    """Creates new wallet and store encrypted keystore file."""
    # password = getpass.getpass(
    #     "Passphrase from keystore: "
    # )  # Prompt the user for a password of keystore file

    configuration = Configuration().load_configuration(user_id)

    api = get_api()
    wallet = api.load_wallet(configuration, private_key, passphrase)

    return {
        "address": wallet.get_address(),
        "pKey": wallet.get_public_key(),
        "mnemonic": wallet.get_mnemonic(),
    }


def restore_wallet(mnemonic_sentence, passphrase, user_id):
    """Creates new wallet and store encrypted keystore file."""
    # passphrase = getpass.getpass(
    #     "Passphrase: "
    # )  # Prompt the user for a password of keystore file

    configuration = Configuration().load_configuration(user_id)

    api = get_api()
    wallet = api.restore_wallet(configuration, mnemonic_sentence, passphrase)

    # print("Account address: %s" % str(wallet.get_address()))
    # print("Account pub key: %s" % str(wallet.get_public_key()))
    # print(
    #     "Keystore path: %s" % configuration.keystore_location
    #     + configuration.keystore_filename
    # )
    # print("Remember these words to restore eth-wallet: %s" % wallet.get_mnemonic())
    return {
        "address": wallet.get_address(),
        "pKey": wallet.get_public_key(),
        "mnemonic": wallet.get_mnemonic(),
    }


def reveal_seed(user_id, password):
    """Reveals private key from encrypted keystore."""
    # password = getpass.getpass(
    #     "Password from keystore: "
    # )  # Prompt the user for a password of keystore file

    configuration = Configuration().load_configuration(user_id)
    api = get_api()

    try:
        wallet = api.get_private_key(configuration, password)
        return {"private_key": str(wallet.get_private_key().hex())}
        # print("Account prv key: %s" % str(wallet.get_private_key().hex()))

    except InvalidPasswordException:
        return {"detail": "Incorrect password!"}

    return None


def send_transaction(to, value, user_id, password, token):
    """Sends transaction."""
    # password = getpass.getpass(
    #     "Password from keystore: "
    # )  # Prompt the user for a password of keystore file

    configuration = Configuration().load_configuration(user_id)
    api = get_api()
    error = {}
    try:
        if token is None:
            # send ETH transaction
            tx_hash, tx_cost_eth = api.send_transaction(
                configuration, password, to, value
            )
        else:
            # send erc20 transaction
            tx_hash, tx_cost_eth = api.send_transaction(
                configuration, password, to, value, token
            )

        return {
            "hash": tx_hash.hex(),
            "cost": str(tx_cost_eth),
        }

    except InsufficientFundsException:
        error = {"detail": "Insufficient ETH funds! Check balance on your address."}
    except InsufficientERC20FundsException:
        error = {
            "detail": "Insufficient ERC20 token funds! Check balance on your address."
        }
    except InvalidAddress:
        error = {"detail": "Invalid recipient(to) address!"}
    except InvalidValueException:
        error = {"detail": "Invalid value to send!"}
    except InvalidPasswordException:
        error = {"detail": "Incorrect password!"}
    except InfuraErrorException:
        error = {"detail": "Wallet is not connected to Ethereum network!"}
    except ERC20NotExistsException:
        error = {"detail": "This token is not added to the wallet!"}

    return error
