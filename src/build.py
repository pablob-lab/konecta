# -*- coding: utf-8 -*-
"""Genera index.html y konecta_plan.md desde una sola fuente de datos.
Uso: python src/build.py  (desde la carpeta konecta)
"""
import base64, json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EVENTOS = [
    {"nombre": "Cena Konecta en Lala", "fecha": "2026-10-01", "detalle": "12 personas · [HORA CENA]"},
    {"nombre": "Lanzamiento Konecta", "fecha": "2026-10-14", "detalle": "Perú Business Fest VIP + parrillada · ticket S/350"},
]

# Líneas del Gantt
LINEAS = [
    {"id": "cena", "nombre": "Cena en Lala"},
    {"id": "com", "nombre": "Invitados y afiliados"},
    {"id": "evt", "nombre": "Lanzamiento"},
    {"id": "pit", "nombre": "Mensaje de los 3"},
    {"id": "post", "nombre": "Después del evento"},
]

# semana, línea, tarea, inicio, fin  (hito = mismo día y tipo "hito")
SEMANAS = [
    {"titulo": "Semana 1 · Definir lo básico", "rango": "22 – 27 sep", "tareas": [
        ("t1", "cena", "Reservar Lala para 12 y confirmar hora", "2026-09-22", "2026-09-24"),
        ("t2", "com", "Definir juntos qué perfil buscamos", "2026-09-22", "2026-09-24"),
        ("t3", "evt", "Cerrar el lugar de la parrillada [LUGAR]", "2026-09-22", "2026-09-29"),
        ("t4", "evt", "Cerrar entradas VIP con el Perú Business Fest", "2026-09-22", "2026-09-29"),
        ("t5", "com", "Cada uno arma su lista de candidatos", "2026-09-24", "2026-09-30"),
    ]},
    {"titulo": "Semana 2 · La cena", "rango": "28 sep – 4 oct", "tareas": [
        ("t6", "cena", "Confirmar a los 12 de la cena", "2026-09-23", "2026-09-29"),
        ("t7", "evt", "Definir aforo [AFORO] y link de pago de S/350", "2026-09-28", "2026-10-02"),
        ("h1", "hito", "Cena Konecta en Lala", "2026-10-01", "2026-10-01", "Cena"),
        ("t8", "com", "Al salir de la cena: cerrar la lista del lanzamiento", "2026-10-01", "2026-10-02"),
        ("t9", "com", "Enviar invitaciones 1:1 (cada uno a los suyos)", "2026-10-02", "2026-10-05"),
    ]},
    {"titulo": "Semana 3 · Preparar", "rango": "5 – 11 oct", "tareas": [
        ("h2", "hito", "Meta: 10 afiliados", "2026-10-05", "2026-10-05", "10 afiliados"),
        ("t10", "com", "Confirmaciones y cobro de tickets", "2026-10-05", "2026-10-09"),
        ("t11", "pit", "Escribir el mensaje: plan a dic 2026 + visión 2027", "2026-10-02", "2026-10-09"),
        ("t12", "evt", "Parrilla: quién cocina y compras (el jue 8 es feriado)", "2026-10-01", "2026-10-09"),
    ]},
    {"titulo": "Semana 4 · Lanzamiento", "rango": "12 – 18 oct", "tareas": [
        ("t13", "pit", "Ensayar el mensaje (máx. 10 min)", "2026-10-12", "2026-10-12"),
        ("t14", "evt", "Montaje y compras finales", "2026-10-12", "2026-10-13"),
        ("h3", "hito", "Lanzamiento Konecta", "2026-10-14", "2026-10-14", "Lanzamiento"),
        ("t15", "post", "Agradecer a cada asistente y afiliar a los interesados", "2026-10-15", "2026-10-18"),
        ("t16", "post", "Retro de los 3: qué funcionó", "2026-10-16", "2026-10-16"),
    ]},
]

