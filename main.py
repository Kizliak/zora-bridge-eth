from web3 import Web3
from loguru import logger
from sys import stderr
from tqdm import tqdm
import random, time

######################### Settings ###############################################################
rpc = 'https://rpc.ankr.com/eth'    # Any Ethereum RPC https://chainlist.org/chain/1
delay_wallets = [900, 1800]         # wait seconds between wallets min and max
min_amount_for_bridge = 0.0069      # min amount to bridge ETH
max_amount_for_bridge = 0.0072      # max amount to bridge ETH
max_gas_in_gwei = 8                 # Max gas price in gwei. If current is higher script will wait
##################################################################################################

bridge_address = Web3.to_checksum_address('0x1a0ad011913a150f69f6a19df447a0cfd9551054')
bridge_abi = '[{"inputs":[{"internalType":"contract L2OutputOracle","name":"_l2Oracle","type":"address"},{"internalType":"address","name":"_guardian","type":"address"},{"internalType":"bool","name":"_paused","type":"bool"},{"internalType":"contract SystemConfig","name":"_config","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"uint8","name":"version","type":"uint8"}],"name":"Initialized","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Paused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":true,"internalType":"uint256","name":"version","type":"uint256"},{"indexed":false,"internalType":"bytes","name":"opaqueData","type":"bytes"}],"name":"TransactionDeposited","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"account","type":"address"}],"name":"Unpaused","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"withdrawalHash","type":"bytes32"},{"indexed":false,"internalType":"bool","name":"success","type":"bool"}],"name":"WithdrawalFinalized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"bytes32","name":"withdrawalHash","type":"bytes32"},{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"}],"name":"WithdrawalProven","type":"event"},{"inputs":[],"name":"GUARDIAN","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"L2_ORACLE","outputs":[{"internalType":"contract L2OutputOracle","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"SYSTEM_CONFIG","outputs":[{"internalType":"contract SystemConfig","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_to","type":"address"},{"internalType":"uint256","name":"_value","type":"uint256"},{"internalType":"uint64","name":"_gasLimit","type":"uint64"},{"internalType":"bool","name":"_isCreation","type":"bool"},{"internalType":"bytes","name":"_data","type":"bytes"}],"name":"depositTransaction","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"donateETH","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"target","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"gasLimit","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct Types.WithdrawalTransaction","name":"_tx","type":"tuple"}],"name":"finalizeWithdrawalTransaction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"finalizedWithdrawals","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"bool","name":"_paused","type":"bool"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_l2OutputIndex","type":"uint256"}],"name":"isOutputFinalized","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"l2Sender","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint64","name":"_byteCount","type":"uint64"}],"name":"minimumGasLimit","outputs":[{"internalType":"uint64","name":"","type":"uint64"}],"stateMutability":"pure","type":"function"},{"inputs":[],"name":"params","outputs":[{"internalType":"uint128","name":"prevBaseFee","type":"uint128"},{"internalType":"uint64","name":"prevBoughtGas","type":"uint64"},{"internalType":"uint64","name":"prevBlockNum","type":"uint64"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"pause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"paused","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"uint256","name":"nonce","type":"uint256"},{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"target","type":"address"},{"internalType":"uint256","name":"value","type":"uint256"},{"internalType":"uint256","name":"gasLimit","type":"uint256"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct Types.WithdrawalTransaction","name":"_tx","type":"tuple"},{"internalType":"uint256","name":"_l2OutputIndex","type":"uint256"},{"components":[{"internalType":"bytes32","name":"version","type":"bytes32"},{"internalType":"bytes32","name":"stateRoot","type":"bytes32"},{"internalType":"bytes32","name":"messagePasserStorageRoot","type":"bytes32"},{"internalType":"bytes32","name":"latestBlockhash","type":"bytes32"}],"internalType":"struct Types.OutputRootProof","name":"_outputRootProof","type":"tuple"},{"internalType":"bytes[]","name":"_withdrawalProof","type":"bytes[]"}],"name":"proveWithdrawalTransaction","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"name":"provenWithdrawals","outputs":[{"internalType":"bytes32","name":"outputRoot","type":"bytes32"},{"internalType":"uint128","name":"timestamp","type":"uint128"},{"internalType":"uint128","name":"l2OutputIndex","type":"uint128"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"unpause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"stateMutability":"payable","type":"receive"}]'

logger.remove()
logger.add(stderr, level=5, format="<lm>{time:YYYY-MM-DD HH:mm:ss}</lm> | <level>{level: <11}</level>| <cyan>{line: <3}</cyan>:<cyan>{function: <25}</cyan> | <lw>{message}</lw>")

