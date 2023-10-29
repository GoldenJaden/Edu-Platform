import os
from flask import Flask, jsonify, request, make_response
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import requests
from flask_restful import Resource, Api
from flask_migrate import Migrate

# configure the application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)

django_prefix = os.environ.get("DJANGO_NGINX_PREFIX")

self_prefix = os.environ.get("MESSENGER_NGINX_PREFIX")


# api to get user data from main app
def get_user_data():
    user_api_url = f"http://{os.environ.get('USER_APP')}:8000/{django_prefix}api/user"
    response = requests.get(user_api_url)
    if response.status_code == 200:
        user_data = response.json()
        return user_data
    return None


# create db models
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender = db.Column(db.Integer, nullable=False)
    chat = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String(1024), nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    send_time = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

    def __str__(self):
        return f"{self.text}"


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(2055), nullable=False)

    def __str__(self):
        return f"{self.name}"


class ChatMembers(db.Model):
    # data
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)
    chat = db.Column(db.Integer, nullable=False)


# api to interact with app
class GetUsers(Resource):
    def get(self):
        return make_response(jsonify(get_user_data()))


class GetUser(Resource):
    def get(self, pk):
        users = get_user_data()
        user = None
        for u in users:
            if u["id"] == pk:
                user = u
                break
        if user is None:
            return {"Error": "User not found"}

        chats = ChatMembers.query.filter_by(user=user["id"])
        chats_id = [chat.id for chat in chats]

        return {"id": user["id"],
                "username": user["username"],
                "chats": chats_id
                }


class GetMessages(Resource):
    def get(self):
        messages_list = [{'id': m.id,
                          'sender': m.sender,
                          'chat': m.chat,
                          'text': m.text,
                          'is_read': m.is_read,
                          'send_time': str(m.send_time)}
                         for m in Message.query.all()]
        return {"Messages": messages_list}, 200


class GetMessage(Resource):
    def get(self, pk):
        message = Message.query.get(pk)
        message_info = {'id': message.id,
                        'sender': message.sender,
                        'chat': message.chat,
                        'text': message.text,
                        'is_read': message.is_read,
                        'send_time': message.send_time
                        }
        return {f"Message with an id of {pk}:": message_info}


class AddMessage(Resource):
    def post(self):
        if request.is_json:
            data = request.json
            if Chat.query.filter_by(id=data['chat']).first() is None:
                return {'Error': 'No chat with this id'}
            if ChatMembers.query.filter_by(user=data['sender'], chat=data['chat']).first() is None:
                return {'Error': 'User not a member of this chat'}

            message = Message(sender=data['sender'],
                              chat=data['chat'],
                              text=data['text'])
            db.session.add(message)
            db.session.commit()
            return make_response(jsonify({
                'id': message.id,
                'sender': message.sender,
                'text': message.text,
                'chat': message.chat,
                'is_read': message.is_read,
                'send_time': message.send_time
            }))

        else:
            return {'Error': 'Request must be JSON'}, 400


class DeleteMessage(Resource):
    def delete(self, pk):
        message = Message.query.get(pk)
        if message is None:
            return {'Error': 'Not found'}, 404
        db.session.delete(message)
        db.session.commit()
        return f'Message {pk} was deleted', 200


class GetChats(Resource):
    def get(self):
        chats_list = [
            {
                'id': chat.id,
                'name': chat.name
            } for chat in Chat.query.all()
        ]
        return {'Chats': chats_list}, 200


class GetChat(Resource):
    def get(self, pk):
        chat = Chat.query.get(pk)
        if chat is None:
            return {'Error': 'Not found'}, 404
        members = ChatMembers.query.filter_by(chat=chat.id)
        members_id = [member.id for member in members]
        chat_info = {
            "id": chat.id,
            "name": chat.name,
            "members": members_id
        }
        return chat_info


class CreateChat(Resource):
    def post(self):
        if request.is_json:
            data = request.json
            chat = Chat(name=data["name"])
            db.session.add(chat)
            db.session.commit()
            return make_response(jsonify({
                'id': chat.id,
                'name': chat.name
            }))
        else:
            return {'Error': 'Request must be JSON'}, 400


class DeleteChat(Resource):
    def delete(self, pk):
        chat = Chat.query.get(pk)
        if chat is None:
            return {'Error': 'Not found'}, 404
        db.session.delete(chat)
        db.session.commit()
        return f'Chat {pk} was deleted', 200


class AddUserToChat(Resource):
    def post(self):
        if request.is_json:
            data = request.json
            chat_member = ChatMembers(user=data['user'], chat=data['chat'])
            db.session.add(chat_member)
            db.session.commit()
            return make_response(jsonify({
                'id': chat_member.id,
                'user': chat_member.user,
                'chat': chat_member.chat
            }))
        else:
            return {'Error': 'Request must be JSON'}, 400


@app.route(f'{self_prefix}')
def index():
    ALLOWED_METHODS = ['GET', 'POST', 'DELETE', 'CREATE', 'PUT']
    routes = []
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            methods = [m for m in rule.methods if m in ALLOWED_METHODS]
            if methods:
                route = {'url': str(rule), 'methods': methods}
                if rule.__dict__.get('_rule_cache', None):
                    route['arguments'] = list(rule.__dict__['_rule_cache'][0])
                routes.append(route)
    return jsonify({'routes': routes})


# add routes
api.add_resource(GetMessages, self_prefix + 'api/messages/')
api.add_resource(AddMessage, self_prefix + 'api/messages/')
api.add_resource(DeleteMessage, self_prefix + 'api/messages/<int:pk>')

api.add_resource(GetChats, self_prefix + 'api/chats/')
api.add_resource(CreateChat, self_prefix + 'api/chats/')
api.add_resource(GetChat, self_prefix + 'api/chats/<int:pk>/')
api.add_resource(DeleteChat, self_prefix + 'api/chats/<int:pk>/')

api.add_resource(AddUserToChat, self_prefix + 'api/chats/users/')

api.add_resource(GetUsers, self_prefix + 'api/users/')
api.add_resource(GetUser, self_prefix + 'api/users/<int:pk>/')

if __name__ == "__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")
