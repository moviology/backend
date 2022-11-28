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
