import os
import json
import time
import asyncio
import random
import hashlib
import base64
from dotenv import load_dotenv
from web3 import AsyncWeb3, AsyncHTTPProvider
from web3.eth import AsyncEth
from eth_account import Account
import aiohttp
import aiofiles

load_dotenv()
class Colors:
    RESET = "\033[0m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    WHITE = "\033[37m"
    GRAY = "\033[90m"
    BOLD = "\033[1m"
class Logger:
    @staticmethod
    def info(msg): print(f"{Colors.GREEN}[✓] {msg}{Colors.RESET}")
    @staticmethod
    def warn(msg): print(f"{Colors.YELLOW}[⚠] {msg}{Colors.RESET}")
    @staticmethod
    def error(msg): print(f"{Colors.RED}[✗] {msg}{Colors.RESET}")
    @staticmethod
    def success(msg): print(f"{Colors.GREEN}[✅] {msg}{Colors.RESET}")
    @staticmethod
    def loading(msg): print(f"{Colors.CYAN}[⟳] {msg}{Colors.RESET}")
    @staticmethod
    def process(msg): print(f"\n{Colors.WHITE}[➤] {msg}{Colors.RESET}")
    @staticmethod
    def debug(msg): print(f"{Colors.GRAY}[…] {msg}{Colors.RESET}")
    @staticmethod
    def critical(msg): print(f"{Colors.RED}{Colors.BOLD}[❌] {msg}{Colors.RESET}")
    @staticmethod
    def summary(msg): print(f"{Colors.WHITE}[✓] {msg}{Colors.RESET}")
    @staticmethod
    def section(msg=None):
        line = "=" * 50
        print(f"\n{Colors.CYAN}{line}{Colors.RESET}")
        if msg: print(f"{Colors.CYAN}{msg}{Colors.RESET}")
        print(f"{Colors.CYAN}{line}{Colors.RESET}\n")
    @staticmethod
    def banner():
        print(f"{Colors.CYAN}{Colors.BOLD}")
        print("██╗  ██╗███████╗██╗  ██╗ ██████╗ ██╗   ██╗ █████╗ ███╗   ██╗████████╗")
        print("██║  ██║██╔════╝╚██╗██╔╝██╔═══██╗██║   ██║██╔══██╗████╗  ██║╚══██╔══╝")
        print("███████║█████╗   ╚███╔╝ ██║   ██║██║   ██║███████║██╔██╗ ██║   ██║   ")
        print("██╔══██║██╔══╝   ██╔██╗ ██║▄▄ ██║██║   ██║██╔══██║██║╚██╗██║   ██║   ")
        print("██║  ██║███████╗██╔╝ ██╗╚██████╔╝╚██████╔╝██║  ██║██║ ╚████║   ██║   ")
        print("╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝ ╚══▀▀═╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ")
        print("                                                                     ")
        print("                           0G Storage                                ")
        print(f"{Colors.RESET}\n")


CHAIN_ID = 80087
RPC_URL = 'https://evmrpc-testnet.0g.ai'
CONTRACT_ADDRESS = '0x56A565685C9992BF5ACafb940ff68922980DBBC5'
METHOD_ID = '0xef3e12dc'
PROXY_FILE = 'proxies.txt'
INDEXER_URL = 'https://indexer-storage-testnet-turbo.0g.ai'
EXPLORER_URL = 'https://chainscan-galileo.0g.ai/tx/'
IMAGE_SOURCES = [
    {'url': 'https://picsum.photos/800/600'},
    {'url': 'https://loremflickr.com/800/600'}
]

class OGStorageBot:
    def __init__(self):
        self.private_keys = []
        self.proxies = []
        self.current_proxy_index = 0
        self.web3 = AsyncWeb3(AsyncHTTPProvider(RPC_URL), modules={'eth': (AsyncEth,)})
        
    def load_private_keys(self):
        """Load private keys from environment variables"""
        try:
            index = 1
            key = os.getenv(f"PRIVATE_KEY_{index}")
            if not key and index == 1 and os.getenv("PRIVATE_KEY"):
                key = os.getenv("PRIVATE_KEY")
                
            while key:
                if self.is_valid_private_key(key):
                    self.private_keys.append(key)
                else:
                    Logger.error(f"Invalid private key at PRIVATE_KEY_{index}")
                index += 1
                key = os.getenv(f"PRIVATE_KEY_{index}")
                
            if not self.private_keys:
                Logger.critical("No valid private keys found in .env file")
                exit(1)
                
            Logger.success(f"Loaded {len(self.private_keys)} private key(s)")
        except Exception as e:
            Logger.critical(f"Failed to load private keys: {str(e)}")
            exit(1)
            
    def is_valid_private_key(self, key):
        """Validate private key format"""
        key = key.strip()
        if not key.startswith("0x"):
            key = "0x" + key
        try:
            bytes_key = bytes.fromhex(key[2:])
            return len(key) == 66 and len(bytes_key) == 32
        except:
            return False
            
    def load_proxies(self):
        """Load proxies from file"""
        try:
            if os.path.exists(PROXY_FILE):
                with open(PROXY_FILE, 'r') as f:
                    self.proxies = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                
                if self.proxies:
                    Logger.info(f"Loaded {len(self.proxies)} proxies from {PROXY_FILE}")
                else:
                    Logger.warn(f"No proxies found in {PROXY_FILE}")
            else:
                Logger.warn(f"Proxy file {PROXY_FILE} not found")
        except Exception as e:
            Logger.error(f"Failed to load proxies: {str(e)}")
            
    def get_next_proxy(self):
        """Get next proxy in rotation"""
        if not self.proxies:
            return None
        proxy = self.proxies[self.current_proxy_index]
        self.current_proxy_index = (self.current_proxy_index + 1) % len(self.proxies)
        return proxy
        
    def get_random_user_agent(self):
        """Return a random user agent string"""
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:124.0) Gecko/20100101 Firefox/124.0'
        ]
        return random.choice(user_agents)
    
    async def check_network_sync(self):
        """Check if network is synced"""
        try:
            Logger.loading("Checking network sync...")
            block_number = await self.web3.eth.block_number
            Logger.success(f"Network synced at block {block_number}")
            return True
        except Exception as e:
            Logger.error(f"Network sync check failed: {str(e)}")
            return False
            
    async def fetch_random_image(self):
        """Fetch random image from sources"""
        try:
            Logger.loading("Fetching random image...")
            source = random.choice(IMAGE_SOURCES)
            headers = {'User-Agent': self.get_random_user_agent()}
            proxy = self.get_next_proxy()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(source['url'], headers=headers, proxy=proxy) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        Logger.success("Image fetched successfully")
                        return image_data
                    else:
                        raise Exception(f"HTTP error: {response.status}")
        except Exception as e:
            Logger.error(f"Error fetching image: {str(e)}")
            raise
            
    async def check_file_exists(self, file_hash):
        """Check if file hash already exists in storage"""
        try:
            Logger.loading(f"Checking file hash {file_hash}...")
            headers = {'User-Agent': self.get_random_user_agent()}
            proxy = self.get_next_proxy()
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"{INDEXER_URL}/file/info/{file_hash}", 
                    headers=headers, 
                    proxy=proxy
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get('exists', False)
                    return False
        except Exception as e:
            Logger.warn(f"Failed to check file hash: {str(e)}")
            return False
            
    async def prepare_image_data(self, image_buffer):
        """Prepare image data with unique hash"""
        MAX_HASH_ATTEMPTS = 5
        attempt = 1
        
        while attempt <= MAX_HASH_ATTEMPTS:
            try:
                salt = os.urandom(16).hex()
                timestamp = str(int(time.time() * 1000))
                hash_input = image_buffer + salt.encode() + timestamp.encode()
                file_hash = "0x" + hashlib.sha256(hash_input).hexdigest()
                file_exists = await self.check_file_exists(file_hash)
                if file_exists:
                    Logger.warn(f"Hash {file_hash} already exists, retrying...")
                    attempt += 1
                    continue
                image_base64 = base64.b64encode(image_buffer).decode('utf-8')
                Logger.success(f"Generated unique file hash: {file_hash}")
                
                return {
                    'root': file_hash,
                    'data': image_base64
                }
            except Exception as e:
                Logger.error(f"Error generating hash (attempt {attempt}): {str(e)}")
                attempt += 1
                if attempt > MAX_HASH_ATTEMPTS:
                    raise Exception(f"Failed to generate unique hash after {MAX_HASH_ATTEMPTS} attempts")
    
    async def upload_to_storage(self, image_data, wallet_address, private_key, wallet_index):
        """Upload file to storage and send transaction"""
        MAX_RETRIES = 3
        TIMEOUT_SECONDS = 300
        attempt = 1
        Logger.loading(f"Checking wallet balance for {wallet_address}...")
        balance = await self.web3.eth.get_balance(wallet_address)
        min_balance = self.web3.to_wei(0.0015, 'ether')
        if balance < min_balance:
            raise Exception(f"Insufficient balance: {self.web3.from_wei(balance, 'ether')} OG")
        
        Logger.success(f"Wallet balance: {self.web3.from_wei(balance, 'ether')} OG")
        
        while attempt <= MAX_RETRIES:
            try:
                Logger.loading(f"Uploading file for wallet #{wallet_index + 1} [{wallet_address}] (Attempt {attempt}/{MAX_RETRIES})...")
                headers = {
                    'User-Agent': self.get_random_user_agent(),
                    'Content-Type': 'application/json'
                }
                proxy = self.get_next_proxy()
                
                payload = {
                    'root': image_data['root'],
                    'index': 0,
                    'data': image_data['data'],
                    'proof': {
                        'siblings': [image_data['root']],
                        'path': []
                    }
                }
                
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{INDEXER_URL}/file/segment",
                        json=payload,
                        headers=headers,
                        proxy=proxy
                    ) as response:
                        if response.status != 200:
                            raise Exception(f"Upload failed with status: {response.status}")
                
                Logger.success("File segment uploaded")
                content_hash = os.urandom(32)
                tx_data = (
                    bytes.fromhex(METHOD_ID[2:]) +
                    bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000020") +
                    bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000014") +
                    bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000060") +
                    bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000080") +
                    bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000000") +
                    bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000001") +
                    content_hash +
                    bytes.fromhex("0000000000000000000000000000000000000000000000000000000000000000")
                )
                
                tx_value = self.web3.to_wei(0.000839233398436224, 'ether')
                gas_price = self.web3.to_wei(1.029599997, 'gwei')
                Logger.loading("Estimating gas...")
                try:
                    gas_estimate = await self.web3.eth.estimate_gas({
                        'to': CONTRACT_ADDRESS,
                        'data': tx_data.hex(),
                        'from': wallet_address,
                        'value': tx_value
                    })
                    gas_limit = int(gas_estimate * 1.5)
                    Logger.success(f"Gas limit set: {gas_limit}")
                except Exception as e:
                    gas_limit = 300000
                    Logger.warn(f"Gas estimation failed, using default: {gas_limit}")
                gas_cost = int(gas_price) * gas_limit
                required_balance = gas_cost + int(tx_value)
                if balance < required_balance:
                    raise Exception(f"Insufficient balance for transaction: {self.web3.from_wei(balance, 'ether')} OG")
                
                # Build and sign transaction
                Logger.loading("Sending transaction...")
                nonce = await self.web3.eth.get_transaction_count(wallet_address, 'latest')
                
                tx = {
                    'to': CONTRACT_ADDRESS,
                    'data': tx_data.hex(),
                    'value': tx_value,
                    'gas': gas_limit,
                    'gasPrice': gas_price,
                    'nonce': nonce,
                    'chainId': CHAIN_ID
                }
                
                signed_tx = self.web3.eth.account.sign_transaction(tx, private_key)
                tx_hash = await self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
                tx_hash_hex = tx_hash.hex()
                tx_link = f"{EXPLORER_URL}{tx_hash_hex}"
                Logger.info(f"Transaction sent: {tx_hash_hex}")
                Logger.info(f"Explorer: {tx_link}")
                Logger.loading(f"Waiting for confirmation ({TIMEOUT_SECONDS}s)...")
                
                try:
                    start_time = time.time()
                    receipt = None
                    
                    while receipt is None and (time.time() - start_time) < TIMEOUT_SECONDS:
                        try:
                            receipt = await self.web3.eth.get_transaction_receipt(tx_hash)
                            await asyncio.sleep(2)
                        except:
                            await asyncio.sleep(5)
                    
                    if receipt is None:
                        raise Exception(f"Timeout after {TIMEOUT_SECONDS} seconds")
                    
                except Exception as e:
                    if "Timeout" in str(e):
                        Logger.warn(f"Transaction timeout after {TIMEOUT_SECONDS}s")
                        receipt = await self.web3.eth.get_transaction_receipt(tx_hash)
                        if receipt and receipt.status == 1:
                            Logger.success(f"Late confirmation in block {receipt.blockNumber}")
                        else:
                            raise Exception(f"Transaction failed or pending: {tx_link}")
                    else:
                        raise
                
                if receipt.status == 1:
                    Logger.success(f"Transaction confirmed in block {receipt.blockNumber}")
                    Logger.success(f"File uploaded, root hash: {image_data['root']}")
                    return receipt
                else:
                    raise Exception(f"Transaction failed: {tx_link}")
                    
            except Exception as e:
                Logger.error(f"Upload attempt {attempt} failed: {str(e)}")
                if attempt < MAX_RETRIES:
                    delay = 10 + random.random() * 20
                    Logger.warn(f"Retrying after {delay:.2f}s...")
                    await asyncio.sleep(delay)
                    attempt += 1
                    continue
                raise
                
    async def process_wallet(self, wallet_index, upload_count, total_uploads):
        """Process a single wallet with multiple uploads"""
        private_key = self.private_keys[wallet_index]
        if not private_key.startswith("0x"):
            private_key = "0x" + private_key
            
        account = Account.from_key(private_key)
        wallet_address = account.address
        
        Logger.section(f"Processing Wallet #{wallet_index + 1} [{wallet_address}]")
        
        successful = 0
        failed = 0
        
        for i in range(1, upload_count + 1):
            upload_number = (wallet_index * upload_count) + i
            Logger.process(f"Upload {upload_number}/{total_uploads} (Wallet #{wallet_index + 1}, File #{i})")
            
            try:
                image_buffer = await self.fetch_random_image()
                image_data = await self.prepare_image_data(image_buffer)
                await self.upload_to_storage(image_data, wallet_address, private_key, wallet_index)
                successful += 1
                Logger.success(f"Upload {upload_number} completed")
                
                if upload_number < total_uploads:
                    Logger.loading("Waiting for next upload...")
                    await asyncio.sleep(3)
            except Exception as e:
                failed += 1
                Logger.error(f"Upload {upload_number} failed: {str(e)}")
                await asyncio.sleep(5)
                
        return successful, failed
                
    async def run(self):
        """Main execution function"""
        try:
            Logger.banner()
            self.load_private_keys()
            self.load_proxies()
            
            # Check network
            Logger.loading("Checking network status...")
            chain_id = await self.web3.eth.chain_id
            if chain_id != CHAIN_ID:
                raise Exception(f"Invalid chainId: expected {CHAIN_ID}, got {chain_id}")
                
            Logger.success(f"Connected to network: chainId {chain_id}")
            
            is_network_synced = await self.check_network_sync()
            if not is_network_synced:
                raise Exception("Network is not synced")
            print(f"{Colors.CYAN}Available wallets:{Colors.RESET}")
            for idx, key in enumerate(self.private_keys):
                account = Account.from_key(key)
                print(f"{Colors.GREEN}[{idx + 1}]{Colors.RESET} {account.address}")
            print()
            upload_count = int(input("How many files to upload per wallet? "))
            if upload_count <= 0:
                Logger.error("Invalid number. Please enter a number greater than 0.")
                return
                
            total_uploads = upload_count * len(self.private_keys)
            Logger.info(f"Starting {total_uploads} uploads ({upload_count} per wallet)")
            total_successful = 0
            total_failed = 0
            
            for wallet_index in range(len(self.private_keys)):
                successful, failed = await self.process_wallet(wallet_index, upload_count, total_uploads)
                total_successful += successful
                total_failed += failed
                
                if wallet_index < len(self.private_keys) - 1:
                    Logger.loading("Switching to next wallet...")
                    await asyncio.sleep(10)
            Logger.section("Upload Summary")
            Logger.summary(f"Total wallets: {len(self.private_keys)}")
            Logger.summary(f"Uploads per wallet: {upload_count}")
            Logger.summary(f"Total attempted: {total_uploads}")
            if total_successful > 0:
                Logger.success(f"Successful: {total_successful}")
            if total_failed > 0:
                Logger.error(f"Failed: {total_failed}")
            Logger.success("All operations completed")
            
        except Exception as e:
            Logger.critical(f"Main process error: {str(e)}")
            return 1
            
        return 0
if __name__ == "__main__":
    bot = OGStorageBot()
    exit_code = asyncio.run(bot.run())
    print(f"{Colors.YELLOW}Process completed ~ Bye bang !{Colors.RESET}")
    exit(exit_code)
