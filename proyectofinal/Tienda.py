from flask import Flask ,jsonify ,request, render_template

# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://MViktoriaU:Delfines/2@MViktoriaU.mysql.pythonanywhere-services.com/MViktoriaU$Tienda'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none

db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow


#**********************************************************************
# Modelos

class Amigurumi(db.Model):
    __tablename__ = 'amigurumi'
    idamigurumi = db.Column(db.Integer, primary_key=True)
    idproducto = db.Column(db.Integer, nullable=False)
    codigo = db.Column(db.String(10), nullable=False)
    nombre = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.String(500))
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.String(20))
    imagen = db.Column(db.String(255))

    def __init__(self, idproducto, codigo, nombre, descripcion, precio, stock, imagen):
        self.idproducto = idproducto
        self.codigo = codigo
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock
        self.imagen = imagen


class Cliente(db.Model):
    __tablename__ = 'cliente'
    idcliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(20), nullable=False)
    apellido = db.Column(db.String(20), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    cel = db.Column(db.String(15), nullable=False)
    direccion = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(30), nullable=False)

    def __init__(self, nombre, apellido, edad, cel, direccion, email):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.cel = cel
        self.direccion = direccion
        self.email = email


class Factura(db.Model):
    __tablename__ = 'factura'
    idfactura = db.Column(db.Integer, primary_key=True)
    idcliente = db.Column(db.Integer, nullable=False)
    fecha_emision = db.Column(db.Date)

    def __init__(self, idcliente, fecha_emision):
        self.idcliente = idcliente
        self.fecha_emision = fecha_emision


class Pedido(db.Model):
    __tablename__ = 'pedido'
    idpedido = db.Column(db.Integer, primary_key=True)
    idcliente = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.Date)
    idproducto = db.Column(db.Integer)
    cantidad_solicitada = db.Column(db.Integer)
    precio = db.Column(db.Float)
    fecha_pedido = db.Column(db.Date)
    estado_pedido = db.Column(db.String(20))

    def __init__(self, idcliente, fecha, idproducto, cantidad_solicitada, precio, fecha_pedido, estado_pedido):
        self.idcliente = idcliente
        self.fecha = fecha
        self.idproducto = idproducto
        self.cantidad_solicitada = cantidad_solicitada
        self.precio = precio
        self.fecha_pedido = fecha_pedido
        self.estado_pedido = estado_pedido

with app.app_context():
    db.create_all()

#  ************************************************************

class AmigurumiSchema(ma.Schema):
    class Meta:
        model = Amigurumi
        fields=('id','nombre','precio','stock','imagen')

class ClienteSchema(ma.Schema):
    class Meta:
        model = Cliente


class FacturaSchema(ma.Schema):
    class Meta:
        model = Factura


class PedidoSchema(ma.Schema):
    class Meta:
        model = Pedido



# Inicializar esquemas
amigurumi_schema = AmigurumiSchema()
amigurumis_schema = AmigurumiSchema(many=True)
pedido_schema = PedidoSchema()
pedidos_schema = PedidoSchema(many=True)


# Rutas

# Rutas para "amigurumi"

@app.route("/amigurumi/", methods=["POST"])
def create_amigurumi():
    idproducto = request.json["idproducto"]
    codigo = request.json["codigo"]
    nombre = request.json["nombre"]
    descripcion = request.json["descripcion"]
    precio = request.json["precio"]
    stock = request.json["stock"]
    imagen = request.json["imagen"]
    new_amigurumi = Amigurumi(idproducto, codigo, nombre, descripcion, precio, stock, imagen)
    db.session.add(new_amigurumi)
    db.session.commit()
    return amigurumi_schema.jsonify(new_amigurumi)


# crea los endpoint o rutas (json)
@app.route('/amigurumi',methods=['GET'])
def get_Amigurumi():
    all_amigurumi=Amigurumi.query.all()         # el metodo query.all() lo hereda de db.Model
    result=amigurumi_schema.dump(all_amigurumi)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)

# retorna un JSON de todos los registros de la tabla

@app.route('/amigurumi/<id>',methods=['GET'])
def get_amigurumi(id):
        amigurumi=Amigurumi.query.get(id)
        return amigurumi_schema.jsonify(amigurumi)

@app.route("/amigurumi/<id>", methods=["PUT"])
def update_amigurumi(id):
    amigurumi = Amigurumi.query.get(id)
    if amigurumi:
        amigurumi.idproducto = request.json["idproducto"]
        amigurumi.codigo = request.json["codigo"]
        amigurumi.nombre = request.json["nombre"]
        amigurumi.descripcion = request.json["descripcion"]
        amigurumi.precio = request.json["precio"]
        amigurumi.stock = request.json["stock"]
        amigurumi.imagen = request.json["imagen"]
        db.session.commit()
        return jsonify({"message": "Amigurumi actualizado correctamente"})
    else:
        return jsonify({"message": "Amigurumi no encontrado"}), 404
    return amigurumi_schema.jsonify(amigurumi)

@app.route("/amigurumi/<id>", methods=["DELETE"])
def delete_amigurumi(id):
    amigurumi = Amigurumi.query.get(id)
    if amigurumi:
        db.session.delete(amigurumi)
        db.session.commit()
        return jsonify({"message": "Amigurumi eliminado correctamente"})
    else:
        return jsonify({"message": "Amigurumi no encontrado"}), 404
    return amigurumi_schema.jsonify(amigurumi)



# Rutas para "pedido"

@app.route("/pedido", methods=["POST"])
def create_pedido():
    idcliente = request.json["idcliente"]
    fecha = request.json["fecha"]
    idproducto = request.json["idproducto"]
    cantidad_solicitada = request.json["cantidad_solicitada"]
    precio = request.json["precio"]
    fecha_pedido = request.json["fecha_pedido"]
    estado_pedido = request.json["estado_pedido"]
    new_pedido = Pedido(idcliente, fecha, idproducto, cantidad_solicitada, precio, fecha_pedido, estado_pedido)
    db.session.add(new_pedido)
    db.session.commit()
    return pedido_schema.jsonify(new_pedido)

@app.route("/pedido", methods=["GET"])
def get_pedidos():
    all_pedidos = Pedido.query.all()
    result = pedidos_schema.dump(all_pedidos)
    return jsonify(result)

@app.route("/pedido/<id>", methods=["DELETE"])
def delete_pedido(id):
    pedido = Pedido.query.get(id)
    if pedido:
        db.session.delete(pedido)
        db.session.commit()
        return jsonify({"message": "Pedido eliminado correctamente"})
    else:
        return jsonify({"message": "Pedido no encontrado"}), 404


#programa principal *******************************

if __name__ == '__main__':
    app.run(port=5008)
    # ejecuta el servidor Flask en el puerto 5000

@app.route('/')
def hello():
    return 'Hello YOU'
'''
@app.route('/')
def index():
    return render_template('Ingresar.html')'''
