from web3 import Web3

# Настройки
RPC_URL = 'https:RPC'  # Укажите ваш RPC URL
CONTRACT_ADDRESS = '0xcontract'  # Укажите адрес контракта
MINT_GROUPS = list(range(0, 2))  # Группы для минта, укажите диапазон
WALLETS_FILE = 'wallets.txt'  # Файл с кошельками

# ABI контракта (замените на актуальное значение)
contract_abi = [
    {
        "inputs": [
            {"internalType": "uint256", "name": "group", "type": "uint256"},
            {"internalType": "address", "name": "wallet", "type": "address"}
        ],
        "name": "mintQuotas",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# Функция для проверки подключения к RPC
def check_rpc_connection(w3):
    try:
        block_number = w3.eth.block_number
        print(f"\nСоединение с RPC установлено. Текущий блок: {block_number}\n")
        return True
    except Exception as e:
        print(f"Ошибка подключения к RPC: {e}")
        return False

# Загрузка кошельков из файла
def load_wallets(filename, w3):
    with open(filename, 'r') as f:
        wallets = [line.strip() for line in f if line.strip()]
    checksum_wallets = [w3.to_checksum_address(wallet) for wallet in wallets]
    return checksum_wallets

# Функция для проверки mintQuotas
def check_mint_eligibility(w3, contract, group, wallet_address):
    return contract.functions.mintQuotas(group, wallet_address).call()

# Основная функция
def main():
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not check_rpc_connection(w3):
        return

    wallets = load_wallets(WALLETS_FILE, w3)
    contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)

    print("Результаты проверки:\n")
    for wallet in wallets:
        eligible = False
        for group in MINT_GROUPS:
            try:
                quota = check_mint_eligibility(w3, contract, group, wallet)
                if quota > 0:
                    print(f"Кошелек: {wallet} | Статус: Eligible | Группа: {group} | Quota: {quota}")
                    eligible = True
                    break
            except Exception as e:
                print(f"Кошелек: {wallet} | Ошибка: {e}")
        if not eligible:
            print(f"Кошелек: {wallet} | Статус: Not Eligible")

if __name__ == "__main__":
    main()
