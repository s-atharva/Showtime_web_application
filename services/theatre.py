from flask import Blueprint, render_template, request, redirect, session, g, url_for, jsonify
from utils import is_admin_check, is_user_check, get_tags
from db.dao import DAO
from utils import slots
from .user import user_services
theatre_services = Blueprint("theatre_services", __name__)

# -----------------------------ADMIN MOVIES---------------------------------------------------


@theatre_services.route("/admin_movies", methods=["GET"])
def get_movies_as_admin():
    movies = DAO.get_movies()
    return render_template('admin_movies.html', movies=movies)


@theatre_services.route("/admin_add_movie", methods=["POST", "GET"])
def add_movie_as_admin():
    if request.method == "POST":
        tags = request.form.getlist('tag')
        payload = request.form.to_dict()
        payload["tags"] = tags
        payload.pop("tag")
        try:
            DAO.add_movie(payload=payload)
        except Exception as e:
            print(str(e))
        return redirect(url_for("theatre_services.get_movies_as_admin"))
    else:
        return render_template("admin_create_movie.html", tags=get_tags())


@theatre_services.route("/admin_update_movie/<movie_id>", methods=["POST", "GET"])
def update_movie_as_admin(movie_id):
    movie = DAO.get_movie_by_id(movie_id=movie_id)
    if request.method == "POST":
        tags = request.form.getlist('tag')
        payload = request.form.to_dict()
        payload["tags"] = tags
        payload.pop("tag")
        try:
            DAO.update_movie(payload=payload, movie_id=movie_id)
        except Exception as e:
            print(str(e))
        return redirect(url_for("theatre_services.get_movies_as_admin"))
    else:
        return render_template("admin_update_movie.html", movie_id=movie_id, tags=get_tags(), movie=movie)


# -----------------------------ADMIN CITIES---------------------------------------------------


@theatre_services.route("/admin_cities", methods=["GET"])
def get_cities_as_admin():
    cities = DAO.get_cities(is_admin=True)
    return render_template('admin_cities.html', cities=cities)


@theatre_services.route("/admin_add_city", methods=["POST", "GET"])
def add_city_as_admin():
    if request.method == "POST":
        payload = request.form.to_dict()
        payload["is_active"] = int(payload.get("is_active", 1))
        try:
            DAO.add_city(payload=payload)
        except Exception as e:
            print(str(e))
        return redirect(url_for("theatre_services.get_cities_as_admin"))
    else:
        return render_template("admin_create_city.html")


# this is not a standard practice, but works for now
@theatre_services.route("/admin_toggle_city_status/<city_id>", methods=["GET"])
def toggle_city_status_as_admin(city_id):
    try:
        DAO.toggle_city_status(city_id=city_id, params=request.args.to_dict())
    except Exception as e:
        print(str(e))
    return redirect(url_for("theatre_services.get_cities_as_admin"))


# -----------------------------ADMIN VENUES---------------------------------------------------

@theatre_services.route("/admin_search_venues_by_city", methods=["GET"])
def search_venues_by_city_as_admin():
    cities = DAO.get_cities(is_admin=False)
    return render_template('admin_search_venues_by_city.html', cities=cities)


@theatre_services.route("/admin_get_venues_by_city", methods=["GET"])
def get_venues_by_city_as_admin():
    city_id = request.args.get("city_id")
    try:
        venues = DAO.get_venues_by_city(city_id=city_id, is_admin=False)
        cities = DAO.get_cities(is_admin=True)
        return render_template("admin_venues.html", venues=venues, cities=cities, current_city_id=city_id)
    except Exception as e:
        print(str(e))
        return redirect(url_for("theatre_services.search_venues_by_city_as_admin"))


@theatre_services.route("/admin_add_venue/<city_id>", methods=["POST", "GET"])
def add_venue_as_admin(city_id: str):
    print(city_id)
    print(request.method)
    if request.method == "POST":
        payload = request.form.to_dict()
        try:
            DAO.add_venue(city_id=city_id, payload=payload)
        except Exception as e:
            print(str(e))
        return redirect(url_for("theatre_services.get_venues_by_city_as_admin", city_id=city_id))
    else:
        return render_template("admin_create_venue.html", city_id=city_id)


@theatre_services.route("/admin_update_venue/<venue_id>", methods=["POST", "GET"])
def update_venue_as_admin(venue_id):
    if request.method == "POST":
        payload = request.form.to_dict()
        print(payload)
        city_id = None
        try:
            DAO.update_venue(payload=payload, venue_id=venue_id)
            city = DAO.get_city_by_venue(venue_id=venue_id)
            return redirect(url_for("theatre_services.get_venues_by_city_as_admin", city_id=city.get('id')))

        except Exception as e:
            print(str(e))
            return redirect(url_for("theatre_services.get_venues_by_city_as_admin"))
    else:
        venue = DAO.get_venue_by_id(venue_id=venue_id, is_admin=False)
        return render_template("admin_update_venue.html", venue_id=venue_id, venue=venue)


# -----------------------------ADMIN SHOWS---------------------------------------------------

@theatre_services.route("/admin_shows/<venue_id>", methods=["GET"])
def get_shows_by_venue_as_admin(venue_id):
    shows = DAO.get_shows_by_venue(venue_id=venue_id)
    movies_by_shows = {}
    if shows:
        movies_by_shows = {
            show["id"]: DAO.get_movie_by_id(show["movie_id"]) for show in shows
        }
    city = DAO.get_city_by_venue(venue_id=venue_id)
    venue = DAO.get_venue_by_id(venue_id=venue_id)
    return render_template('admin_shows.html', shows=shows, city=city, venue=venue, movies_by_shows=movies_by_shows,
                           slots=slots)


