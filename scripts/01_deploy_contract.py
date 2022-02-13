from brownie import (
    BankV1,
    TransparentUpgradeableProxy,
    ProxyAdmin,
    config,
    network,
    Contract,
    Wei,
    web3,
)
from scripts.help_script import get_account, encode_function_data

# Uncomment for devnet
def main():
    admin = get_account()
    account1 = get_account(1)
    print(f"Deploying Bank Contract to {network.show_active()}")
    bank = BankV1.deploy({"from": admin})
    bank_encode_function = encode_function_data()
    print(f"Deploying ProxyAdmin Contract to {network.show_active()}")
    proxy_admin = ProxyAdmin.deploy({"from": admin})
    print(f"Deploying Proxy Contract to {network.show_active()}")
    proxy = TransparentUpgradeableProxy.deploy(
        bank.address,
        proxy_admin.address,
        bank_encode_function,
        {"from": admin},
    )
    print(f"Proxy Contract deployed at {proxy}")
    proxy_bank = Contract.from_abi(
        "BankV1",
        proxy.address,
        BankV1.abi,
    )
    print(f"Deposit 20 ETH from {account1} to {proxy_bank}")
    proxy_bank.deposit({
        "from":account1,
        "amount":Wei("20 ether")
    })
    balance = proxy_bank.balances.call(account1)
    print(f"{account1} Deposit Balance : {web3.fromWei(balance, 'ether')} ETH")

# Uncomment for testnet ropsten
# def main():
#     account = get_account()
#     print(f"Deploying Bank Contract to {network.show_active()}")
#     bank = BankV1.deploy(
#         {
#             "from": account[0],
#             "gas_limit": 500000,
#             "priority_fee": Wei("2 gwei"),
#         },
#         publish_source=config["networks"][network.show_active()][
#             "verify"
#         ],
#     )
#     bank_encode_function = encode_function_data()
#     print(f"Deploying ProxyAdmin Contract to {network.show_active()}")
#     proxy_admin = ProxyAdmin.deploy(
#         {
#             "from": account[0],
#             "gas_limit": 500000,
#             "priority_fee": Wei("2 gwei"),
#         },
#         publish_source=config["networks"][network.show_active()][
#             "verify"
#         ],
#     )
#     print(f"Deploying Proxy Contract to {network.show_active()}")
#     proxy = TransparentUpgradeableProxy.deploy(
#         bank.address,
#         proxy_admin.address,
#         bank_encode_function,
#         {
#             "from": account[0],
#             "gas_limit": 6000000,
#             "priority_fee": Wei("2 gwei"),
#         },
#         publish_source=config["networks"][network.show_active()][
#             "verify"
#         ],
#     )
#     proxy_bank = Contract.from_abi("BankV1", proxy.address, BankV1.abi)
#     print(f"Deposit 0.002 ETH from {account[0]} to {proxy_bank}")
#     proxy_bank.deposit({
#         "from":account[0],
#         "amount":Wei("0.002 ether"),
#         "gas_limit": 500000,
#         "priority_fee": Wei("2 gwei"),
#     })
