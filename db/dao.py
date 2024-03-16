from .db_models import Venue, City, Movie, User, Show, Booking
from .db_engine import DBEngine
from .db_schema import cities_schema, user_schema, venues_schema, movies_schema, movie_schema, city_schema, \
    venues_schema, venue_schema, shows_schema, show_schema, bookings_schema, booking_schema
import uuid
from datetime import datetime
from sqlalchemy.orm import joinedload


class DAO:
    # -------------------------------do not delete this one---------------------------------------------------------
    @classmethod
    def _add_venue(cls, payload: dict):
        cls._attach_id_to_payload(payload)
        city_name = payload.pop("city_name")
        with DBEngine.get_db_session() as session:
            city = session.query(City).filter(City.name == city_name).one()
            new_venue = Venue(**payload, city=city)
            session.add(new_venue)

    @classmethod
    def get_test_data(cls):
        with DBEngine.get_db_session() as session:
            rows = session.query(Venue).all()
        return rows

    @classmethod
    def _attach_id_to_payload(cls, payload: dict):
        payload["id"] = str(uuid.uuid4())

    # --------------------------------- City:---------------------------------------------------
    @classmethod
    def add_city(cls, payload: dict):
        cls._attach_id_to_payload(payload)
        with DBEngine.get_db_session() as session:
            session.add(City(**payload))

    @classmethod
    def get_cities(cls, is_admin=False):
        with DBEngine.get_db_session() as session:
            if is_admin:
                cities = session.query(City).all()
            else:
                cities = session.query(City).filter(City.is_active == 1).all()
            # keeping this one just for reference that how we can access the venues from a city
            # venues = [(city.name, [venue.name for venue in city.venues]) for city in cities]
            cities = cities_schema.dump(cities)
            return cities

    @classmethod
    def get_city_by_venue(cls, venue_id):
        with DBEngine.get_db_session() as session:
            venue = session.query(Venue).filter(Venue.id == venue_id).one()
            city = city_schema.dump(venue.city)
            return city

    @classmethod
    def get_city(cls, city_id, is_admin=False):
        with DBEngine.get_db_session() as session:
            city = session.query(City).filter(City.id == city_id and City.is_active == 1).one()
            city = city_schema.dump(city)
            return city

    @classmethod
    def toggle_city_status(cls, city_id, params):
        print(params)
        with DBEngine.get_db_session() as session:
            session.query(City).filter_by(id=city_id).update(params)

    # --------------------------------- Movie:---------------------------------------------------
    @classmethod
    def add_movie(cls, payload: dict):
        cls._attach_id_to_payload(payload)
        payload["release_date"] = datetime.strptime(payload["release_date"], '%Y-%m-%d').date()
        with DBEngine.get_db_session() as session:
            new_movie = Movie(**payload)
            session.add(new_movie)

    @classmethod
    def update_movie(cls, payload: dict, movie_id: str):
        payload["release_date"] = datetime.strptime(payload["release_date"], '%Y-%m-%d').date()
        with DBEngine.get_db_session() as session:
            session.query(Movie).filter_by(id=movie_id).update(payload)

    @classmethod
    def get_movies(cls, is_admin=False):
        with DBEngine.get_db_session() as session:
            movies = session.query(Movie).all()
            movies = movies_schema.dump(movies)
            return movies

    @classmethod
    def get_movie_by_id(cls, movie_id):
        with DBEngine.get_db_session() as session:
            movie = session.query(Movie).filter(Movie.id == movie_id).one()
            movie = movie_schema.dump(movie)
            return movie

    @classmethod
    def get_movies_by_city(cls, city_id, is_admin=False):
        with DBEngine.get_db_session() as session:
            movies = session.query(Movie).join(Show).join(Venue).join(City) \
                .filter(City.id == city_id).all()
            movies = movies_schema.dump(movies)
            return movies

    # --------------------------------- Venue:---------------------------------------------------

    @classmethod
    def add_venue(cls, city_id: str, payload: dict):
        cls._attach_id_to_payload(payload)
        with DBEngine.get_db_session() as session:
            city = session.query(City).filter(City.id == city_id).one()
            new_venue = Venue(**payload, city=city)
            session.add(new_venue)

    @classmethod
    def get_venues(cls):
        with DBEngine.get_db_session() as session:
            venues = session.query(Venue).all()
            venues = venues_schema.dump(venues)
            return venues

    @classmethod
    def get_venues_by_city(cls, city_id: str, is_admin: bool):
        with DBEngine.get_db_session() as session:
            city = session.query(City).filter(City.id == city_id).one()
            venues = city.venues
            venues = venues_schema.dump(venues)
            # Is this different from the above one?
            # venues = venues_schema.dump([venue for venue in city.venues])
            return venues

    @classmethod
    def update_venue(cls, payload: dict, venue_id: str):
        with DBEngine.get_db_session() as session:
            session.query(Venue).filter_by(id=venue_id).update(payload)

    @classmethod
    def get_venue_by_id(cls, venue_id, is_admin=False):
        with DBEngine.get_db_session() as session:
            venue = session.query(Venue).filter(Venue.id == venue_id).one()
            venue = venue_schema.dump(venue)
            return venue

    @classmethod
    def get_venue_by_show(cls, show_id, is_admin=False):
        with DBEngine.get_db_session() as session:
            show = session.query(Show).filter(Show.id == show_id).one()
            venue = show.venue
            venue = venue_schema.dump(venue)
            return venue

    @classmethod
    def get_venues_by_city_and_movie(cls, city_id, movie_id):
        with DBEngine.get_db_session() as session:
            filtered_venues = session.query(Venue).options(joinedload(Venue.shows)).filter_by(city_id=city_id).all()
            # venues = venues_schema.dump(venues)
            print("----------------------------")
            print("Venues by city and movie")
            for venue in filtered_venues:
                print(venue.name)
            print("---------------------------")
            print("Show by city and movie")
            print(movie_id)
            filtered_shows = []
            for venue in filtered_venues:
                for show in venue.shows:
                    if show.movie_id == movie_id:
                        filtered_shows.append(show)
                        print(show.movie.name, show.movie_id)
                # shows = [show for show in venue.shows if show.movie_id == movie_id]
            # print(shows)
            filtered_venues = venues_schema.dump(filtered_venues)
            filtered_shows = shows_schema.dump(filtered_shows)
            return filtered_venues, filtered_shows

    # ----------------------------User:-------------------------------------------
    @classmethod
    def add_user(cls, payload):
        print(payload)
        cls._attach_id_to_payload(payload)
        with DBEngine.get_db_session() as session:
            new_user = User(**payload)
            session.add(new_user)

    @classmethod
    def get_user(cls, payload):
        print(payload)
        # cls._attach_id_to_payload(payload)
        with DBEngine.get_db_session() as session:
            user = session.query(User).filter(User.user_name == payload.get("user_name")).one()
            user = user_schema.dump(user)
            return user

    @classmethod
    def get_user_by_id(cls, user_id):
        with DBEngine.get_db_session() as session:
            user = session.query(User).filter(User.id == user_id).one()
            user = user_schema.dump(user)
            return user

    @classmethod
    def get_booking_by_user(cls, user_id):
        with DBEngine.get_db_session() as session:
            user = session.query(User).filter(User.id == user_id).one()
            bookings = user.bookings
            bookings = bookings_schema.dump(bookings)
            return bookings
    # ----------------------------Show:---------------------------------------------
    @classmethod
    def get_shows_by_venue(cls, venue_id, is_admin=False):
        try:
            with DBEngine.get_db_session() as session:
                venue = session.query(Venue).filter(Venue.id == venue_id).one()
                shows = shows_schema.dump(venue.shows)
                return shows
        except Exception as e:
            print(str(e))
            return []

    @classmethod
    def add_show(cls, payload, venue_id):
        movie_id = payload.pop("movie_id")
        cls._attach_id_to_payload(payload)
        payload["event_date"] = datetime.strptime(payload["event_date"], '%Y-%m-%d').date()
        with DBEngine.get_db_session() as session:
            movie = session.query(Movie).filter(Movie.id == movie_id).one()
            venue = session.query(Venue).filter(Venue.id == venue_id).one()
            new_show = Show(**payload, movie=movie, venue=venue)
            session.add(new_show)

    @classmethod
    def update_show(cls, payload: dict, show_id: str):
        if "event_date" in payload.keys():
            payload["event_date"] = datetime.strptime(payload["event_date"], '%Y-%m-%d').date()
        with DBEngine.get_db_session() as session:
            session.query(Show).filter_by(id=show_id).update(payload)

    @classmethod
    def update_show_booking_count(cls, show_id, payload):
        booking_count_inc_by = payload["booking_count_inc_by"]
        show = cls.get_show_by_id(show_id=show_id)
        booking_count = show["booking_count"] + booking_count_inc_by
        cls.update_show(payload={"booking_count": booking_count}, show_id=show_id)

    @classmethod
    def get_show_by_id(cls, show_id: str):
        with DBEngine.get_db_session() as session:
            show = session.query(Show).filter(Show.id == show_id).one()
            show = show_schema.dump(show)
            return show

    # ----------------------------Bookings: ----------------------------------------

    @classmethod
    def add_booking(cls, payload):
        with DBEngine.get_db_session() as session:
            cls._attach_id_to_payload(payload=payload)
            show_id = payload.pop("show_id")
            show = session.query(Show).filter(Show.id == show_id).one()
            user_id = payload.pop("user_id")
            user = session.query(User).filter(User.id == user_id).one()
            new_booking = Booking(tickets_count = payload["tickets_count"], id=payload["id"])
            new_booking.user = user
            new_booking.show = show
            session.add(new_booking)

            return payload["id"]

    @classmethod
    def get_booking_details(cls, booking_id):
        with DBEngine.get_db_session() as session:
            booking = session.query(Booking).filter(Booking.id == booking_id).one()
            show = booking.show
            slot = show.slot
            event_date = show.event_date
            total_price = f"{show.price}*{booking.tickets_count}={show.price*booking.tickets_count}"
            movie_name = show.movie.name
            venue_name = show.venue.name
            city_name = show.venue.city.name
            user_name = booking.user.user_name
            booked_at = booking.booked_at
            return {
                "event_date": event_date,
                "slot": slot,
                "total_price": total_price,
                "movie_name": movie_name,
                "venue_name": venue_name,
                "city_name": city_name,
                "user_name": user_name,
                "booking_id": booking_id,
                "booked_at": booked_at
            }

    @classmethod
    def delete_booking(cls, booking_id):
        with DBEngine.get_db_session() as session:
            booking = session.query(Booking).filter(Booking.id == booking_id).one()
            updated_show_bookings = booking.show.booking_count - booking.tickets_count
            print(booking.show_id)
            cls.update_show(payload={"booking_count": updated_show_bookings}, show_id=booking.show_id)
            session.delete(booking)

