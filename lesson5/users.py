from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    get_flashed_messages,
    make_response,
)
import json

app = Flask(__name__)
app.secret_key = "secret_key"


def get_last_id(users: list) -> int:
    if not users:
        return -1
    return (max(users, key=lambda user: user["id"]))["id"]


def find_user(users: list, id: int) -> dict:
    return next(filter(lambda user: user.get("id") == id, users), None)


@app.get("/")
def start():
    with open("user.json", mode="rt") as fread:
        users = json.load(fread)
    resp = redirect(url_for("users_get"), code=302)
    resp.set_cookie('users', json.dumps(users))
    return resp


@app.get("/users/<int:id>")
def user_get(id):
    users = json.loads(request.cookies.get('users'))
    user = find_user(users, id)
    errors = {} if user else {"id": f"User ID {id} does not exist!"}
    return render_template("users/show.html", user=user, errors=errors)


@app.get("/users")
def users_get():
    users = json.loads(request.cookies.get('users'))
    errors = {}
    messages = get_flashed_messages(with_categories=True)
    return render_template("users/index.html", users=users, errors=errors, messages=messages)


@app.post("/users")
def users_post():
    user = request.form.to_dict()
    if len(user["nickname"]) > 5:
        return (
            render_template(
                "users/new.html",
                user=user,
                errors={"nickname": "too much symbols!"},
            ),
            422,
        )
    users = json.loads(request.cookies.get('users'))
    user["id"] = get_last_id(users) + 1
    users.append(user)
    flash("Новый пользователь успешно создан.", category="success")
    resp = redirect(url_for("users_get"), code=302)
    resp.set_cookie('users', json.dumps(users))
    return resp


@app.get("/users/new")
def user_new():
    user = {}
    errors = {}
    return render_template("users/new.html", user=user, errors=errors)


@app.get("/user/<int:id>/edit")
def user_edit(id):
    users = json.loads(request.cookies.get('users'))
    user = find_user(users, id)
    errors = {} if user else {"id": f"User ID {id} does not exist!"}
    return render_template("users/edit.html", user=user, errors=errors)


@app.post("/users/<int:id>/patch")
def user_patch(id):
    user = request.form.to_dict()
    if not user["nickname"]:
        return (
            render_template(
                "users/edit.html", user=user, errors={"nickname": "can not be blank!"}
            ),
            422,
        )
    if not user["email"]:
        return (
            render_template(
                "users/edit.html", user=user, errors={"email": "can not be blank!"}
            ),
            422,
        )
    users = json.loads(request.cookies.get('users'))
    user_prev = find_user(users, id)
    user["id"] = user_prev["id"]
    idx = users.index(user_prev)
    users[idx] = user
    flash("Данные пользователя успешно обновлены.", category="success")
    resp = redirect(url_for("users_get"), code=302)
    resp.set_cookie('users', json.dumps(users))
    return resp


@app.post("/users/<int:id>/delete")
def delete_user(id):
    users = json.loads(request.cookies.get('users'))
    user = find_user(users, id)
    del users[users.index(user)]
    flash("Пользователь был успешно удален.", category="success")
    resp = redirect(url_for("users_get"), code=302)
    resp.set_cookie('users', json.dumps(users))
    return resp
