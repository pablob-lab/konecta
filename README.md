# Konecta

Plan simple hasta el lanzamiento del 14 oct 2026. Es de Pablo, Sebastián y Emilio.

- **Página:** https://pablob-lab.github.io/konecta/
- `index.html`: la página. Tiene los 2 eventos, un checklist por semana, el Gantt y el camino a 2027.
- `konecta_plan.md`: lo mismo en texto.
- `konecta_invitados.xlsx`: la plantilla de la lista de invitados y afiliados. Tiene listas desplegables y un resumen por socio. Se regenera con `python src/make_excel.py`. **Ojo: el repo es público. No suban aquí la lista llena con teléfonos y correos.**
- `src/build.py`: aquí se editan las tareas. Después corre `python src/build.py` para regenerar todo.

Las marcas (✓) se guardan en el navegador de cada uno.
