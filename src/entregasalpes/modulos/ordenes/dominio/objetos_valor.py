"""Objetos valor del dominio de vuelos

En este archivo usted encontrará los objetos valor del dominio de vuelos

"""

from __future__ import annotations

from dataclasses import dataclass, field
from entregasalpes.seedwork.dominio.objetos_valor import ObjetoValor, Codigo, Ruta, Locacion
from datetime import datetime
from enum import Enum

@dataclass(frozen=True)
class CodigoIATA(Codigo):
    ...

@dataclass(frozen=True)
class CodigoICAO(Codigo):
    ...

@dataclass(frozen=True)
class NombreAero():
    nombre: str

@dataclass(frozen=True)
class Leg(Ruta):
    fecha_salida: datetime
    fecha_llegada: datetime
    origen: Locacion
    destino: Locacion

    def origen(self) -> Locacion:
        return self.origen

    def destino(self) -> Locacion:
        return self.destino

    def fecha_salida(self) -> datetime:
        return self.fecha_salida
    
    def fecha_llegada(self) -> datetime:
        return self.fecha_llegada

@dataclass(frozen=True)
class Segmento(Ruta):
    legs: list[Leg]

    def origen(self) -> Locacion:
        return self.legs[0].origen

    def destino(self) -> Locacion:
        return self.legs[-1].destino

    def fecha_salida(self) -> datetime:
        return self.legs[0].fecha_salida
    
    def fecha_llegada(self) -> datetime:
        return self.legs[-1].fecha_llegada


@dataclass(frozen=True)
class Producto(ObjetoValor):
    odos: list[Odo] = field(default_factory=list)
    #proveedor: 'Proveedor' = field(default_factory='Proveedor')

    @classmethod
    def es_ida_y_vuelta(self) -> bool:
        return self.odos[0].origen() == self.odos[-1].destino()

    @classmethod
    def es_solo_ida(self) -> bool:
        return len(self.odos) == 1

    def tipo_vuelo(self):
        if self.es_ida_y_vuelta():
            return TipoVuelo.IDA_Y_VUELTA
        elif self.es_solo_ida:
            return TipoVuelo.IDA
        else:
            return TipoVuelo.OPEN_JAW

    def ruta(self):
        if self.es_ida_y_vuelta():
            return f"{str(self.odos[0].origen())}-{str(self.odos[-1].origen())}"
        elif self.es_solo_ida:
            return f"{str(self.odos[0].origen())}-{str(self.odos[0].destino())}"
        else:
            return f"{str(self.odos[0].origen())}-{str(self.odos[-1].destino())}"


class Clase(Enum):
    ECONOMICA = "Economica"
    PREMIUM = "Premium"
    EJECUTIVA = "Ejecutiva"
    PRIMERA = "Primera"

class TipoProducto(Enum):
    TECNOLOGIA = "Tecnología"
    COMIDA = "Comida"
    OTRO = "Otro"

@dataclass(frozen=True)
class ParametroBusca(ObjetoValor):
    pasajeros: list[Pasajero] = field(default_factory=list)


class EstadoOrden(str, Enum):
    CREADA = "Creada"
    PREPACIONPRODUCTO = "PreparacionProductos"
    CANCELADA = "Cancelada"
    ENCAMINO = "Encamino"
    ENTREGADA = "Entregada"