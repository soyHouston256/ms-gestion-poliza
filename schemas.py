from pydantic import BaseModel
class policy_types(BaseModel):
    id: int
    codigo: str
    nombre: str
    descripcion: str
    categoria: str
    modalidad: str

class policies(BaseModel):
    codigo_poliza: int
    numero_poliza: str
    codigo_persona: int
    producto: policy_types

class ProductoOut(BaseModel):
    id: int
    codigo: str
    nombre: str
    descripcion: str
    categoria: str
    modalidad: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True