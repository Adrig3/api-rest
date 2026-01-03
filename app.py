from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configuración MySQL + Sakila
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/sakila'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Customer(db.Model):
    __tablename__ = 'customer'

    customer_id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(50))
    address_id = db.Column(db.Integer)
    active = db.Column(db.Boolean)
    create_date = db.Column(db.DateTime)
    last_update = db.Column(db.DateTime)

class Rental(db.Model):
    __tablename__ = 'rental'

    rental_id = db.Column(db.Integer, primary_key=True)
    rental_date = db.Column(db.DateTime)
    inventory_id = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    return_date = db.Column(db.DateTime)
    staff_id = db.Column(db.Integer)
    last_update = db.Column(db.DateTime)




    

# endpoint 1
@app.route('/api/v1/customers', methods=['POST'])
def create_customer():
    data = request.json

    if not data:
        return jsonify({"error": "JSON requerido"}), 400

    customer = Customer(
        store_id=data.get('store_id'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        address_id=data.get('address_id'),
        active=data.get('active', 1),
        create_date=datetime.now()  # <-- obligatorio
    )

    db.session.add(customer)
    db.session.commit()

    return jsonify({
        "message": "Cliente creado correctamente",
        "customer_id": customer.customer_id
    }), 201


# endpoint 2
from flask import request, jsonify

@app.route('/api/v1/customers', methods=['GET'])
def get_customers():
    try:
        # Parámetros de paginación
        limit = request.args.get('limit', default=50, type=int)   # por defecto 50
        offset = request.args.get('offset', default=0, type=int)

        # Parámetros de filtrado opcionales
        first_name_filter = request.args.get('first_name', type=str)
        last_name_filter = request.args.get('last_name', type=str)
        email_filter = request.args.get('email', type=str)

        # Construir query base
        query = Customer.query

        # Aplicar filtros si vienen
        if first_name_filter:
            query = query.filter(Customer.first_name.ilike(f"%{first_name_filter}%"))
        if last_name_filter:
            query = query.filter(Customer.last_name.ilike(f"%{last_name_filter}%"))
        if email_filter:
            query = query.filter(Customer.email.ilike(f"%{email_filter}%"))

        # Aplicar paginación
        customers = query.order_by(Customer.customer_id).offset(offset).limit(limit).all()

        # Convertir resultados a lista de diccionarios
        result = []
        for c in customers:
            result.append({
                "customer_id": c.customer_id,
                "store_id": c.store_id,
                "first_name": c.first_name,
                "last_name": c.last_name,
                "email": c.email,
                "address_id": c.address_id,
                "active": c.active,
                "create_date": c.create_date.strftime('%Y-%m-%d %H:%M:%S') if c.create_date else None,
                "last_update": c.last_update.strftime('%Y-%m-%d %H:%M:%S') if c.last_update else None
            })

        return jsonify({
            "status": "ok",
            "count": len(result),
            "customers": result
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# endpoint 3
@app.route('/api/v1/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    try:
        # Buscar cliente por ID
        customer = Customer.query.get(customer_id)

        if not customer:
            return jsonify({
                "status": "error",
                "message": f"Cliente con ID {customer_id} no encontrado"
            }), 404

        # Convertir a diccionario
        customer_data = {
            "customer_id": customer.customer_id,
            "store_id": customer.store_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "email": customer.email,
            "address_id": customer.address_id,
            "active": customer.active,
            "create_date": customer.create_date.strftime('%Y-%m-%d %H:%M:%S') if customer.create_date else None,
            "last_update": customer.last_update.strftime('%Y-%m-%d %H:%M:%S') if customer.last_update else None
        }

        return jsonify({
            "status": "ok",
            "customer": customer_data
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500
    
# endpoint 4
from datetime import datetime
from flask import request, jsonify

@app.route('/api/v1/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    try:
        # Buscar cliente por ID
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({
                "status": "error",
                "message": f"Cliente con ID {customer_id} no encontrado"
            }), 404

        # Obtener datos JSON enviados en la solicitud
        data = request.json
        if not data:
            return jsonify({"error": "JSON requerido"}), 400

        # Actualizar campos (puedes actualizar todos los que quieras)
        customer.store_id = data.get('store_id', customer.store_id)
        customer.first_name = data.get('first_name', customer.first_name)
        customer.last_name = data.get('last_name', customer.last_name)
        customer.email = data.get('email', customer.email)
        customer.address_id = data.get('address_id', customer.address_id)
        customer.active = data.get('active', customer.active)
        customer.last_update = datetime.now()  # actualizar la fecha de modificación

        # Guardar cambios
        db.session.commit()

        # Devolver respuesta
        return jsonify({
            "status": "ok",
            "message": f"Cliente con ID {customer_id} actualizado correctamente"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# endpoint 5
from flask import jsonify

@app.route('/api/v1/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    try:
        # Buscar el cliente por ID
        customer = Customer.query.get(customer_id)
        if not customer:
            return jsonify({
                "status": "error",
                "message": f"Cliente con ID {customer_id} no encontrado"
            }), 404

        # Eliminar el cliente
        db.session.delete(customer)
        db.session.commit()

        return jsonify({
            "status": "ok",
            "message": f"Cliente con ID {customer_id} eliminado correctamente"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500




if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)