from extensions import db
from sqlalchemy.dialects.postgresql import ENUM

# Define los enums con los mismos nombres que en la BD PostgreSQL
dias_enum = ENUM('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', name='dia_semana', create_type=False)
bloques_enum = ENUM(
    '08:00 - 10:00',
    '10:00 - 12:00',
    '14:00 - 16:00',
    '16:00 - 18:00',
    '18:00 - 20:00',
    name='bloque_horario',
    create_type=False
)

class Estudiante(db.Model):
    __tablename__ = 'Estudiantes'
    ID_Estudiante = db.Column(db.Integer, primary_key=True)
    Nombres = db.Column(db.String(100), nullable=False)
    Apellidos = db.Column(db.String(100), nullable=False)
    Fecha_Nacimiento = db.Column(db.Date, nullable=False)
    Ciclo = db.Column(db.String(20))
    Sede = db.Column(db.String(100))

class Contacto(db.Model):
    __tablename__ = 'Contacto'
    ID_Contacto = db.Column(db.Integer, primary_key=True)
    ID_Estudiante = db.Column(db.Integer, db.ForeignKey('Estudiantes.ID_Estudiante'))
    Telefono = db.Column(db.String(20))
    Correo_Electronico = db.Column(db.String(100))

class PreferenciasTemas(db.Model):
    __tablename__ = 'PreferenciasTemas'
    ID_Preferencia = db.Column(db.Integer, primary_key=True)
    ID_Estudiante = db.Column(db.Integer, db.ForeignKey('Estudiantes.ID_Estudiante'))
    Tema = db.Column(db.String(100))
    Nivel_Interes = db.Column(db.SmallInteger)

class ExpositoresRecomendados(db.Model):
    __tablename__ = 'ExpositoresRecomendados'
    ID_Expositor = db.Column(db.Integer, primary_key=True)
    ID_Estudiante = db.Column(db.Integer, db.ForeignKey('Estudiantes.ID_Estudiante'))
    Nombre_Expositor = db.Column(db.String(100))
    Comentario = db.Column(db.String(255))

class DisponibilidadHoraria(db.Model):
    __tablename__ = 'DisponibilidadHoraria'
    ID_Disponibilidad = db.Column(db.Integer, primary_key=True)
    ID_Estudiante = db.Column(db.Integer, db.ForeignKey('Estudiantes.ID_Estudiante'))
    Dia = db.Column(dias_enum, nullable=False)
    Bloque_Horario = db.Column(bloques_enum, nullable=False)
    Disponible = db.Column(db.Boolean, default=False)
