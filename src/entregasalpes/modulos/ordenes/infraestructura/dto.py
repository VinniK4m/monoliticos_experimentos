"""DTOs para la capa de infrastructura del dominio de vuelos

En este archivo usted encontrará los DTOs (modelos anémicos) de
la infraestructura del dominio de vuelos

"""

from entregasalpes.config.db import db
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

import uuid

Base = db.declarative_base()

# Tabla intermedia para tener la relación de muchos a muchos entre la tabla reservas e itinerarios
ordenes_productos = db.Table(
    "ordenes_productos",
    db.Model.metadata,
    db.Column("orden_id", db.String(40), db.ForeignKey("ordenes.id")),
    db.Column("odo_orden", db.Integer),
    db.Column("segmento_orden", db.Integer),
    db.Column("leg_orden", db.Integer),
    db.Column("fecha_salida", db.DateTime),
    db.Column("fecha_llegada", db.DateTime),
    db.Column("origen_codigo", db.String(10)),
    db.Column("destino_codigo", db.String(10)),
    db.ForeignKeyConstraint(
        ["odo_orden", "segmento_orden", "leg_orden", "fecha_salida", "fecha_llegada", "origen_codigo", "destino_codigo"],
        ["itinerarios.odo_orden", "itinerarios.segmento_orden", "itinerarios.leg_orden", "itinerarios.fecha_salida", "itinerarios.fecha_llegada", "itinerarios.origen_codigo", "itinerarios.destino_codigo"]
    )
)

class Producto(db.Model):
    __tablename__ = "productos"
    codigo = db.Column(db.Integer, primary_key=True, nullable=False)
    serial = db.Column(db.String(10), primary_key=True, nullable=False)
    descripcion = db.Column(db.String(100), primary_key=True, nullable=False)
    precio = db.Column(db.Integer, nullable=False, primary_key=True)
    fecha_vencimiento = db.Column(db.DateTime, nullable=False, primary_key=True)
    tipo_producto = db.Column(db.String(100), nullable=False)


class Orden(db.Model):
    __tablename__ = "ordenes"
    id = db.Column(db.String(40), primary_key=True)
    fecha_creacion = db.Column(db.DateTime, nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)
    productos = db.relationship('Producto', secondary=ordenes_productos, backref='ordenes')

class EventosOrden(db.Model):
    __tablename__ = "eventos_reserva"
    id = db.Column(db.String(40), primary_key=True)
    id_entidad = db.Column(db.String(40), nullable=False)
    fecha_evento = db.Column(db.DateTime, nullable=False)
    version = db.Column(db.String(10), nullable=False)
    tipo_evento = db.Column(db.String(100), nullable=False)
    formato_contenido = db.Column(db.String(10), nullable=False)
    nombre_servicio = db.Column(db.String(40), nullable=False)
    contenido = db.Column(db.Text, nullable=False)

class ReservaAnalitica(db.Model):
    __tablename__ = "analitica_ordenes"
    fecha_creacion = db.Column(db.Date, primary_key=True)
    total = db.Column(db.Integer, primary_key=True, nullable=False)