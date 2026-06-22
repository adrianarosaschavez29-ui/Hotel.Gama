from flask import Flask, render_template, redirect, send_from_directory, request, Response
from pathlib import Path
from datetime import datetime

app = Flask(
    __name__,
    template_folder="templates",
    static_folder="templates",
    static_url_path=""
)

app.secret_key = "gama123"

BASE = Path(__file__).parent / "templates"

reservas = []
huespedes = []
mensajes = []
resenas = []
solicitudes_servicios = []
facturas = []
usuarios = [
    {
        "correo": "admin@gamahotel.com",
        "rol": "Administrador",
        "estado": "Activo"
    },
    {
        "correo": "recepcion@gamahotel.com",
        "rol": "Recepcionista",
        "estado": "Activo"
    }
]
datos_hotel = {
    "nombre": "Hotel Gama",
    "direccion": "Av. La Paz 1289, Miraflores",
    "telefono": "+51 1 240-5000"
}
precios = {
    "Estándar Simple": 300,
    "Deluxe": 580,
    "Suite": 900,
    "Suite Presidencial": 1200
}

habitaciones = [
    {"numero": 101, "estado": "Libre"},
    {"numero": 102, "estado": "Ocupada"},
    {"numero": 103, "estado": "Ocupada"},
    {"numero": 104, "estado": "Limpieza"},
    {"numero": 105, "estado": "Libre"},
    {"numero": 106, "estado": "Mantenimiento"},
]


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/guardar_reserva", methods=["POST"])
def guardar_reserva():
    nombre = request.form["nombre"]
    dni = request.form["dni"]
    telefono = request.form["telefono"]
    correo = request.form["correo"]
    habitacion = request.form["habitacion"]
    entrada = request.form["entrada"]
    salida = request.form["salida"]

    precio = precios.get(habitacion, 0)

    reservas.append({
        "nombre": nombre,
        "dni": dni,
        "telefono": telefono,
        "correo": correo,
        "habitacion": habitacion,
        "entrada": entrada,
        "salida": salida,
        "precio": precio
    })

    return redirect("/reservas-admin.html")


@app.route("/cliente.html")
def cliente():
    ultima = reservas[-1] if reservas else None
    return render_template("cliente.html", reservas=reservas, ultima=ultima)


@app.route("/admin.html")
def admin():
    total_reservas = len(reservas)
    ingresos = sum(r["precio"] for r in reservas)
    ultima_reserva = reservas[-1] if reservas else None

    dias = [
        "Lunes", "Martes", "Miércoles",
        "Jueves", "Viernes", "Sábado", "Domingo"
    ]

    meses = [
        "enero", "febrero", "marzo", "abril",
        "mayo", "junio", "julio", "agosto",
        "septiembre", "octubre", "noviembre", "diciembre"
    ]

    hoy = datetime.now()
    fecha_actual = f"{dias[hoy.weekday()]}, {hoy.day} de {meses[hoy.month-1]}"

    return render_template(
        "admin.html",
        reservas=reservas,
        total_reservas=total_reservas,
        ingresos=ingresos,
        ultima_reserva=ultima_reserva,
        fecha_actual=fecha_actual
    )

@app.route("/reservas-admin.html")
def reservas_admin():
    return render_template("reservas-admin.html", reservas=reservas)


@app.route("/huespedes-admin.html")
def huespedes_admin():
    return render_template("huespedes-admin.html", huespedes=huespedes)


@app.route("/agregar_huesped", methods=["POST"])
def agregar_huesped():
    nombre = request.form["nombre"]
    dni = request.form["dni"]
    correo = request.form["correo"]
    telefono = request.form["telefono"]

    huespedes.append({
        "nombre": nombre,
        "dni": dni,
        "correo": correo,
        "telefono": telefono
    })

    return redirect("/huespedes-admin.html")


@app.route("/facturacion-admin.html")
def facturacion_admin():
    ingresos = sum(f["importe"] for f in facturas)
    por_cobrar = sum(f["importe"] for f in facturas if f["estado"] == "Pendiente")

    return render_template(
        "facturacion-admin.html",
        facturas=facturas,
        ingresos=ingresos,
        total_facturas=len(facturas),
        por_cobrar=por_cobrar
    )


@app.route("/habitaciones-admin.html")
def habitaciones_admin():
    disponibles = sum(1 for h in habitaciones if h["estado"] == "Libre")
    ocupadas = sum(1 for h in habitaciones if h["estado"] == "Ocupada")
    limpieza = sum(1 for h in habitaciones if h["estado"] == "Limpieza")
    mantenimiento = sum(1 for h in habitaciones if h["estado"] == "Mantenimiento")

    return render_template(
        "habitaciones-admin.html",
        habitaciones=habitaciones,
        disponibles=disponibles,
        ocupadas=ocupadas,
        limpieza=limpieza,
        mantenimiento=mantenimiento
    )


@app.route("/cambiar_estado_habitacion", methods=["POST"])
def cambiar_estado_habitacion():
    numero = int(request.form["numero"])
    nuevo_estado = request.form["estado"]

    for h in habitaciones:
        if h["numero"] == numero:
            h["estado"] = nuevo_estado
            break

    return redirect("/habitaciones-admin.html")


