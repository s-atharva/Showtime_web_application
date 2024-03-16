from flask import Blueprint, render_template, request, redirect, session, g, url_for, jsonify
from db.dao import DAO
from utils import is_admin_check, is_user_check

user_services = Blueprint("user_services", __name__)


@user_services.route("/", methods=["GET"])
def login():
    return redirect_if_already_logged_in(redirect_admin_function="user_services.get_admin_dashboard",
                                         redirect_user_function="user_services.get_user_home",
                                         render_template_file="generic_login.html")


@user_services.route("/user_login", methods=["GET", "POST"])
def user_login():
    if request.method == "POST":
        payload = request.form.to_dict()
        payload["is_admin"] = False
        return login_helper(payload=payload)
    else:
        return redirect_if_already_logged_in(render_template_file="user_login.html")


@user_services.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        payload = request.form.to_dict()
        payload["is_admin"] = True
        return login_helper(payload=payload)
    else:
        return redirect_if_already_logged_in(render_template_file="admin_login.html")


def redirect_if_already_logged_in(redirect_admin_function="user_services.get_admin_dashboard",
                                  redirect_user_function="user_services.get_user_home",
                                  render_template_file="generic_login.html"):
    if g.user_name and g.is_admin:
        return redirect(url_for(redirect_admin_function))
    elif g.user_name:
        return redirect(url_for(redirect_user_function))
    else:
        return render_template(render_template_file)


def login_helper(payload: dict):
    try:
        user = DAO.get_user(payload)
        if user and user.get("user_name") == payload.get("user_name") and user.get("password") == payload.get(
                "password"):
            session["user_name"] = payload.get("user_name")
            g.user_name = payload.get("user_name")

            session["is_admin"] = payload.get("is_admin")
            g.is_admin = payload.get("is_admin")

            session["user_id"] = user.get("id")
            g.user_id = user.get("id")
            print(f"User id: {g.user_id}")

            if payload.get("is_admin"):
                return redirect(url_for("user_services.get_admin_dashboard"))
            else:
                return redirect(url_for("user_services.get_user_home"))
        else:
            return redirect(url_for("user_services.login"))
    except Exception as e:
        print(str(e))
        return redirect(url_for("user_services.login"))


@user_services.route("/user", methods=["POST"])
def add_user():
    payload = request.form.to_dict()
    if payload["is_admin"] == "False":
        payload["is_admin"] = False
    else:
        payload["is_admin"] = True
    DAO.add_user(payload=payload)
    return jsonify(True)


@user_services.route("/user_home", methods=["GET"])
def get_user_home():
    if g.user_name and not g.is_admin:
        return render_template("user_home.html")
    elif g.user_name and g.is_admin:
        return redirect(url_for("user_services.user_login"))
    else:
        return redirect(url_for("user_services.get_admin_dashboard"))


@user_services.route("/admin_dashboard", methods=["GET", "POST"])
def get_admin_dashboard():
    if is_admin_check():
        return render_template("admin_dashboard.html")
    elif is_user_check():
        return redirect(url_for("user_services.get_user_home"))
    else:
        return redirect(url_for("user_services.login"))


@user_services.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    g.pop("user_id", None)

    session.pop("user_name", None)
    g.pop("user_name", None)

    session.pop("is_admin", None)
    g.pop("is_admin", None)
    return redirect(url_for("user_services.login"))


@user_services.route("/user_profile", methods=["POST", "GET"])
def get_user_profile():
    user_id = g.user_id
    bookings_details = []
    # 1. get list of bookings for this user
    try:
        bookings = DAO.get_booking_by_user(user_id=user_id)
        for booking in bookings:
            bookings_details.append(DAO.get_booking_details(booking_id=booking["id"]))
    except Exception as e:
        print(str(e))
    # 2. get booking details for each booking_id
    return render_template("user_profile.html", bookings_details=bookings_details)
