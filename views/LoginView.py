import hashlib
from flask import request
from flask_restful import Resource
from flask_restful import Resource
from flask_jwt_extended import create_access_token

from models import User, db


class LoginView(Resource):
    def post(self):
        contrasena_encriptada = hashlib.md5(
            request.json["password"].encode("utf-8")
        ).hexdigest()
        usuario = (
            db.session.query(User)
            .filter(
                User.email == request.json["email"],
                User.password == contrasena_encriptada,
            )
            .first()
        )
        db.session.commit()
        if usuario is None:
            return "Email o contraseña incorrecto", 401
        else:
            token_de_acceso = create_access_token(
                identity=usuario.dar_atributos()
            )
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}