# Functions

def sleeping(x):
    for i in tqdm(range(x), desc='sleep ', bar_format='{desc}: {n_fmt}/{total_fmt}'):
        time.sleep(1)

def bridgeFlow(address, private_key, w3_eth) -> None:
    bridge_status = False
    try:
        bridge_status = bridge_start(address, private_key, w3_eth)
    except Exception as e:
        logger.error(f'{address} - {e}')
        with open('failed_wallets.txt', 'a') as file:
            file.write(f'{address}\n')

    if bridge_status == True:
        with open('success_wallets.txt', 'a') as file:
            file.write(f'{address}\n')
    else:
        with open('failed_wallets.txt', 'a') as file:
            file.write(f'{address}\n')

def bridge_start(address, private_key, w3_eth) -> bool:

    balance_eth_in_wei = w3_eth.eth.get_balance(Web3.to_checksum_address(address))

    while True:
        gas_price = w3_eth.from_wei(w3_eth.eth.gas_price, 'gwei')

        if gas_price < float(max_gas_in_gwei):
            logger.info(f'Gas price is {gas_price} < {max_gas_in_gwei} gwei from settings.')
            break
        logger.info(f'Gas price: {gas_price} > {max_gas_in_gwei} gwei from settings')
        time.sleep(15)

    random_number = round(random.uniform(float(min_amount_for_bridge), float(max_amount_for_bridge)), 6)
    bridge_amount_in_wei = Web3.to_wei(random_number, 'ether')

    bridge_status = bridge_from_eth_to_zora(
        address=       Web3.to_checksum_address(address), 
        private_key=   private_key, 
        bridge_amount= bridge_amount_in_wei,
        w3_eth=        w3_eth)

    return bridge_status

def bridge_from_eth_to_zora(address, private_key, bridge_amount, w3_eth)-> bool:

    bridge_contract = w3_eth.eth.contract(address=bridge_address, abi=bridge_abi)
    gas = bridge_contract.functions.depositTransaction(
        address,
        bridge_amount,
        100000,
        False,
        Web3.to_bytes(text='')
    ).estimate_gas({
        'from':  address, 
        'value': bridge_amount, 
        'nonce': w3_eth.eth.get_transaction_count(address)
    })

    gas = int(gas * 1.2)

    if (gas + bridge_amount) > w3_eth.eth.get_balance(address):
        logger.error(f'{address} - Insufficient funds including gas.')
        return False

    tx_raw = bridge_contract.functions.depositTransaction(
        address,
        bridge_amount,
        100000,
        False,
        Web3.to_bytes(text='')
    ).build_transaction({
        'from':     address,
        'value':    bridge_amount,
        'gas':      gas,
        'gasPrice': w3_eth.eth.gas_price,
        'nonce':    w3_eth.eth.get_transaction_count(address)
    })

    signed_tx = w3_eth.eth.account.sign_transaction(tx_raw, private_key)
    raw_tx_hash = w3_eth.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_hash = w3_eth.to_hex(raw_tx_hash)
        
    tx_receipt = w3_eth.eth.wait_for_transaction_receipt(raw_tx_hash, timeout=600)
    if tx_receipt.status == 1:
        logger.success(f'Bridge done https://etherscan.io/tx/{tx_hash}')
        status = 1
        return True
    else:
        time.sleep(20)
        tx_receipt = w3_eth.eth.get_transaction_receipt(tx_hash)
        status = tx_receipt.status
        if status == 1:
            logger.success(f'{address} bridge done - https://etherscan.io/tx/{tx_hash}')
            return True
        else:
            logger.error(f'{address} bridge failed - https://etherscan.io/tx/{tx_hash}')
            return False
    return False

if __name__ == '__main__':

    with open('wallets.txt', 'r') as file:     #privatekey в файл wallets.txt
        wallets = [row.strip() for row in file]
    with open('failed_wallets.txt', 'w') as file:
        pass
    with open('success_wallets.txt', 'w') as file:
        pass
    
    w3_eth = Web3(Web3.HTTPProvider(rpc))
    print(f'Total wallets: {len(wallets)}\n')

    count_wallets = len(wallets)
    number_wallets = 0

    while wallets:
        number_wallets += 1
        private_key = wallets.pop(0)
        address = w3_eth.eth.account.from_key(private_key).address
        print(f'{number_wallets}/{count_wallets} - {address}\n')

        bridgeFlow(address, private_key, w3_eth)

        if number_wallets != count_wallets:
            sleeping(random.randint(delay_wallets[0], delay_wallets[1]))
        print()
        
    print(input(f'More web3 scripts: https://t.me/legalcrypt'))
