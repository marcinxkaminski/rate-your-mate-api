from flask_restful import Resource

BADGES = [{}]


class Badges(Resource):
    def get(self) -> str:
        """
        Gets list of users available to rate
        """
        return USERS

    def post(self) -> str:
        return "POST"

    def put(self) -> str:
        return "PUT"

    def delete(self) -> str:
        return "DELETE"
