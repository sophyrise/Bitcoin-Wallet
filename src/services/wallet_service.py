
from src.repositories.user_repository import UserRepository
from src.repositories.wallet_repository import WalletRepository
from src.schemas.wallet import WalletResponse


class WalletService:
    def __init__(
        self,
        wallet_repository: WalletRepository,
        user_repository: UserRepository,
    ) -> None:
        self.wallet_repository = wallet_repository
        self.user_repository = user_repository

    def create_wallet(self, user_id: int) -> WalletResponse:
        pass

    def get_wallet(self, address: str, user_id: int) -> WalletResponse:
        pass

    def get_wallets_by_user(self, user_id: int) -> list[WalletResponse]:
        pass

    def satoshi_to_btc(self, satoshi: int) -> float:
        return satoshi / 100000000

    def btc_to_satoshi(self, btc: float) -> int:
        return int(btc * 100000000)

    async def get_btc_to_usd_rate(self) -> float:
        pass