CAMINO = [
    ("Octubre", "Cena, 10 afiliados y lanzamiento", "~30 – 40 miembros"),
    ("Oct – Nov", "Afiliar los 50 restantes (20 por socio en total)", "~80 miembros"),
    ("Diciembre", "Encuentro de cierre de año [FECHA]", "~100 miembros"),
    ("2027 · T1", "Cenas mensuales, alianzas y membresía a definir", "estimado"),
    ("2027 · T2", "Casos de éxito de los miembros", "estimado"),
    ("2027 · T3–T4", "Preparación y pitch a fondos", "estimado"),
]

OJO = [
    "Lugar, Business Fest y aforo tienen que estar cerrados antes del 29 sep. Si no, las invitaciones no pueden salir.",
    "Entre la cena y el lanzamiento hay solo 13 días, y el jueves 8 oct es feriado.",
    "En la mesa de la cena no se habla de afiliación ni del evento. Eso va 1:1, después.",
]

REUNIONES = [
    ("mié 23 sep", "Arranque: lugar, Business Fest, aforo"),
    ("lun 28 sep", "Listas de candidatos y ticket"),
    ("jue 1 oct", "15 min al salir de la cena: cerrar la lista"),
    ("lun 5 oct", "¿Llegamos a 10 afiliados?"),
    ("vie 9 oct", "Todo listo para el 14"),
    ("vie 16 oct", "Retro"),
]

PENDIENTES = ["[HORA CENA]", "[LUGAR]", "[AFORO]", "[HORA LANZAMIENTO]", "[FECHA] cierre de año", "Invitados especiales (en gestión)"]


def md():
    L = ["# Konecta · Plan hasta el lanzamiento", "", "Pablo, Sebastián y Emilio. Todo se decide entre los 3.", "",
         "## Fechas clave", ""]
    L += [f"- **{e['nombre']}**: {e['fecha']} · {e['detalle']}" for e in EVENTOS]
    L += ["", "## Ojo", ""] + [f"- {o}" for o in OJO] + [""]
    for s in SEMANAS:
        L += [f"## {s['titulo']} ({s['rango']})", ""]
        L += [("- ◆ **" + n + "**" if l == "hito" else f"- [ ] {n}") for _, l, n, a, b, *_ in s["tareas"]]
        L.append("")
    L += ["## Camino a 2027 (estimado)", "", "| Cuándo | Qué | Comunidad |", "|---|---|---|"]
    L += [f"| {a} | {b} | {c} |" for a, b, c in CAMINO]
    L += ["", "## Reuniones de los 3", ""] + [f"- **{a}**: {b}" for a, b in REUNIONES]
    L += ["", "## Falta definir", ""] + [f"- {p}" for p in PENDIENTES] + [""]
    return "\n".join(L)


README = """# Konecta

Plan simple hasta el lanzamiento del 14 oct 2026. Es de Pablo, Sebastián y Emilio.

- **Página:** https://pablob-lab.github.io/konecta/
- `index.html`: la página. Tiene los 2 eventos, un checklist por semana, el Gantt y el camino a 2027.
- `konecta_plan.md`: lo mismo en texto.
- `konecta_invitados.xlsx`: la plantilla de la lista de invitados y afiliados. Tiene listas desplegables y un resumen por socio. Se regenera con `python src/make_excel.py`. **Ojo: el repo es público. No suban aquí la lista llena con teléfonos y correos.**
- `src/build.py`: aquí se editan las tareas. Después corre `python src/build.py` para regenerar todo.

Las marcas (✓) se guardan en el navegador de cada uno.
"""


def build():
    data = {"eventos": EVENTOS, "lineas": LINEAS, "semanas": SEMANAS, "camino": CAMINO,
            "ojo": OJO, "reuniones": REUNIONES, "pendientes": PENDIENTES}
    js = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    tpl = open(os.path.join(ROOT, "src", "template.html"), encoding="utf-8").read()
    logo = "data:image/png;base64," + base64.b64encode(open(os.path.join(ROOT, "logo-konecta.png"), "rb").read()).decode()
    out = {"index.html": tpl.replace("/*__DATA__*/null", js).replace("__LOGO__", logo), "konecta_plan.md": md(), "README.md": README}
    for name, content in out.items():
        with open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(content)
    print("ok")


if __name__ == "__main__":
    build()
