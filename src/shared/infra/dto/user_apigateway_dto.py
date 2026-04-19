class UserApiGatewayDTO:
    name: str
    email: str
    user_id: str

    def __init__(self, name: str, email: str, user_id: str):
        self.name = name
        self.email = email
        self.user_id = user_id

    @staticmethod
    def from_api_gateway(user_data: dict) -> 'UserApiGatewayDTO':
        """
        This method is used to convert the user data from the API Gateway to a UserApiGatewayDTO object.
        """
        return UserApiGatewayDTO(
            name=user_data['name'],
            email=user_data['email'],
            user_id=user_data['sub']
        )

    def __eq__(self, other):
        return self.name == other.name and self.email == other.email and self.user_id == other.user_id