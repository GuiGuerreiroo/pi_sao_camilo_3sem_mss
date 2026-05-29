from unittest.mock import MagicMock
from src.modules.resend_code.app.resend_code_controller import ResendCodeController
from src.modules.resend_code.app.resend_code_usecase import ResendCodeUseCase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock
from src.shared.helpers.errors.usecase_errors import UserExpiredError, NoItemsFound

class Test_ResendCodeController:

    def test_resend_code_controller_success(self):
        repo = UserRepositoryMock()
        usecase = MagicMock()
        usecase.return_value = True

        controller = ResendCodeController(usecase=usecase)

        request = HttpRequest(body={
            'email': '21.00458-7@maua.br'
        })

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body['message'] == 'Código reenviado com sucesso!'

    def test_resend_code_controller_missing_email(self):
        repo = UserRepositoryMock()
        usecase = ResendCodeUseCase(repo=repo)
        controller = ResendCodeController(usecase=usecase)

        request = HttpRequest(body={})

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == "Field email is missing"

    def test_resend_code_controller_invalid_email_type(self):
        repo = UserRepositoryMock()
        usecase = ResendCodeUseCase(repo=repo)
        controller = ResendCodeController(usecase=usecase)

        request = HttpRequest(body={
            'email': 123456
        })

        response = controller(request=request)

        assert response.status_code == 400
        assert "Field email isn't in the right type" in response.body

