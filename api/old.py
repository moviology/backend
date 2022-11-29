# @app.route("/register", methods=['GET', 'POST'])
# def register():
#     if request.method == "POST":
#         user_name = request.form.get("name")
#         user_email = request.form.get("email")
#         user_pw = request.form.get("password")
#
#         if users_data.find_one({"email": user_email}) is not None:
#             return render_template("registerFail.html")
#         else:
#             encrypted_password = sha256_crypt.hash(user_pw)
#             new_user = {
#                 "name": user_name,
#                 "email": user_email,
#                 "password": encrypted_password
#             }
#             users_data.insert_one(new_user)
#
#             fetched_user = users_data.find_one({"email": user_email})
#             session["name"] = fetched_user["_id"]
#
#             return render_template("index.html")
#     return render_template("register.html")


# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         user_email = request.form.get("email")
#         user_pw = request.form.get("password")
#         fetched_user = users_data.find_one({"email": user_email})
#
#         if fetched_user is None or not sha256_crypt.verify(user_pw, fetched_user['password']):
#             print("Incorrect login details")
#             return render_template("loginFail.html")
#         else:
#             print("Logged in successfully")
#             session["name"] = fetched_user["_id"]
#
#         return render_template("index.html")
#     return render_template("login.html")
#
# @app.route("/authenticate", methods=["GET", "POST"])
# def authenticate():
#     if session.get("name"):
#         return render_template("index.html")
#     return render_template("authentication.html")




# #
# from flask import Flask
# from flask import jsonify
# from flask import request
#
# from flask_jwt_extended import create_access_token
# from flask_jwt_extended import get_jwt_identity
# from flask_jwt_extended import jwt_required
# from flask_jwt_extended import JWTManager
#
# app = Flask(__name__)
#
# # Setup the Flask-JWT-Extended extension
# app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
# jwt = JWTManager(app)
#
#
# # Create a route to authenticate your users and return JWTs. The
# # create_access_token() function is used to actually generate the JWT.
# @app.route("/login", methods=["POST"])
# @jwt_required(optional=True)
# def login():
#     username = request.form.get("email", None)
#     password = request.form.get("password", None)
#     if username != "test" or password != "test":
#         return jsonify({"msg": "Bad username or password"}), 401
#
#     access_token = create_access_token(identity=username)
#     print(get_jwt_identity())
#     return jsonify(access_token=access_token)
#
#
# # Protect a route with jwt_required, which will kick out requests
# # without a valid JWT present.
# @app.route("/protected")
# @jwt_required()
# def protected():
#     # Access the identity of the current user with get_jwt_identity
#     current_user = get_jwt_identity()
#     print(current_user)
#     return jsonify(logged_in_as=current_user), 200
#
#
# if __name__ == "__main__":
#     app.run()