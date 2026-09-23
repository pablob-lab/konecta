# -*- coding: utf-8 -*-
"""Genera index.html y konecta_plan.md desde una sola fuente de datos.
Uso: python src/build.py  (desde la carpeta konecta)
"""
import base64, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHEET_URL = "https://docs.google.com/spreadsheets/d/14X2Y4gjCXVnSD0NDkwmoGj2VSMd-Bp0sp0DLGN6vRGI/edit"

MISION = ("Conectamos a emprendedores con trayectoria con las personas, empresas y fondos que les abren la "
          "siguiente puerta, desde un espacio donde se deja el ego y se habla desde lo humano.")
VISION = ("Ser el ecosistema de emprendedores más valioso del Perú, donde cada conexión genera riqueza para toda "
          "la comunidad: en relaciones y en capital.")
VALORES = [
    ("Humano primero", "En la mesa somos personas, no cargos. Se deja el ego en la puerta."),
    ("Dar antes de pedir", "Cada miembro aporta (contactos, servicios, tiempo) antes de esperar algo."),
    ("Curaduría con apertura", "Elegimos bien a quién invitamos, sin volvernos excluyentes."),
    ("Confianza", "Lo que se habla en la cena se queda en la cena."),
    ("Crecemos juntos", "Si a uno le va bien, gana toda la comunidad."),
]

EQUIPO = [
    {"id": "seb", "nombre": "Sebastián", "rol": "Fundador · CEO", "lema": "La cara y la voz de Konecta",
     "hace": ["Reserva en Lala y confirma a los 12 de la cena", "Guía la dinámica de la cena",
              "Lidera el perfil de invitado, la misión/visión/valores y el mensaje", "Invitados especiales",
              "Cobro por Yape y confirmaciones", "El 14: recibe a los invitados y da el mensaje", "Publica el contenido del evento"]},
    {"id": "pab", "nombre": "Pablo", "rol": "Socio · CRO", "lema": "Crecimiento y cierre",
     "hace": ["Lugar de la parrillada y entradas VIP del Business Fest", "Parrilla y compras (con Emilio)",
              "Lidera los candidatos, el cierre de la lista y la meta de 10 afiliados", "Sheet al día y conteo de cada lunes",
              "Agradece a los asistentes y afilia a los interesados"]},
    {"id": "emi", "nombre": "Emilio", "rol": "Socio · [COO – POR CONFIRMAR]", "lema": "Operación y experiencia",
     "hace": ["Debrief de la cena y agradecimiento a los 12", "Parrilla y compras (con Pablo)", "DJ y audiovisual",
              "Montaje y logística VIP del 14", "Cierre de cuentas y retro"]},
]
EQUIPO_NOTA = ("Cada tarea tiene un solo responsable. Cuando dice «participan los 3», el que lidera se asegura de que se haga. Las decisiones importantes se toman entre los 3.")

LINEAS = [
    {"id": "base", "nombre": "Konecta (identidad)"},
    {"id": "cena", "nombre": "Cena en Lala"},
    {"id": "com", "nombre": "Invitados y afiliados"},
    {"id": "evt", "nombre": "Lanzamiento"},
    {"id": "pit", "nombre": "Mensaje del lanzamiento"},
    {"id": "post", "nombre": "Después del evento"},
]

