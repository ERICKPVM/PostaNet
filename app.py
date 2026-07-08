import os
from flask import Flask

from routes.admin.dashboard import dashboard_admin
from routes.admin.auth import auth
from routes.admin.usuarios import usuarios
from routes.admin.zonas import zonas

from routes.recepcion.familias import familias
from routes.recepcion.pacientes import pacientes
from routes.recepcion.dashboard import dashboard_recepcion
from routes.recepcion.documentos import documentos

from routes.medico.dashboard import dashboard_medico
from routes.medico.pacientes import pacientes_medico
from routes.medico.consultas import consultas

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(
    "static",
    "uploads",
    "documentos"
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.secret_key = "postanet_secret"

app.register_blueprint(auth)
app.register_blueprint(dashboard_admin)
app.register_blueprint(usuarios)
app.register_blueprint(zonas)

app.register_blueprint(familias)
app.register_blueprint(pacientes)
app.register_blueprint(dashboard_recepcion)
app.register_blueprint(documentos)

app.register_blueprint(dashboard_medico)
app.register_blueprint(pacientes_medico)
app.register_blueprint(consultas)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)