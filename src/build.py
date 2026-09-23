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
     "hace": ["Lidera el proyecto y cuida la esencia", "Anfitrión de la cena y del lanzamiento",
              "Invitados especiales, fondos y alianzas estratégicas", "Da el mensaje del lanzamiento"]},
    {"id": "pab", "nombre": "Pablo", "rol": "Socio · CRO", "lema": "Crecimiento y cierre",
     "hace": ["Meta de 60 afiliados y lista de invitados (Excel)", "Acuerdo VIP con el Perú Business Fest",
              "Ticket S/350: link de pago y cobro", "Métricas y seguimiento semanal"]},
    {"id": "emi", "nombre": "Emilio", "rol": "Socio · [COO – POR CONFIRMAR]", "lema": "Operación y experiencia",
     "hace": ["Reserva en Lala y lugar de la parrillada", "Proveedores: parrilla, compras, DJ y audiovisual",
              "Montaje y logística del 14 oct", "Contenido y fotos del evento"]},
]
EQUIPO_NOTA = ("Las decisiones importantes se toman entre los 3. Sebastián lidera y representa a Konecta; "
               "Pablo y Emilio ejecutan el resto.")

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
        ("t1", "cena", "Reservar Lala para 12 y confirmar hora", "2026-09-22", "2026-09-24", "emi", "seb", "Reserva confirmada por escrito con hora [HORA CENA]."),
        ("t2", "base", "Validar misión, visión y valores", "2026-09-23", "2026-09-28", "seb", "los3", "Los 3 aprueban el texto final (hoy es un borrador)."),
        ("t3", "com", "Definir qué perfil de invitado y afiliado buscamos", "2026-09-22", "2026-09-24", "seb", "los3", "Criterios acordados (ver sección Eventos)."),
        ("t4", "evt", "Cerrar el lugar de la parrillada", "2026-09-22", "2026-09-29", "emi", "seb", "Lugar confirmado: [LUGAR]."),
        ("t5", "evt", "Cerrar entradas VIP con el Perú Business Fest", "2026-09-22", "2026-09-29", "pab", "seb", "Acuerdo con cantidad de entradas y cómo se entregan."),
        ("t6", "com", "Cada uno arma su lista de candidatos en el Excel", "2026-09-24", "2026-09-30", "los3", "pab", "Mínimo 20 nombres por socio cargados en el Excel."),
        ("t7", "com", "Invitados especiales: reconfirmar para el 14 oct", "2026-09-22", "2026-10-09", "seb", "", "Cada invitado especial confirmó o declinó."),
    ]},
    {"titulo": "Semana 2 · La cena", "rango": "28 sep – 4 oct", "tareas": [
        ("t8", "cena", "Confirmar a los 12 de la cena", "2026-09-23", "2026-09-29", "seb", "emi", "12 confirmados, con nombre en el Excel."),
        ("t9", "evt", "Definir aforo y link de pago de S/350", "2026-09-28", "2026-10-02", "pab", "emi", "Aforo [AFORO] fijado y link de pago probado."),
        ("h1", "hito", "Cena Konecta en Lala", "2026-10-01", "2026-10-01", "Cena"),
        ("t10", "com", "Al salir de la cena: cerrar la lista del lanzamiento", "2026-10-01", "2026-10-02", "seb", "los3", "Lista final marcada en el Excel."),
        ("t11", "com", "Enviar invitaciones 1:1 (cada uno a los suyos)", "2026-10-02", "2026-10-05", "los3", "pab", "Todos los de la lista en estado Invitado."),
        ("t12", "com", "Tantear 1:1 a los 12 de la cena para afiliarse", "2026-10-02", "2026-10-05", "pab", "seb", "Cada uno de los 12 tuvo su conversación."),
    ]},
    {"titulo": "Semana 3 · Preparar", "rango": "5 – 11 oct", "tareas": [
        ("h2", "hito", "Meta: 10 afiliados", "2026-10-05", "2026-10-05", "10 afiliados"),
        ("t13", "com", "Confirmaciones y cobro de tickets", "2026-10-05", "2026-10-09", "pab", "", "Confirmados con ticket pagado, marcado en el Excel."),
        ("t14", "pit", "Escribir el mensaje: plan a dic 2026 + visión 2027", "2026-10-02", "2026-10-09", "seb", "pab", "Texto de máximo 10 minutos, revisado por los 3."),
        ("t15", "evt", "Parrilla: quién cocina y compras (jue 8 es feriado)", "2026-10-01", "2026-10-09", "emi", "", "Proveedor o cocinero confirmado y compras hechas."),
        ("t16", "evt", "DJ y cobertura audiovisual (si van)", "2026-10-01", "2026-10-07", "emi", "pab", "Confirmado o descartado."),
    ]},
    {"titulo": "Semana 4 · Lanzamiento", "rango": "12 – 18 oct", "tareas": [
        ("t17", "pit", "Ensayar el mensaje", "2026-10-12", "2026-10-12", "seb", "los3", "Ensayado frente a Pablo y Emilio."),
        ("t18", "evt", "Montaje y compras finales", "2026-10-12", "2026-10-13", "emi", "pab", "Todo listo en el lugar el 13 en la noche."),
        ("h3", "hito", "Lanzamiento Konecta", "2026-10-14", "2026-10-14", "Lanzamiento"),
        ("t19", "post", "Agradecer a cada asistente (≤24 h)", "2026-10-15", "2026-10-15", "seb", "los3", "Mensaje personal a cada asistente."),
        ("t20", "post", "Afiliar a los interesados", "2026-10-15", "2026-10-18", "pab", "", "Interesados en estado Afiliado en el Excel."),
        ("t21", "post", "Fotos y contenido del evento", "2026-10-15", "2026-10-18", "emi", "", "Material publicado con consentimiento de los que aparecen."),
        ("t22", "post", "Retro de los 3: qué funcionó y qué cambiar", "2026-10-16", "2026-10-16", "seb", "los3", "Acuerdos anotados para las próximas 6 semanas."),
    ]},
]

