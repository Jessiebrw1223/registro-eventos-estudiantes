from flask import Flask, render_template, request, redirect
from extensions import db
from models import Estudiante, Contacto, PreferenciasTemas, ExpositoresRecomendados, DisponibilidadHoraria
from datetime import datetime
import urllib.parse

app = Flask(__name__)

# Configura la URI de conexión a PostgreSQL en Azure
usuario = "admin12"
password = "Gato$Rojo_84!"
host = "admin12.postgres.database.azure.com"
puerto = 5432
basedatos = "RegistroEventosEstudiantes"

# Codifica la contraseña para la URL
password_encoded = urllib.parse.quote_plus(password)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'postgresql+psycopg2://{usuario}:{password_encoded}@{host}:{puerto}/{basedatos}?sslmode=require'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensión SQLAlchemy
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        try:
            estudiante = Estudiante(
                Nombres=request.form.get('nombres'),
                Apellidos=request.form.get('apellidos'),
                Fecha_Nacimiento=datetime.strptime(request.form.get('fecha_nacimiento'), '%Y-%m-%d'),
                Ciclo=request.form.get('ciclo'),
                Sede=request.form.get('sede')
            )
            db.session.add(estudiante)
            db.session.commit()

            telefono = request.form.get('telefono')
            correo = request.form.get('correo')
            if telefono or correo:
                contacto = Contacto(
                    ID_Estudiante=estudiante.ID_Estudiante,
                    Telefono=telefono,
                    Correo_Electronico=correo
                )
                db.session.add(contacto)

            for i in range(1, 4):
                tema = request.form.get(f'tema{i}')
                interes = request.form.get(f'interes{i}')
                if tema and interes:
                    db.session.add(PreferenciasTemas(
                        ID_Estudiante=estudiante.ID_Estudiante,
                        Tema=tema,
                        Nivel_Interes=int(interes)
                    ))

            for i in range(1, 3):
                nombre_exp = request.form.get(f'nombre_expositor{i}')
                comentario = request.form.get(f'comentario{i}')
                if nombre_exp:
                    db.session.add(ExpositoresRecomendados(
                        ID_Estudiante=estudiante.ID_Estudiante,
                        Nombre_Expositor=nombre_exp,
                        Comentario=comentario
                    ))

            dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
            bloques = [
                '08:00 - 10:00', '10:00 - 12:00',
                '14:00 - 16:00', '16:00 - 18:00', '18:00 - 20:00'
            ]
            for dia in dias:
                for bloque in bloques:
                    key = f'{dia}_{bloque}'.replace(':', '').replace(' ', '').replace('-', '_')
                    disponible = request.form.get(key) == 'on'
                    db.session.add(DisponibilidadHoraria(
                        ID_Estudiante=estudiante.ID_Estudiante,
                        Dia=dia,
                        Bloque_Horario=bloque,
                        Disponible=disponible
                    ))

            db.session.commit()
            return redirect('/gracias')

        except Exception as e:
            db.session.rollback()  # Importante para evitar sesión corrupta
            return f"<h2>Error al procesar el formulario:</h2><pre>{e}</pre>", 500

    return render_template('formulario.html')

@app.route('/gracias')
def gracias():
    return render_template('gracias.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Crea las tablas si no existen
    app.run(debug=True)
