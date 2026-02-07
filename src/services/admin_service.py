from src.repositories.user_repository import UserRepository
from src.repositories.wallet_repository import WalletRepository
from src.schemas.admin import AdminUserWalletsResponse


class AdminService:
    def __init__(
        self,
        user_repository: UserRepository,
        wallet_repository: WalletRepository,
    ) -> None:
        self.user_repository = user_repository
        self.wallet_repository = wallet_repository

    def get_users_wallets(self) -> list[AdminUserWalletsResponse]:
        users = self.user_repository.get_all()
        if not users:
            return []

        addresses_by_user = self.wallet_repository.get_addresses_by_user_ids(
            [user.id for user in users]
        )

        return [
            AdminUserWalletsResponse(
                user_id=user.id,
                api_key=user.api_key,
                wallets=addresses_by_user.get(user.id, []),
            )
            for user in users
        ]
