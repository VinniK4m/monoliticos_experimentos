"""Entidades del dominio de vuelos

En este archivo usted encontrará las entidades del dominio de vuelos

"""

from __future__ import annotations
from dataclasses import dataclass, field
import datetime

import entregasalpes.modulos.ordenes.dominio.objetos_valor as ov
from entregasalpes.modulos.ordenes.dominio.eventos import ReservaCreada, ReservaAprobada, ReservaCancelada, ReservaPagada
from entregasalpes.seedwork.ordenes.entidades import Locacion, AgregacionRaiz, Entidad

@dataclass
class Aeropuerto(Locacion):
    codigo: ov.Codigo = field(default_factory=ov.Codigo)
    nombre: ov.NombreAero = field(default_factory=ov.NombreAero)

    def __str__(self) -> str:
        return self.codigo.codigo.upper()

@dataclass
class Proveedor(Entidad):
    codigo: ov.Codigo = field(default_factory=ov.Codigo)
    nombre: ov.NombreAero = field(default_factory=ov.NombreAero)
    itinerarios: list[ov.Itinerario] = field(default_factory=list[ov.Itinerario])

    def obtener_itinerarios(self, odos: list[Odo], parametros: ParametroBusca):
        return self.itinerarios

@dataclass
class Pasajero(Entidad):
    clase: ov.Clase = field(default_factory=ov.Clase)
    tipo: ov.TipoPasajero = field(default_factory=ov.TipoPasajero)

@dataclass
class Orden(AgregacionRaiz):
    id_cliente: uuid.UUID = field(hash=True, default=None)
    estado: ov.EstadoOrden = field(default=ov.EstadoOrden.CREADA)
    productos: list[ov.Itinerario] = field(default_factory=list[ov.Itinerario])

    def crear_reserva(self, reserva: Reserva):
        self.id_cliente = reserva.id_cliente
        self.estado = reserva.estado
        self.itinerarios = reserva.itinerarios
        self.fecha_creacion = datetime.datetime.now()

        self.agregar_evento(ReservaCreada(id_reserva=self.id, id_cliente=self.id_cliente, estado=self.estado.name, fecha_creacion=self.fecha_creacion))
        # TODO Agregar evento de compensación

    def aprobar_reserva(self):
        self.estado = ov.EstadoReserva.APROBADA
        self.fecha_actualizacion = datetime.datetime.now()

        self.agregar_evento(ReservaAprobada(self.id, self.fecha_actualizacion))
        # TODO Agregar evento de compensación

    def cancelar_reserva(self):
        self.estado = ov.EstadoReserva.CANCELADA
        self.fecha_actualizacion = datetime.datetime.now()

        self.agregar_evento(ReservaCancelada(self.id, self.fecha_actualizacion))
        # TODO Agregar evento de compensación
    
    def pagar_reserva(self):
        self.estado = ov.EstadoReserva.PAGADA
        self.fecha_actualizacion = datetime.datetime.now()

        self.agregar_evento(ReservaPagada(self.id, self.fecha_actualizacion))
        # TODO Agregar evento de compensación
