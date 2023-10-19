import hashlib

from flask_restful import Resource
from flask import jsonify,request

from models import User, db

class SignUpView(Resource):
    def post(self):

        user = User.query.filter(
            User.email == request.json["email"]
        ).first()
        
        if request.json["password1"] != request.json["password2"]:
            return "Las contraseñas no coinciden", 401
        
        if user is None:
            password_encript = hashlib.md5(
                request.json["password1"].encode("utf-8")
            ).hexdigest()

            new_user = User(
                username = request.json["username"],
                password = password_encript,
                email = request.json["email"],
            )

            db.session.add(new_user)
            db.session.commit()
            return jsonify(
                mensaje="Usuario creado exitosamente",
            )
        else:
            return "El usuario ya existe", 404