@theatre_services.route("/admin_add_show/<venue_id>", methods=["POST", "GET"])
def add_show_as_admin(venue_id):
    if request.method == "POST":
        payload = request.form.to_dict()
        try:
            DAO.add_show(payload=payload, venue_id=venue_id)
        except Exception as e:
            print(str(e))
        return redirect(url_for("theatre_services.get_shows_by_venue_as_admin", venue_id=venue_id))
    else:
        return render_template("admin_create_show.html", venue_id=venue_id, movies=DAO.get_movies(), slots=slots)


@theatre_services.route("/admin_update_show/<show_id>", methods=["POST", "GET"])
def update_show_as_admin(show_id):
    show = DAO.get_show_by_id(show_id=show_id)
    movie = DAO.get_movie_by_id(movie_id=show.get('movie_id'))
    if request.method == "POST":
        payload = request.form.to_dict()
        try:
            DAO.update_show(payload=payload, show_id=show_id)
        except Exception as e:
            print(str(e))
        return redirect(url_for("theatre_services.get_shows_by_venue_as_admin", venue_id=show.get('venue_id')))
    else:
        return render_template("admin_update_show.html", venue_id=show.get("venue_id"), movies=DAO.get_movies(), slots=slots, show=show, current_movie=movie)


# -----------------------------USER BOOKINGS---------------------------------------------------
@theatre_services.route("/search_movies_by_location_as_user", methods=["GET", "POST"])
def get_show_booking_wizard():

    payload = request.form.to_dict()
    city_id = payload.get("city_id")
    movies = None
    current_city = None
    if city_id:
        current_city = DAO.get_city(city_id=city_id)
        try:
            movies = DAO.get_movies_by_city(city_id=city_id, is_admin=False)
            print(movies)
        except Exception as e:
            print(str(e))

    cities = DAO.get_cities(is_admin=False)

    return render_template("user_search_movies_by_location_form.html", cities=cities, movies=movies, current_city=current_city)


@theatre_services.route("/get_venues_and_shows_by_movie_as_user/city/<city_id>/movie/<movie_id>", methods=["GET"])
def get_venues_and_shows_by_movie_as_user(city_id: str, movie_id: str):
    # get list of venues and their respective shows for a given city_id and movie_id
    # print(city_id, movie_id)
    filtered_venues_pre, filtered_shows = DAO.get_venues_by_city_and_movie(city_id=city_id, movie_id=movie_id)
    # print([venue.get("name") for venue in filtered_venues])
    # print([show.get("slot") for show in filtered_shows])

    filtered_venues = []
    filtered_venue_ids = [show["venue_id"] for show in filtered_shows]
    for venue in filtered_venues_pre:
        if venue["id"] in filtered_venue_ids:
            filtered_venues.append(venue)

    current_city = DAO.get_city(city_id=city_id)
    current_movie = DAO.get_movie_by_id(movie_id=movie_id)
    return render_template("user_get_venues_and_shows_by_movie_city.html", current_movie=current_movie,
                           current_city=current_city, filtered_venues=filtered_venues, filtered_shows=filtered_shows)


@theatre_services.route("/confirm_booking_as_user/movies/<movie_id>/shows/<show_id>", methods=["POST", "GET"])
def confirm_booking_as_user(movie_id, show_id):
    user = DAO.get_user_by_id(g.get("user_id"))
    venue = DAO.get_venue_by_show(show_id=show_id)
    city = DAO.get_city_by_venue(venue_id=venue["id"])
    movie = DAO.get_movie_by_id(movie_id=movie_id)
    show = DAO.get_show_by_id(show_id=show_id)
    if request.method == "GET":
        return render_template(
            "user_confirm_booking_form.html", show=show,
            user_name=user.get("user_name"), user_id=g.get("user_id"), movie=movie,
            venue=venue, city=city
        )
    else:
        payload = request.form.to_dict()
        payload["user_id"] = g.get("user_id")
        payload["tickets_count"] = int(payload["tickets_count"])
        try:
            booking_id = DAO.add_booking(payload=payload)
            DAO.update_show_booking_count(show_id=show_id, payload={"booking_count_inc_by": payload["tickets_count"]})
            return redirect(
                url_for(
                    "theatre_services.acknowledge_booking_confirmed_for_user",
                    booking_id=booking_id, user_id=g.get("user_id")
                )
            )
        except Exception as e:
            print(str(e))
            return render_template(
                "user_confirm_booking_form.html", show=show,
                user_name=user.get("user_name"), movie=movie,
                venue=venue, city=city, error_message="Error in booking a show"
            )


@theatre_services.route("/acknowledge_booking_confirmed_for_user/user/<user_id>/bookings/<booking_id>", methods=["GET"])
def acknowledge_booking_confirmed_for_user(user_id, booking_id):
    booking_details = DAO.get_booking_details(booking_id=booking_id)
    return render_template("user_acknowledge_booking_confirmed.html", **booking_details,
                           user_id=user_id)


@theatre_services.route("/delete_booking/<booking_id>", methods=["GET"])
def delete_booking(booking_id):
    try:
        DAO.delete_booking(booking_id=booking_id)
    except Exception as e:
        print(str(e))
    return redirect(url_for("user_services.get_user_profile"))
