import pytest
from src.modules.update_user.app.update_user_usecase import UpdateUserUsecase
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from unittest.mock import patch, MagicMock
from src.shared.helpers.errors.usecase_errors import CognitoNotAuthorizedError, CognitoInvalidPasswordError


class Test_UpdateUserUsecase:
    def test_update_user_usecase(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        user = usecase(user_id="550e8400-e29b-41d4-a716-446655440002", new_name="Guilherme Alterado")

        assert user.name == "Guilherme Alterado"

    def test_update_user_usecase_not_found(self):
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)

        with pytest.raises(NoItemsFound):
            usecase(user_id="invalid")

    @patch('boto3.client')
    def test_update_user_usecase_with_cognito_success(self, mock_boto):
        mock_client = MagicMock()
        mock_client.exceptions.NotAuthorizedException = type('NotAuthorizedException', (Exception,), {})
        mock_client.exceptions.InvalidPasswordException = type('InvalidPasswordException', (Exception,), {})
        mock_boto.return_value = mock_client
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        
        user = usecase(
            user_id="550e8400-e29b-41d4-a716-446655440002", 
            new_name="Guilherme Cognito", 
            access_token="valid_token", 
            old_password="old", 
            new_password="new"
        )
        
        mock_client.update_user_attributes.assert_called_once_with(
            AccessToken="valid_token",
            UserAttributes=[{'Name': 'name', 'Value': 'Guilherme Cognito'}]
        )
        mock_client.change_password.assert_called_once_with(
            PreviousPassword="old",
            ProposedPassword="new",
            AccessToken="valid_token"
        )
        assert user.name == "Guilherme Cognito"

    @patch('boto3.client')
    def test_update_user_usecase_cognito_not_authorized(self, mock_boto):
        mock_client = MagicMock()
        mock_client.exceptions.NotAuthorizedException = type('NotAuthorizedException', (Exception,), {})
        mock_client.exceptions.InvalidPasswordException = type('InvalidPasswordException', (Exception,), {})
        mock_client.update_user_attributes.side_effect = mock_client.exceptions.NotAuthorizedException()
        mock_boto.return_value = mock_client
        
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        
        with pytest.raises(CognitoNotAuthorizedError):
            usecase(
                user_id="550e8400-e29b-41d4-a716-446655440002", 
                new_name="Guilherme", 
                access_token="invalid_token"
            )

    @patch('boto3.client')
    def test_update_user_usecase_cognito_invalid_password(self, mock_boto):
        mock_client = MagicMock()
        mock_client.exceptions.NotAuthorizedException = type('NotAuthorizedException', (Exception,), {})
        mock_client.exceptions.InvalidPasswordException = type('InvalidPasswordException', (Exception,), {})
        mock_client.change_password.side_effect = mock_client.exceptions.InvalidPasswordException()
        mock_boto.return_value = mock_client
        
        repo = UserRepositoryMock()
        usecase = UpdateUserUsecase(repo=repo)
        
        with pytest.raises(CognitoInvalidPasswordError):
            usecase(
                user_id="550e8400-e29b-41d4-a716-446655440002", 
                access_token="token",
                old_password="old",
                new_password="bad"
            )
