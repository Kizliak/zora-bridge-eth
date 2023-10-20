# Zora-bridge-eth
Bridge ETH from Ethereum network to Zora mainnet. Features:
- check current gwei gas price in Ethereum network and wait for lower if needed.
- write all success and failed wallets to files failed_wallets.txt / success_wallets.txt
- simple code, easy to audit

## Installation

Download script:
```
apt install python3-pip, git
git clone https://github.com/Kizliak/zora-bridge-eth
cd zora-bridge-eth
```
Install libraries:
```
sudo apt-get update \
&& sudo apt-get install python3-venv git -y \
&& python3 -m venv venv \
&& source ./venv/bin/activate \
&& pip3 install -r requirements.txt
```

Add private keys:
```
nano pwallets.txt
```
and edit settings in main.py

Run script:
```
python3 main.py
```
