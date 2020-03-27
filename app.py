from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os



app = Flask(__name__)
# @app.route('/',methods=['GET','POST'])
# def get():
#     return jsonify({'mgs': 'hello'})

basedir = os.path.abspath(os.path.dirname(__file__))

#database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'bd.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONs'] = True # show notify in terminal
#init db
db = SQLAlchemy(app)
#init ma
ma = Marshmallow(app)
#product class
# make model in sql lite
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    def __int__(self, name, description, price, qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

#product schema

class ProductSchema(ma.Schema):
    class meta:#field allowed to show 
        fields = ('id','name','description','price','qty')


#init schema

product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

@app.route('/product',methods=['POST'])
def add_product():
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']


    new_product = Product(name,description,price,qty)

    db.session.add(new_product)
    db.session.commit()
    return product_schema.jsonify(new_product)
#get all product 

@app.route('/product',methods=['GET'])
def get_product():
    all_product = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result.data)

#get single product 

@app.route('/product/<id>',methods=['GET'])
def get_single_product(id):
    product = Product.query.get(id)
    return product_schema.jsonify(product)

#update product 
@app.route('/product/<id>',methods=['PUT'])
def update_product(id):
    product = Product.query.get(id)
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    qty = request.json['qty']


    product.name = name
    product.description = description
    product.price = price
    product.qty = qty

    db.session.commit()
    return product_schema.jsonify(product)


#delete product 
@app.route('/product/<id>',methods=['DELETE'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return product_schema.jsonify(product)

if __name__ == "__main__":
    app.run(debug=True)