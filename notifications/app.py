import os
from flask import Flask, jsonify, request, make_response
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
import requests
from flask_restful import Resource, Api


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

flask_nginx = os.environ.get("FLASK_NGINX_PREFIX")
django_nginx = os.environ.get("DJANGO_NGINX_PREFIX")


# Get User information via API
def get_user_data():
    user_api_url = f"http://{os.environ.get('USER_APP')}:8000/{os.environ.get('DJANGO_NGINX_PREFIX')}api/user"
    response = requests.get(user_api_url)
    if response.status_code == 200:
        users_data = response.json()
        return users_data
    return None

# Модель Уведомления
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(80), nullable=False)
    body = db.Column(db.String(500), nullable=True)
    is_read = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return self.title
    
# CRUD Notification
    
class GetNotifications(Resource):
    def get(self):
        notifications_list = [{'id': s.id, 'recipient_id': s.recipient_id,
                               'title': s.title, 'body': s.body,
                               'is_read': s.is_read} for s in Notification.query.all()]
        return {"Notifications": notifications_list}, 200
    
class GetNotificationsForID(Resource):
    def get(self, pk):
        if pk not in [s['id'] for s in get_user_data()]:
                return {'Error': f'The user with id {pk} does not exist'}
        notifications_list = [{'id': s.id, 'recipient_id': s.recipient_id,
                               'title': s.title, 'body': s.body,
                               'is_read': s.is_read} for s in Notification.query.filter_by(recipient_id=pk)]
        return {f"Notifications for user with id {pk}:": notifications_list}
    
class GetNotification(Resource):
    def get(self, pk):
        notification = Notification.query.get(pk)
        notification_ser = {'id': notification.id, 'recipient_id': notification.recipient_id,
                            'title': notification.title, 'body': notification.body, 'is_read': notification.is_read}
        return {f"Notification with an id of {pk}:": notification_ser}
    
class AddNotification(Resource):
    def post(self):
        if request.is_json:
            data = request.json
            if data['recipient_id'] not in [s['id'] for s in get_user_data()]:
                return {'Error': f'The user with id {data["recipient_id"]} does not exist'}
            
            notif = Notification(recipient_id=data['recipient_id'], title=data['title'],
                                 body=data['body'], is_read=data['is_read'])
            db.session.add(notif)
            db.session.commit()
            return make_response(jsonify({'id': notif.id, 'recipient_id': notif.recipient_id,
                               'title': notif.title, 'body': notif.body,
                               'is_read': notif.is_read}), 201)
        else:
            return {'Error': 'Request must be JSON'}, 400
        
        
class DeleteNotification(Resource):
    def delete(self, pk):
        notif = Notification.query.get(pk)
        if notif is None:
            return {'Error': 'not found'}, 404
        db.session.delete(notif)
        db.session.commit()
        return f'Notification {pk} is deleted', 200
    
class DeleteNotificationsForID(Resource):
    def delete(self, pk):
        notif = Notification.query.filter_by(recipient_id=pk)
        if notif is None:
            return {'Error': 'this user has no notifications or does not exist'}, 404
        for s in notif:
            db.session.delete(s)
        db.session.commit()
        
@app.route(flask_nginx + '/api/routes/')
def routes():
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
    routes[0]['description'] = "Get all routes"
    routes[1]['description'] = "Get all notifications"
    routes[2]['description'] = "Create a notification"
    routes[3]['description'] = "Delete a notification by id"
    routes[4]['description'] = "Get all notifications for the user by his id"
    routes[5]['description'] = "Delete all notifications for the user by his id"
    return jsonify({'routes': routes})
        
        
api.add_resource(GetNotifications, flask_nginx + '/api/notifications/')
api.add_resource(AddNotification, flask_nginx + '/api/notifications/')
api.add_resource(DeleteNotification, flask_nginx + '/api/notifications/')
api.add_resource(GetNotification, flask_nginx + '/api/notifications/<int:pk>/')
api.add_resource(GetNotificationsForID, flask_nginx + '/api/notifications/user/<int:pk>/')
api.add_resource(DeleteNotificationsForID, flask_nginx + '/api/notifications/user/<int:pk>/')




        
if __name__ == "__main__":
    app.run(port=5000, debug=True, host="0.0.0.0")