@app.route("/eliminar_habitacion/<int:numero>")
def eliminar_habitacion(numero):
    global habitaciones
    habitaciones = [h for h in habitaciones if h["numero"] != numero]
    return redirect("/habitaciones-admin.html")


@app.route("/agregar_habitacion", methods=["POST"])
def agregar_habitacion():
    numero = int(request.form["numero"])
    estado = request.form["estado"]

    habitaciones.append({
        "numero": numero,
        "estado": estado
    })

    return redirect("/habitaciones-admin.html")



@app.route("/reportes-admin.html")
def reportes_admin():
    ingresos = sum(r["precio"] for r in reservas)
    total_reservas = len(reservas)
    total_huespedes = len(huespedes)
    total_mensajes = len(mensajes)

    return render_template(
        "reportes-admin.html",
        ingresos=ingresos,
        total_reservas=total_reservas,
        total_huespedes=total_huespedes,
        total_mensajes=total_mensajes
    )


@app.route("/exportar_reservas")
def exportar_reservas():
    contenido = "Nombre,DNI,Telefono,Correo,Habitacion,Entrada,Salida,Precio\n"

    for r in reservas:
        contenido += f"{r['nombre']},{r['dni']},{r['telefono']},{r['correo']},{r['habitacion']},{r['entrada']},{r['salida']},{r['precio']}\n"

    return Response(
        contenido,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=reservas_hotel_gama.csv"}
    )


@app.route("/servicios-admin.html")
def servicios_admin():
    return render_template(
        "servicios-admin.html",
        solicitudes_servicios=solicitudes_servicios
    )


@app.route("/solicitar_servicio", methods=["POST"])
def solicitar_servicio():
    habitacion = request.form["habitacion"]
    servicio = request.form["servicio"]
    hora = request.form["hora"]

    solicitudes_servicios.append({
        "habitacion": habitacion,
        "servicio": servicio,
        "hora": hora,
        "estado": "Preparando"
    })

    return redirect("/servicios-admin.html")


@app.route("/enviar_mensaje", methods=["POST"])
def enviar_mensaje():
    nombre = request.form["nombre"]
    habitacion = request.form["habitacion"]
    texto = request.form["mensaje"]

    mensajes.append({
    "id": len(mensajes),
    "nombre": nombre,
    "habitacion": habitacion,
    "mensaje": texto,
    "hora": "Ahora",
    "respuesta": ""
}    )

    return redirect("/cliente.html")


@app.route("/mensajes-admin.html")
def mensajes_admin():
    return render_template("mensajes-admin.html", mensajes=mensajes)

@app.route("/mensaje/<int:id>")
def ver_mensaje(id):
    mensaje = mensajes[id]
    return render_template("ver-mensaje.html", mensaje=mensaje)


@app.route("/responder_mensaje/<int:id>", methods=["POST"])
def responder_mensaje(id):
    respuesta = request.form["respuesta"]
    mensajes[id]["respuesta"] = respuesta
    return redirect("/mensajes-admin.html")


@app.route("/chat-admin.html")
def chat_admin():
    return render_template("chat-admin.html", mensajes=mensajes)


@app.route("/responder_chat", methods=["POST"])
def responder_chat():
    respuesta = request.form["respuesta"]

    if mensajes:
        mensajes[-1]["respuesta"] = respuesta

    return redirect("/chat-admin.html")

@app.route("/configuracion-admin.html")
def configuracion_admin():
    return render_template(
        "configuracion-admin.html",
        usuarios=usuarios,
        datos_hotel=datos_hotel
    )
@app.route("/guardar_datos_hotel", methods=["POST"])
def guardar_datos_hotel():
    datos_hotel["nombre"] = request.form["nombre"]
    datos_hotel["direccion"] = request.form["direccion"]
    datos_hotel["telefono"] = request.form["telefono"]

    return redirect("/configuracion-admin.html")

@app.route("/agregar_usuario", methods=["POST"])
def agregar_usuario():

    correo = request.form["correo"]
    rol = request.form["rol"]

    usuarios.append({
        "correo": correo,
        "rol": rol,
        "estado": "Activo"
    })

    return redirect("/configuracion-admin.html")
@app.route("/eliminar_usuario/<int:id>")
def eliminar_usuario(id):

    if 0 <= id < len(usuarios):
        usuarios.pop(id)

    return redirect("/configuracion-admin.html")

@app.route("/resena.html")
def resena():
    return render_template(
        "resena.html",
        resenas=resenas
    )
@app.route("/agregar_resena", methods=["POST"])
def agregar_resena():

    nombre = request.form["nombre"]
    puntuacion = request.form["puntuacion"]
    comentario = request.form["comentario"]
    
    resenas.append({
    "nombre": nombre,
    "puntuacion": puntuacion,
    "comentario": comentario,
    "fecha": datetime.now().strftime("%d/%m/%Y")
    })

    return redirect("/resena.html")


@app.route("/<path:pagina>")
def paginas(pagina):
    if pagina.endswith(".html") and (BASE / pagina).exists():
        return render_template(pagina)

    if (BASE / pagina).exists():
        return send_from_directory(BASE, pagina)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)