EVENTOS = [
    {"nombre": "Cena Konecta en Lala", "fecha": "2026-10-01", "detalle": "12 personas · [HORA CENA]",
     "objetivo": "Que Pablo viva la dinámica, tantear a los 12 para afiliarse y cerrar la lista del lanzamiento.",
     "antes": [("Reserva confirmada (hora y menú)", "emi"), ("Confirmar a los 12", "seb"), ("Acordar qué buscamos, sin tocar la dinámica", "los3")],
     "durante": [("La dinámica de siempre: sin pitch ni temas comerciales en la mesa", "seb"), ("Observar quién encaja, sin anotar nada en la mesa", "los3")],
     "despues": [("Debrief de 15 min al salir", "los3"), ("Cerrar la lista del lanzamiento", "seb"), ("Agradecer a los 12", "seb"), ("Tanteo 1:1 de afiliación", "pab")]},
    {"nombre": "Lanzamiento Konecta", "fecha": "2026-10-14", "detalle": "Perú Business Fest VIP + parrillada · ticket S/350",
     "objetivo": "Presentar Konecta y su plan, y sumar afiliados sin romper la esencia.",
     "antes": [("Entradas VIP con el Business Fest", "pab"), ("Lugar de la parrillada", "emi"), ("Link de pago y cobro", "pab"), ("Mensaje escrito y ensayado", "seb"), ("Parrilla, compras y montaje", "emi")],
     "durante": [("Recibir a cada invitado", "seb"), ("VIP en el Business Fest → traslado a la parrillada", "emi"), ("Mensaje de Sebastián (máx. 10 min)", "seb"), ("Invitación a afiliarse, sin presión", "pab"), ("Fotos solo con consentimiento", "emi")],
     "despues": [("Agradecimiento personal (≤24 h)", "seb"), ("Afiliar a los interesados", "pab"), ("Cierre de cuentas", "pab"), ("Contenido publicado", "emi"), ("Retro de los 3", "los3")]},
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
    "El lugar, el Business Fest y el aforo tienen que estar cerrados antes del 29 sep. Si no, las invitaciones no pueden salir.",
    "Entre la cena y el lanzamiento hay solo 13 días, y el jueves 8 oct es feriado.",
    "En la mesa de la cena no se habla de afiliación ni del evento. Eso va 1:1, después.",
]

REUNIONES = [
    ("mié 23 sep", "Arranque: lugar, Business Fest, aforo, misión y valores", "los3"),
    ("lun 28 sep", "Listas de candidatos, ticket y misión/visión final", "los3"),
    ("jue 1 oct", "15 min al salir de la cena: cerrar la lista", "los3"),
    ("lun 5 oct", "¿Llegamos a 10 afiliados?", "pab"),
    ("vie 9 oct", "Todo listo para el 14", "emi"),
    ("vie 16 oct", "Retro", "seb"),
]

PENDIENTES = ["[HORA CENA]", "[LUGAR]", "[AFORO]", "[HORA LANZAMIENTO]", "[FECHA] cierre de año",
              "[COO – POR CONFIRMAR] rol de Emilio", "Misión, visión y valores (borrador)", "Invitados especiales (en gestión)"]

NOMBRE = {"seb": "Sebastián", "pab": "Pablo", "emi": "Emilio", "los3": "Los 3", "": ""}


def md():
    L = ["# Konecta", "", "## Misión", "", MISION, "", "## Visión", "", VISION, "", "## Valores", ""]
    L += [f"{i}. **{a}.** {b}" for i, (a, b) in enumerate(VALORES, 1)]
    L += ["", "_Borrador: lo validan los 3._", "", "## Equipo", "", EQUIPO_NOTA, ""]
    for e in EQUIPO:
        L += [f"**{e['nombre']} · {e['rol']}**: {e['lema']}", ""] + [f"- {h}" for h in e["hace"]] + [""]
    L += ["## Ojo", ""] + [f"- {o}" for o in OJO] + [""]
    for s in SEMANAS:
        L += [f"## {s['titulo']} ({s['rango']})", "", "| ✓ | Tarea | Responsable | Apoya | Fechas | Hecho cuando |", "|---|---|---|---|---|---|"]
        for t in s["tareas"]:
            if t[1] == "hito":
                L.append(f"| ◆ | **{t[2]}** | | | {t[3]} | |")
            else:
                L.append(f"| ☐ | {t[2]} | {NOMBRE[t[5]]} | {NOMBRE[t[6]]} | {t[3]} → {t[4]} | {t[7]} |")
        L.append("")
    for e in EVENTOS:
        L += [f"## {e['nombre']} ({e['fecha']})", "", e["objetivo"], ""]
        for k, n in (("antes", "Antes"), ("durante", "Durante"), ("despues", "Después")):
            L += [f"**{n}**", ""] + [f"- [ ] {x} ({NOMBRE[o]})" for x, o in e[k]] + [""]
    L += ["## Criterios para invitar", ""] + [f"- **{a}:** {b}" for a, b in CRITERIOS]
    L += ["", "## Camino a 2027 (estimado)", "", "| Cuándo | Qué | Comunidad |", "|---|---|---|"]
    L += [f"| {a} | {b} | {c} |" for a, b, c in CAMINO]
    L += ["", "## Reuniones de los 3", ""] + [f"- **{a}**: {b} (prepara: {NOMBRE[c]})" for a, b, c in REUNIONES]
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
