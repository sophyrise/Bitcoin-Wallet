from __future__ import annotations

from fastapi import HTTPException, status

from src.repositories.transaction_repository import TransactionRepository
from src.repositories.wallet_repository import WalletRepository
from src.schemas.transaction import TransactionCreate, TransactionResponse


class TransactionService:
    def __init__(
        self,
        transaction_repository: TransactionRepository,
        wallet_repository: WalletRepository,
    ) -> None:
        self.transaction_repository = transaction_repository
        self.wallet_repository = wallet_repository

    def create_transaction(
        self, transaction_data: TransactionCreate, user_id: int
    ) -> TransactionResponse:
        from_wallet = self.wallet_repository.get_by_address(
            transaction_data.from_address
        )
        if not from_wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Source wallet not found",
            )

        if from_wallet.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't own the source wallet",
            )

        to_wallet = self.wallet_repository.get_by_address(transaction_data.to_address)
        if not to_wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Destination wallet not found",
            )

        amount_satoshi = self.btc_to_satoshi(transaction_data.amount_btc)

        is_same_user = from_wallet.user_id == to_wallet.user_id
        fee = self.calculate_fee(amount_satoshi, is_same_user)

        total_deduction = amount_satoshi + fee

        if from_wallet.balance < total_deduction:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance",
            )

        new_from_balance = from_wallet.balance - total_deduction
        new_to_balance = to_wallet.balance + amount_satoshi

        self.wallet_repository.update_balance(from_wallet.id, new_from_balance)
        self.wallet_repository.update_balance(to_wallet.id, new_to_balance)

        transaction = self.transaction_repository.create(
            transaction_data.from_address,
            transaction_data.to_address,
            amount_satoshi,
            fee,
        )

        return TransactionResponse(
            id=transaction.id,
            from_address=transaction.from_address,
            to_address=transaction.to_address,
            amount_btc=self.satoshi_to_btc(transaction.amount),
            fee_btc=self.satoshi_to_btc(transaction.fee),
            created_at=transaction.created_at,
        )

    def get_transactions_by_user(self, user_id: int) -> list[TransactionResponse]:
        transactions = self.transaction_repository.get_by_user(user_id)
        return [
            TransactionResponse(
                id=t.id,
                from_address=t.from_address,
                to_address=t.to_address,
                amount_btc=self.satoshi_to_btc(t.amount),
                fee_btc=self.satoshi_to_btc(t.fee),
                created_at=t.created_at,
            )
            for t in transactions
        ]

    def get_transactions_by_wallet(
        self, address: str, user_id: int
    ) -> list[TransactionResponse]:
        wallet = self.wallet_repository.get_by_address(address)
        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wallet not found",
            )

        if wallet.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this wallet",
            )

        transactions = self.transaction_repository.get_by_wallet(address)
        return [
            TransactionResponse(
                id=t.id,
                from_address=t.from_address,
                to_address=t.to_address,
                amount_btc=self.satoshi_to_btc(t.amount),
                fee_btc=self.satoshi_to_btc(t.fee),
                created_at=t.created_at,
            )
            for t in transactions
        ]

    def calculate_fee(self, amount: int, is_same_user: bool) -> int:
        if is_same_user:
            return 0
        return int(amount * 0.015)

    def satoshi_to_btc(self, satoshi: int) -> float:
        return satoshi / 100_000_000

    def btc_to_satoshi(self, btc: float) -> int:
        return int(btc * 100_000_000)