# id, línea, tarea, inicio, fin, responsable, apoyo, "hecho cuando"
# hito: id, "hito", nombre, fecha, fecha, etiqueta corta
SEMANAS = [
    {"titulo": "Semana 1 · Definir lo básico", "rango": "22 – 27 sep", "tareas": [
        ("t1", "cena", "Reservar Lala para 12 y confirmar hora y menú", "2026-09-22", "2026-09-24", "seb", "", "Reserva confirmada por escrito con hora [HORA CENA]."),
        ("t2", "com", "Definir el perfil de invitado y afiliado", "2026-09-22", "2026-09-24", "seb", "los3", "Criterios acordados (ver sección Eventos)."),
        ("t3", "base", "Validar misión, visión y valores", "2026-09-23", "2026-09-28", "seb", "los3", "Los 3 aprueban el texto final (hoy es un borrador)."),
        ("t4", "evt", "Cerrar el lugar de la parrillada", "2026-09-22", "2026-09-29", "pab", "", "Lugar confirmado: [LUGAR]."),
        ("t5", "evt", "Cerrar las entradas VIP con el Perú Business Fest", "2026-09-22", "2026-09-29", "pab", "", "Acuerdo con cantidad de entradas y cómo se entregan."),
        ("t6", "cena", "Confirmar a los 12 de la cena en Lala", "2026-09-23", "2026-09-29", "seb", "", "12 confirmados, con nombre en el Sheet."),
        ("t7", "com", "Cargar 20 candidatos por socio en el Sheet", "2026-09-24", "2026-09-30", "pab", "los3", "Cada socio tiene 20 nombres en el Sheet."),
        ("t8", "com", "Reconfirmar a los invitados especiales para el 14 oct", "2026-09-22", "2026-10-09", "seb", "", "Cada invitado especial confirmó o declinó."),
    ]},
    {"titulo": "Semana 2 · La cena", "rango": "28 sep – 4 oct", "tareas": [
        ("t9", "evt", "Cobro del ticket de S/350 por Yape de Sebastián", "2026-09-28", "2026-10-02", "seb", "", "Número de Yape compartido con los 3. El aforo se ajusta según la demanda."),
        ("h1", "hito", "Cena Konecta en Lala", "2026-10-01", "2026-10-01", "Cena"),
        ("t10", "cena", "Guiar la dinámica de la cena (sin pitch ni temas comerciales)", "2026-10-01", "2026-10-01", "seb", "", "La cena fluyó como siempre."),
        ("t11", "cena", "Debrief de 15 min al salir de la cena", "2026-10-01", "2026-10-01", "emi", "", "Notas de qué preservar, compartidas con los 3."),
        ("t12", "com", "Cerrar la lista del lanzamiento", "2026-10-01", "2026-10-02", "pab", "los3", "Lista final marcada en el Sheet."),
        ("t13", "cena", "Agradecer a los 12 de la cena", "2026-10-02", "2026-10-02", "emi", "los3", "Cada uno de los 12 recibió un mensaje."),
    ]},
    {"titulo": "Semana 3 · Preparar", "rango": "5 – 11 oct", "tareas": [
        ("h2", "hito", "Meta: 10 afiliados (lidera Pablo)", "2026-10-05", "2026-10-05", "10 afiliados"),
        ("t14", "com", "Confirmaciones y cobro de tickets", "2026-10-05", "2026-10-09", "seb", "", "Confirmados con Yape recibido, marcado en el Sheet."),
        ("t15", "com", "Mantener el Sheet al día y pasar el conteo de afiliados cada lunes", "2026-09-28", "2026-10-18", "pab", "", "Conteo enviado cada lunes al grupo de socios."),
        ("t16", "pit", "Escribir el mensaje: plan a dic 2026 + visión 2027 (máx. 10 min)", "2026-10-02", "2026-10-09", "seb", "los3", "Texto acordado por los 3."),
        ("t17", "evt", "Parrilla: quién cocina, proveedor y compras (jue 8 es feriado)", "2026-10-01", "2026-10-09", "pab+emi", "", "Proveedor o cocinero confirmado y compras hechas."),
        ("t18", "evt", "DJ y cobertura audiovisual: confirmar o descartar", "2026-10-01", "2026-10-07", "emi", "los3", "Confirmado o descartado."),
    ]},
    {"titulo": "Semana 4 · Lanzamiento", "rango": "12 – 18 oct", "tareas": [
        ("t19", "evt", "Montaje y compras finales", "2026-10-12", "2026-10-13", "emi", "los3", "Todo listo en el lugar el 13 en la noche."),
        ("h3", "hito", "Lanzamiento Konecta", "2026-10-14", "2026-10-14", "Lanzamiento"),
        ("t20", "evt", "Recibir a cada invitado", "2026-10-14", "2026-10-14", "seb", "los3", "Cada invitado fue recibido personalmente."),
        ("t21", "pit", "Dar el mensaje del lanzamiento", "2026-10-14", "2026-10-14", "seb", "los3", "Mensaje dado, máximo 10 min."),
        ("t22", "evt", "Logística del VIP en el Business Fest y traslado a la parrillada", "2026-10-14", "2026-10-14", "emi", "los3", "Todos llegaron a la parrillada."),
        ("t23", "evt", "Fotos y video del evento (solo con consentimiento)", "2026-10-14", "2026-10-14", "diego", "", "Cobertura cuadrada con Diego."),
        ("t24", "post", "Agradecer a cada asistente (≤24 h)", "2026-10-15", "2026-10-15", "pab", "los3", "Mensaje personal a cada asistente."),
        ("t25", "post", "Afiliar a los interesados", "2026-10-15", "2026-10-18", "pab", "", "Interesados en estado Afiliado en el Sheet."),
        ("t26", "post", "Cierre de cuentas del evento", "2026-10-16", "2026-10-16", "emi", "", "Ingresos y gastos cuadrados y compartidos."),
        ("t27", "post", "Publicar las fotos y el contenido del evento", "2026-10-15", "2026-10-18", "seb", "", "Material publicado con consentimiento de los que aparecen."),
        ("t28", "post", "Retro de los 3", "2026-10-16", "2026-10-16", "emi", "los3", "Acuerdos anotados para las próximas 6 semanas."),
    ]},
]

