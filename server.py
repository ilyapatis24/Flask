import pydantic
from flask import Flask, jsonify, request
from flask.views import MethodView
from models import Session, Advert

app = Flask('app')


class HttpError(Exception):
    def __init__(self, status_code: int, description: str | dict | list):
        self.status_code = status_code
        self.description = description


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"status": "error", "description": error.description})
    response.status_code = error.status_code
    return response


class CreateAdvert(pydantic.BaseModel):
    title: str
    description: str
    owner: str

    @pydantic.validator("title")
    def is_ascii_title(cls, value: str):
        if not value.isascii():
            raise ValueError('incorrect title')
        return value

    @pydantic.validator("description")
    def is_ascii_description(cls, value: str):
        if not value.isascii():
            raise ValueError('incorrect description')
        return value

    @pydantic.validator("owner")
    def is_ascii_owner(cls, value: str):
        if not value.isascii():
            raise ValueError('incorrect owner name')
        return value
    
def get_advert(advert_id: int, session: Session):
    advert = session.get(Advert, advert_id)
    if advert is None:
        raise HttpError(404, 'advert not found')
    return advert

def validate(unvalidated_data: dict, validation_model):
    try:
        return validation_model(**unvalidated_data).dict()
    except pydantic.ValidationError as er:
        raise HttpError(400, er.errors())


class AdvertView(MethodView):
    def get(self, advert_id: int):
        with Session() as session:
            advert = get_advert(advert_id, session)
            return jsonify({"id": advert_id, "title": advert.title, "description": advert.description,
                            "creation_date": advert.creation_date.strftime("%m.%d.%y"), "owner": advert.owner})

    def post(self):
        json_data = request.json
        json_data = validate(json_data, CreateAdvert)
        with Session() as session:
            advert = Advert(**json_data)
            session.add(advert)
            session.commit()
            return jsonify({"id": advert.id})
        
    def delete(self, advert_id: int):
        with Session() as session:
            advert = get_advert(advert_id, session)
            session.delete(advert)
            session.commit()
            return jsonify({"status": "deleted"})
        
def index():
    return "Hello world!"


app.add_url_rule("/adverts/<int:advert_id>/", view_func=AdvertView.as_view("advert"), methods=["GET", "DELETE"])
app.add_url_rule("/adverts/", view_func=AdvertView.as_view("advert_create"), methods=["POST"])
app.add_url_rule("/", view_func=index, methods=["GET"])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')