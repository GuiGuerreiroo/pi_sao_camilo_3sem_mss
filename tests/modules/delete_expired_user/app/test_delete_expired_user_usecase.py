import pytest
from unittest.mock import MagicMock
from src.modules.delete_expired_user.app.delete_expired_user_usecase import DeleteExpiredUserUseCase

class Test_DeleteExpiredUserUseCase:
    def test_delete_expired_user_success(self):
        usecase = DeleteExpiredUserUseCase()
        usecase.client = MagicMock()
        usecase.client.admin_delete_user.return_value = {}
        
        emails = ["test1@maua.br", "test2@maua.br"]
        
        deleted = usecase(emails_to_be_deleted=emails)
        
        assert deleted == emails
        assert usecase.client.admin_delete_user.call_count == 2
        usecase.client.admin_delete_user.assert_any_call(
            UserPoolId=usecase.user_pool_id,
            Username="test1@maua.br"
        )
        usecase.client.admin_delete_user.assert_any_call(
            UserPoolId=usecase.user_pool_id,
            Username="test2@maua.br"
        )

    def test_delete_expired_user_not_found(self):
        usecase = DeleteExpiredUserUseCase()
        usecase.client = MagicMock()
        
        ExceptionClass = type('UserNotFoundException', (Exception,), {})
        usecase.client.exceptions.UserNotFoundException = ExceptionClass
        
        usecase.client.admin_delete_user.side_effect = ExceptionClass()
        
        emails = ["nonexistent@maua.br"]
        
        deleted = usecase(emails_to_be_deleted=emails)
        
        # It appends even if not found in cognito, according to usecase logic
        assert deleted == emails

    def test_delete_expired_user_error(self):
        usecase = DeleteExpiredUserUseCase()
        usecase.client = MagicMock()
        
        ExceptionClass = type('UserNotFoundException', (Exception,), {})
        usecase.client.exceptions.UserNotFoundException = ExceptionClass
        
        usecase.client.admin_delete_user.side_effect = Exception("Some other error")
        
        emails = ["error@maua.br"]
        
        with pytest.raises(Exception, match="Some other error"):
            usecase(emails_to_be_deleted=emails)
