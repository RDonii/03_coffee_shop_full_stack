import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc, or_
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

db_drop_and_create_all()


# ROUTES
@app.route('/')
def home_page():
    return 'not implemented'

@app.route('/drinks', methods = ['GET'])
def get_drinks_for_all():
    drinks_query = Drink.query.all()
    drinks = [drink.short() for drink in drinks_query]

    return jsonify({
        "success": True,
        "drinks": drinks
    })

@app.route('/drinks-detail', methods = ['GET'])
@requires_auth('get:drinks-detail')
def drinks_detail(payload):
    try:
        drinks_query = Drink.query.all()
        drinks = [drink.long() for drink in drinks_query]
        return jsonify({
            'success': True,
            'drinks': drinks
        })
    except:
        abort(500)



@app.route('/drinks', methods = ['POST'])
@requires_auth(permission='post:drinks')
def post_drinks(payload):
    data = request.get_json()
    new_title = data.get('title', None)
    new_recipe = data.get('recipe', None)

    if new_title==None or new_recipe==None:
        abort(400)

    else:
        try:
            new_recipe = "["+json.dumps(new_recipe)+"]"
            new_drink = Drink(title=new_title, recipe=new_recipe)
            new_drink.insert()

            
            new_drink_long = new_drink.long()

            return jsonify({
                'success': True,
                'drinks': new_drink_long
            })
        except:
            abort(422)

@app.route('/drinks/<int:id>', methods = ['PATCH'])
@requires_auth(permission='patch:drinks')
def update_drinks(payload, id):
    drink = Drink.query.filter(Drink.id==id).one_or_none()
    if drink==None:
        abort(404)
    
    data = request.get_json()
    update_title = data.get('title', None)
    update_recipe = data.get('recipe', None)

    try:
        if update_title==None and update_recipe==None:
            abort(400)
        if update_title!=None:
            drink.title = update_title
        if update_recipe!=None:
            drink.recipe=update_recipe
        drink.update()
    except:
        abort(422)
    
    drinks = drink.long()

    return jsonify({
        'success': True,
        'drinks': [drinks]
    })

@app.route('/drinks/<int:id>', methods = ['DELETE'])
@requires_auth(permission='delete:drinks')
def delete_drinks(payload, id):
    drink = Drink.query.filter(Drink.id==id).one_or_none()
    if drink==None:
        abort(404)
    try:
        drink_query = Drink.query.filter(Drink.id==id)
        drink_query.delete()
    except:
        abort(500)

    return jsonify({
        'success': True,
        'delete': id
    })

# Error Handling


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(400)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

@app.errorhandler(500)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response