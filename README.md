# Estrés canino en guarderías: diagnóstico de calidad de datos

**Actividad:** GA1-220501094-01-AA1-EV05 – Diagnosticar la calidad de datos: preparación, exploración y documentación
**Aprendiz:** Laura Vanessa Henao · **Ficha:** 3169901

## Descripción
Proyecto de ciencia de datos sobre el bienestar de los perros durante su estadía en guarderías. Este repositorio contiene el diagnóstico inicial de calidad de los datasets del proyecto, hecho con Python y Pandas.

## Propósito
Evaluar si los datos tienen condiciones adecuadas para analizar la pregunta del proyecto y documentar los problemas encontrados y las acciones de limpieza propuestas.

## Pregunta analítica
¿Existe relación entre el número de perros por espacio y los días de estadía con el nivel de estrés observado en perros alojados en una guardería canina?

## Datasets
| Archivo | Contenido |
|---|---|
| `data/raw/perros_ingreso.csv` | Ficha de ingreso: edad, sexo, primera vez, fecha de ingreso, días de estadía |
| `data/raw/observaciones_estres.csv` | Observaciones diarias: perros en el espacio, señales de estrés y nivel de estrés (0 a 3) |

> Los archivos incluidos son **datos de ejemplo simulados**, creados con `scripts/generar_datos_ejemplo.py`, con problemas de calidad incluidos a propósito. Para el proyecto real se reemplazan por las observaciones recolectadas, manteniendo los mismos nombres y columnas.

## Estructura
```
├── README.md
├── .gitignore
├── requirements.txt
├── data/raw/                  # datasets del proyecto
├── notebooks/diagnostico_calidad.ipynb
├── reports/informe_diagnostico.md
└── scripts/generar_datos_ejemplo.py
```

## Cómo reproducir el diagnóstico
```bash
git clone <URL-del-repositorio>
cd estres-canino-diagnostico
python -m venv .venv
.venv\Scripts\activate          # en Windows  (en Linux/Mac: source .venv/bin/activate)
pip install -r requirements.txt
jupyter lab
```
Abrir `notebooks/diagnostico_calidad.ipynb` y ejecutar todas las celdas (*Run All*). Si se quieren regenerar los datos de ejemplo: `python scripts/generar_datos_ejemplo.py`.

## Resultados
El informe con los hallazgos está en [`reports/informe_diagnostico.md`](reports/informe_diagnostico.md).
