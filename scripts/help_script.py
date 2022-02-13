from brownie import network, accounts, config
import eth_utils

NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "hardhat",
    "development",
    "ganache",
]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = (
    NON_FORKED_LOCAL_BLOCKCHAIN_ENVIRONMENTS
    + [
        "mainnet-fork",
        "binance-fork",
        "matic-fork",
    ]
)


def get_account(number=None):
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if number:
        return accounts[number]
    if network.show_active() in config["networks"]:
        account = accounts.from_mnemonic(
            mnemonic=config["wallets"]["from_mnemonic"], count=5
        )
        return account
    return None


def encode_function_data(initializer=None, *args):
    """Encodes the function call so we can work with an initializer.

    Args:
        initializer ([brownie.network.contract.ContractTx], optional):
        The initializer function we want to call. Example: `box.store`.
        Defaults to None.

        args (Any, optional):
        The arguments to pass to the initializer function

    Returns:
        [bytes]: Return the encoded bytes.
    """
    if not len(args):
        args = b""

    if initializer:
        return initializer.encode_input(*args)

    return b""
