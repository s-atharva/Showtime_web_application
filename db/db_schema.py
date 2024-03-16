from marshmallow import Schema, fields, EXCLUDE, pre_dump
import json


class Venue(Schema):
    id = fields.String()
    name = fields.String()
    address = fields.String()
    capacity = fields.Integer()
    city_id = fields.String()


class City(Schema):
    id = fields.String()
    name = fields.String()
    is_active = fields.Integer()


class Show(Schema):
    id = fields.String()
    slot = fields.String()
    event_date = fields.Date()
    price = fields.Integer()
    last_updated = fields.DateTime()
    booking_count = fields.Integer()
    movie_id = fields.String()
    venue_id = fields.String()


class Movie(Schema):
    id = fields.String()
    name = fields.String()
    tags = fields.List(fields.String())
    last_updated = fields.DateTime()
    release_date = fields.Date()

    @pre_dump
    def treat_json(self, data, **kwargs):
        if isinstance(data.tags, str):
            data.tags = json.loads(data.tags)

        return data


class Booking(Schema):
    id = fields.String()
    ticket_count = fields.Integer()
    show_id = fields.String()
    user_id = fields.String()
    booked_at = fields.DateTime()


class User(Schema):
    id = fields.String()
    name = fields.String()
    is_admin = fields.Boolean()
    user_name = fields.String()
    password = fields.String()


# -------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------

venue_schema = Venue(unknown=EXCLUDE)
venues_schema = Venue(unknown=EXCLUDE, many=True)

city_schema = City(unknown=EXCLUDE)
cities_schema = City(unknown=EXCLUDE, many=True)

show_schema = Show(unknown=EXCLUDE)
shows_schema = Show(unknown=EXCLUDE, many=True)

movie_schema = Movie(unknown=EXCLUDE)
movies_schema = Movie(unknown=EXCLUDE, many=True)

booking_schema = Booking(unknown=EXCLUDE)
bookings_schema = Booking(unknown=EXCLUDE, many=True)

user_schema = User(unknown=EXCLUDE)
users_schema = User(unknown=EXCLUDE, many=True)
