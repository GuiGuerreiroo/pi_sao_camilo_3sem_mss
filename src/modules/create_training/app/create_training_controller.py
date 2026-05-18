from datetime import datetime
from src.shared.domain.enums.symptoms import SYMPTOMS
from src.shared.domain.enums.usrine_color import URINE_COLOR
from src.shared.domain.enums.modality import MODALITY
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.dto.user_apigateway_dto import UserApiGatewayDTO
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter, InvalidRange
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, BedrockIntegrationError, ForbiddenAction
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import Created,NotFound, BadRequest, InternalServerError, Forbidden, ServiceUnavailable
from .create_training_usecase import CreateTrainingUseCase



class CreateTrainingController:
    
    def __init__(self, usecase: CreateTrainingUseCase):
        self.CreateTrainingUseCase = usecase

    def __call__(self, request: IRequest) -> IResponse: 
        try:
            if request.data.get('requester_user') is None:
                raise MissingParameters('requester_user')

            requester_user = UserApiGatewayDTO.from_api_gateway(request.data.get('requester_user'))

            if not isinstance(requester_user.user_id, str):
                raise WrongTypeParameter('user_id', 'str', type(requester_user.user_id))

            if requester_user.role != ROLE.USER.value:
                raise ForbiddenAction("user")

            # timestamp em milissegundos do momento atual
            current_timestamp = int(datetime.now().timestamp()) * 1000

            modality= request.data.get('modality')

            if modality is None:
                raise MissingParameters('modality')

            try:
                modality_enum = MODALITY(modality)

            except ValueError:
                raise WrongTypeParameter('modality', f"one of {[m.value for m in MODALITY]}", modality)

            start_date= request.data.get('start_date')

            if start_date is None:
                raise MissingParameters('start_date')

            if not isinstance(start_date, int):
                raise WrongTypeParameter('start_date', 'int', type(start_date))
            
            # todo timestamp miliseconds tme 13 digitos
            if len(str(start_date)) != 13:
                raise InvalidRange('start_date', 'start_date must be in millisecond')

            end_date= request.data.get('end_date')

            if end_date is None:
                raise MissingParameters('end_date')

            if not isinstance(end_date, int):
                raise WrongTypeParameter('end_date', 'int', type(end_date))

            # todo timestamp miliseconds tme 13 digitos
            if len(str(end_date)) != 13:
                raise InvalidRange('end_date', 'end_date must be in millisecond')

            # expected to be in minutes
            duration= request.data.get('duration')

            if duration is None:
                raise MissingParameters('duration')

            if not isinstance(duration, float):
                raise WrongTypeParameter('duration', 'float', type(duration))

            # validando que duration está em minutos
            if duration < 1:
                raise InvalidRange('duration', 'duration should be greater than 0 minutes')

            # validando a data de inicio é menor que a de fim
            if start_date >= end_date:
                raise InvalidRange('start_date', 'start_date should be less than end_date')

            if start_date > current_timestamp or end_date > current_timestamp:
                raise InvalidRange('start_date', 'start_date and end_date should be less than current timestamp')

            # validando a duração é maior que 0
            if duration <= 0.0:
                raise InvalidRange('duration', 'duration should be greater than 0')

            
            environment_temperature= request.data.get('environment_temperature')

            if environment_temperature is None:
                raise MissingParameters('environment_temperature')

            if not isinstance(environment_temperature, float):
                raise WrongTypeParameter('environment_temperature', 'float', type(environment_temperature))

            if environment_temperature < -40.0:
                raise InvalidRange('environment_temperature', 'environment_temperature should be greater than or equal to -40')

            if environment_temperature > 50.0:
                raise InvalidRange('environment_temperature', 'environment_temperature should be less than or equal to 50')


            environment_humidity= request.data.get('environment_humidity')

            if environment_humidity is None:
                raise MissingParameters('environment_humidity')

            if not isinstance(environment_humidity, float):
                raise WrongTypeParameter('environment_humidity', 'float', type(environment_humidity))

            urine_color= request.data.get('urine_color')

            if urine_color is None:
                raise MissingParameters('urine_color')

            try:
                urine_color_enum = URINE_COLOR(urine_color)

            except ValueError:
                raise WrongTypeParameter('urine_color', f"one of {[u.value for u in URINE_COLOR]}", urine_color)

            pre_training_symptoms = request.data.get('pre_training_symptoms')

            if pre_training_symptoms:
                if not isinstance(pre_training_symptoms, list):
                    raise WrongTypeParameter('pre_training_symptoms', 'list', type(pre_training_symptoms))

                for symptom in pre_training_symptoms:
                    try:
                        SYMPTOMS(symptom)
                    except ValueError:
                        raise WrongTypeParameter('pre_training_symptoms', f"one of {[s.value for s in SYMPTOMS]}", symptom)
     
            # pesoem Kg
            pre_training_weight = request.data.get('pre_training_weight')

            if pre_training_weight is None:
                raise MissingParameters('pre_training_weight')

            if not isinstance(pre_training_weight, float):
                raise WrongTypeParameter('pre_training_weight', 'float', type(pre_training_weight))

            # peso antes do treino precisa ser maior que 35kg
            if pre_training_weight <= 35.0:
                raise InvalidRange('pre_training_weight', 'pre_training_weight should be greater than 35kg')

            # peso antes do treino não pode ser maior que 200kg
            if pre_training_weight > 200.0:
                raise InvalidRange('pre_training_weight', 'pre_training_weight should be less than or equal to 200kg')
            
            pre_training_hydration = request.data.get('pre_training_hydration')

            if pre_training_hydration is None:
                raise MissingParameters('pre_training_hydration')

            if not isinstance(pre_training_hydration, float):
                raise WrongTypeParameter('pre_training_hydration', 'float', type(pre_training_hydration))

            # hidratacao antes do treino precisa ser maior que 0
            if pre_training_hydration < 0.0:
                raise InvalidRange('pre_training_hydration', 'pre_training_hydration should be greater than or equal to 0')

            # hidratacao antes do treino não pode ser maior que 5000ml = 5 liters
            if pre_training_hydration > 5000.0:
                raise InvalidRange('pre_training_hydration', 'pre_training_hydration should be less than or equal to 5000')

            during_training_hydration = request.data.get('during_training_hydration')

            if during_training_hydration :

                if not isinstance(during_training_hydration, float):
                    raise WrongTypeParameter('during_training_hydration', 'float', type(during_training_hydration))

                # hidratacao durante o treino precisa ser maior que 0
                if during_training_hydration <= 0.0:
                    raise InvalidRange('during_training_hydration', 'during_training_hydration should be greater than or equal to 0')

                # hidratacao durante o treino não pode ser maior que 5000ml = 5 liters
                if during_training_hydration > 5000.0:
                    raise InvalidRange('during_training_hydration', 'during_training_hydration should be less than or equal to 5000')

            else:
                during_training_hydration = 0.0

            during_training_urine_elimination = request.data.get('during_training_urine_elimination')

            if during_training_urine_elimination:
                if not isinstance(during_training_urine_elimination, float):
                    raise WrongTypeParameter('during_training_urine_elimination', 'float', type(during_training_urine_elimination))

                if during_training_urine_elimination <= 0.0:
                    raise InvalidRange('during_training_urine_elimination', 'during_training_urine_elimination should be greater than or equal to 0ml')

                if during_training_urine_elimination > 4000.0:
                    raise InvalidRange('during_training_urine_elimination', 'during_training_urine_elimination should be less than or equal to 4000ml')

            else:
                during_training_urine_elimination = 0.0


            post_training_symptoms= request.data.get('post_training_symptoms')

            if post_training_symptoms:
                if not isinstance(post_training_symptoms, list):
                    raise WrongTypeParameter('post_training_symptoms', 'list', type(post_training_symptoms))

                for symptom in post_training_symptoms:
                    try:
                        SYMPTOMS(symptom)
                    except ValueError:
                        raise WrongTypeParameter('post_training_symptoms', f"one of {[s.value for s in SYMPTOMS]}", symptom)
            
            # peso em Kg
            post_training_weight= request.data.get('post_training_weight')

            if post_training_weight is None:
                raise MissingParameters('post_training_weight')

            if not isinstance(post_training_weight, float):
                raise WrongTypeParameter('post_training_weight', 'float', type(post_training_weight))

            # peso depois do treino precisa ser maior que 35kg
            if post_training_weight <= 35.0:
                raise InvalidRange('post_training_weight', 'post_training_weight should be greater than or equal to 35kg')

            # peso depois do treino não pode ser maior que 200kg
            if post_training_weight > 200.0:
                raise InvalidRange('post_training_weight', 'post_training_weight should be less than or equal to 200kg')

            soaked_clothes = request.data.get('soaked_clothes')

            if soaked_clothes:
                if not isinstance(soaked_clothes, bool):
                    raise WrongTypeParameter('soaked_clothes', 'bool', type(soaked_clothes))


            training_intensity= request.data.get('training_intensity')

            if training_intensity is None:
                raise MissingParameters('training_intensity')

            if not isinstance(training_intensity, float):
                raise WrongTypeParameter('training_intensity', 'float', type(training_intensity))

            # intensidade do treino precisa ser de 1 a 10
            if training_intensity < 1 or training_intensity > 10:
                raise InvalidRange('training_intensity', 'training_intensity should be between 1 and 10')

            training = self.CreateTrainingUseCase(
                user_id=requester_user.user_id,
                modality=modality_enum,
                start_date=start_date,
                end_date=end_date,
                duration=duration,
                environment_temperature=environment_temperature,
                environment_humidity=environment_humidity,
                urine_color=urine_color_enum,
                pre_training_symptoms=pre_training_symptoms,
                pre_training_weight=pre_training_weight,
                pre_training_hydration=pre_training_hydration,
                during_training_hydration=during_training_hydration,
                during_training_urine_elimination=during_training_urine_elimination,
                post_training_symptoms=post_training_symptoms,
                post_training_weight=post_training_weight,
                soaked_clothes=soaked_clothes,
                training_intensity=training_intensity
            )

            viewmodel = {
                'training': training.model_dump(mode='json', exclude_none=True),
                'message': 'Training successfully created and reviewed by AI'
            }

            response = Created(viewmodel)

            return response

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except BedrockIntegrationError as err:
            return ServiceUnavailable(body=err.message)

        except ForbiddenAction as err:
            return Forbidden(body=err.message)

        except InvalidRange as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return InternalServerError(body=str(err))