EVENTOS = [
    {"nombre": "Cena Konecta en Lala", "fecha": "2026-10-01", "detalle": "12 personas · [HORA CENA]",
     "objetivo": "Que Pablo viva la dinámica y cerrar la lista del lanzamiento. La afiliación se da de forma orgánica.",
     "antes": [("Reservar Lala (hora y menú)", "seb"), ("Confirmar a los 12", "seb"), ("Definir el perfil de invitado", "seb*")],
     "durante": [("La dinámica de siempre: sin pitch ni temas comerciales", "seb")],
     "despues": [("Debrief de 15 min al salir", "emi"), ("Cerrar la lista del lanzamiento", "pab*"), ("Agradecer a los 12", "emi*")]},
    {"nombre": "Lanzamiento Konecta", "fecha": "2026-10-14", "detalle": "Perú Business Fest VIP + parrillada · ticket S/350 por Yape",
     "objetivo": "Presentar Konecta y su plan. La afiliación se da de forma orgánica, sin presión.",
     "antes": [("Entradas VIP con el Business Fest", "pab"), ("Lugar de la parrillada", "pab"), ("Cobro por Yape y confirmaciones", "seb"),
               ("Mensaje del lanzamiento escrito", "seb*"), ("Parrilla y compras", "pab+emi"), ("DJ y audiovisual: sí o no", "emi*"), ("Montaje", "emi*")],
     "durante": [("Recibir a cada invitado", "seb*"), ("VIP en el Business Fest → traslado a la parrillada", "emi*"), ("Mensaje del lanzamiento (máx. 10 min)", "seb*"), ("Fotos y video con consentimiento", "diego")],
     "despues": [("Agradecimiento personal (≤24 h)", "pab*"), ("Afiliar a los interesados", "pab"), ("Cierre de cuentas", "emi"), ("Publicar el contenido", "seb"), ("Retro de los 3", "emi*")]},
]

CRITERIOS = [
    ("Trayectoria", "Tiene historia demostrable. No se exige facturación alta."),
    ("Marca", "Su proyecto tiene una identidad reconocible."),
    ("Innovación", "Aporta algo distinto."),
    ("Potencial", "Hay señales de que va a crecer."),
    ("Sin ego", "Puede hablar desde lo humano. Este criterio no se negocia."),
    ("Suma al mix", "Aporta un rubro, una etapa o un perfil distinto al del grupo."),
]

CAMINO = [
    ("Octubre", "Cena, 10 afiliados y lanzamiento", "~30 – 40 miembros"),
    ("Oct – Nov", "Afiliar los 50 restantes (20 por socio)", "~80 miembros"),
    ("Diciembre", "Encuentro de cierre de año [FECHA]", "~100 miembros"),
    ("2027 · T1", "Cenas mensuales, alianzas y membresía a definir", "estimado"),
    ("2027 · T2", "Casos de éxito de los miembros", "estimado"),
    ("2027 · T3–T4", "Preparación y pitch a fondos", "estimado"),
]

OJO = [
    "El lugar de la parrillada y las entradas VIP del Business Fest tienen que estar cerrados antes del 29 sep.",
    "Entre la cena y el lanzamiento hay solo 13 días, y el jueves 8 oct es feriado.",
    "La afiliación es orgánica: nada de venta en la mesa ni presión en el evento. El aforo se ajusta según la demanda.",
]

REUNIONES = [
    ("mié 23 sep", "Arranque", "seb*"),
    ("lun 28 sep", "Listas, ticket y misión/visión final", "pab*"),
    ("lun 5 oct", "¿Llegamos a 10 afiliados?", "pab*"),
    ("vie 9 oct", "Todo listo para el 14", "emi*"),
    ("vie 16 oct", "Retro", "emi*"),
]

PENDIENTES = ["[HORA CENA]", "[LUGAR]", "[HORA LANZAMIENTO]", "[FECHA] cierre de año",
              "[COO – POR CONFIRMAR] rol de Emilio", "Cobertura de fotos: cuadrar con Diego",
              "Misión, visión y valores (borrador)", "Invitados especiales (en gestión)"]

NOMBRE = {"seb*": "Sebastián", "pab*": "Pablo", "emi*": "Emilio", "seb": "Sebastián", "pab": "Pablo", "emi": "Emilio", "los3": "Los 3", "pab+emi": "Pablo y Emilio", "diego": "Diego (por cuadrar)", "": ""}


def md():
    L = ["# Konecta", "", "## Misión", "", MISION, "", "## Visión", "", VISION, "", "## Valores", ""]
    L += [f"{i}. **{a}.** {b}" for i, (a, b) in enumerate(VALORES, 1)]
    L += ["", "_Borrador: lo validan los 3._", "", "## Equipo", "", EQUIPO_NOTA, ""]
    for e in EQUIPO:
        L += [f"**{e['nombre']} · {e['rol']}**: {e['lema']}", ""] + [f"- {h}" for h in e["hace"]] + [""]
    L += ["## Ojo", ""] + [f"- {o}" for o in OJO] + [""]
    for s in SEMANAS:
        L += [f"## {s['titulo']} ({s['rango']})", "", "| ✓ | Tarea | Responsable | Fechas | Hecho cuando |", "|---|---|---|---|---|"]
        for t in s["tareas"]:
            if t[1] == "hito":
                L.append(f"| ◆ | **{t[2]}** | | {t[3]} | |")
            else:
                L.append(f"| ☐ | {t[2]} | {NOMBRE[t[5]]}{' (lidera, participan los 3)' if t[6] == 'los3' else ''} | {t[3]} → {t[4]} | {t[7]} |")
        L.append("")
    for e in EVENTOS:
        L += [f"## {e['nombre']} ({e['fecha']})", "", e["objetivo"], ""]
        for k, n in (("antes", "Antes"), ("durante", "Durante"), ("despues", "Después")):
            L += [f"**{n}**", ""] + [f"- [ ] {x} ({NOMBRE[o]}{', con los 3' if o.endswith('*') else ''})" for x, o in e[k]] + [""]
    L += ["## Criterios para invitar", ""] + [f"- **{a}:** {b}" for a, b in CRITERIOS]
    L += ["", "## Camino a 2027 (estimado)", "", "| Cuándo | Qué | Comunidad |", "|---|---|---|"]
    L += [f"| {a} | {b} | {c} |" for a, b, c in CAMINO]
    L += ["", "## Reuniones de los 3", ""] + [f"- **{a}**: {b} (lidera: {NOMBRE[c]}, participan los 3)" for a, b, c in REUNIONES]
    L += ["", "## Falta definir", ""] + [f"- {p}" for p in PENDIENTES] + [""]
    return "\n".join(L)


README = """# Konecta

La página de inicio de Konecta. Sebastián (fundador y CEO), Pablo (CRO) y Emilio.

- **Página:** https://pablob-lab.github.io/konecta/
- `index.html`: misión, visión y valores; equipo y roles; plan por semanas con responsable; Gantt; checklist de los 2 eventos; camino a 2027.
- **Lista de invitados:** Google Sheet compartido (solo lo abren Sebastián, Pablo y Emilio). La plantilla se genera con `python src/make_excel.py`. No suban aquí la lista llena: el repo es público.
- `konecta_plan.md`: todo lo anterior en texto.
- `src/build.py`: aquí se editan los textos y las tareas. Después corre `python src/build.py`.

Las marcas (✓) se guardan en el navegador de cada uno.
"""


def build():
    data = {"mision": MISION, "vision": VISION, "valores": VALORES, "equipo": EQUIPO, "equipoNota": EQUIPO_NOTA,
            "lineas": LINEAS, "semanas": SEMANAS, "eventos": EVENTOS, "criterios": CRITERIOS, "camino": CAMINO,
            "ojo": OJO, "reuniones": REUNIONES, "pendientes": PENDIENTES, "nombre": NOMBRE}
    js = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    tpl = open(os.path.join(ROOT, "src", "template.html"), encoding="utf-8").read()
    logo = "data:image/png;base64," + base64.b64encode(open(os.path.join(ROOT, "logo-konecta.png"), "rb").read()).decode()
    out = {"index.html": tpl.replace("/*__DATA__*/null", js).replace("__LOGO__", logo).replace("__SHEET__", SHEET_URL), "konecta_plan.md": md(), "README.md": README}
    for name, content in out.items():
        with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)
    print("ok")


if __name__ == "__main__":
    build()
