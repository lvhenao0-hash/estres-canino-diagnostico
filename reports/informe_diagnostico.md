# Informe técnico: diagnóstico de calidad de datos

**Evidencia:** GA1-220501094-01-AA1-EV05
**Aprendiz:** Laura Vanessa Henao · **Ficha:** 3169901

## 1. Proyecto y pregunta analítica
**Proyecto:** Bienestar canino en guarderías y hoteles para perros.

**Pregunta:** ¿Existe relación entre el número de perros por espacio y los días de estadía con el nivel de estrés observado en perros alojados en una guardería canina?

## 2. Descripción de los datasets
| Dataset | Archivo | Contenido | Relación con la pregunta |
|---|---|---|---|
| `perros` | `perros_ingreso.csv` | Una fila por perro: edad, sexo, primera vez, fecha de ingreso, días de estadía | Datos de control y duración de la estadía |
| `obs` | `observaciones_estres.csv` | Una fila por perro y día: perros en el espacio, señales de estrés, nivel de estrés (0 a 3) | Factores y variable de resultado |

Los datos usados en este diagnóstico son **simulados**, generados para practicar la detección de problemas de calidad. El procedimiento es el mismo con los datos reales.

## 3. Resultados de la inspección estructural
| Dataset | Filas | Columnas | Tipos de datos | Observaciones |
|---|---|---|---|---|
| `perros` | 61 | 6 | texto: 4, decimal: 1, entero: 1 | 60 perros distintos; 1 fila duplicada |
| `obs` | 362 | 9 | entero: 5, texto: 2, decimal: 2 | 2 filas duplicadas; `perros_en_espacio` quedó como texto |

## 4. Valores faltantes, tipos de datos e inconsistencias
**Valores faltantes**
- `perros`: `edad_anios` (5) y `primera_vez_guarderia` (4).
- `obs`: `perros_en_espacio` (12), `nivel_estres` (6) y `jadeo` (3).

**Tipos de datos**
- `perros_en_espacio` debería ser numérica, pero tiene 2 valores con texto («12 perros», «ocho»).
- `fecha_ingreso` está como texto y debería ser fecha.

**Inconsistencias**
- 2 niveles de estrés fuera de la escala 0 a 3.
- 1 día de estadía menor a 1.
- 1 registro con más de 30 perros en el espacio (atípico).
- 2 edades imposibles (negativa o mayor a 25 años).
- 1 observación con un `perro_id` que no existe en la ficha de ingreso.
- `sexo` tiene 4 escrituras distintas para 2 categorías.

## 5. Principales hallazgos y acciones propuestas
| Dataset | Problema | Evidencia | Posible impacto | Acción propuesta |
|---|---|---|---|---|
| `perros` | Faltantes | 5 y 4 nulos | Menos datos de control | Revisar la ficha original; imputar la edad con la mediana solo si es necesario |
| `perros` | Valores imposibles | 2 edades inválidas | Distorsionan promedios | Verificar y corregir, o marcar como nulo |
| `perros` | Duplicados | 1 fila | Cuenta dos veces a un perro | `drop_duplicates()` |
| `perros` | Categorías inconsistentes | 4 valores en `sexo` | Agrupaciones incorrectas | `str.strip()` y `str.capitalize()` |
| `perros` | Tipo de dato | `fecha_ingreso` como texto | No permite cálculos con fechas | `pd.to_datetime(dayfirst=True)` |
| `obs` | Faltantes | 12, 6 y 3 nulos | Se pierden observaciones clave | Completar desde la ficha; excluir si no es posible |
| `obs` | Tipo de dato | `perros_en_espacio` como texto | Impide correlaciones | `pd.to_numeric(errors='coerce')` y corrección manual |
| `obs` | Fuera de rango | 2 niveles fuera de 0-3; 1 día < 1 | Sesgan la relación estudiada | Marcar como nulos y revisar la ficha |
| `obs` | Atípicos | 1 registro con más de 30 perros | Distorsiona la relación con el estrés | Verificar si es error de digitación |
| `obs` | Integridad entre archivos | 1 `perro_id` sin ficha | No se puede unir con los datos del perro | Revisar el identificador o excluir |
| `obs` | Duplicados | 2 filas | Cuenta dos veces la misma observación | `drop_duplicates()` |

## 6. Conclusiones
Los datos son aprovechables, pero necesitan preparación antes de analizar la relación entre perros por espacio, días de estadía y estrés. Lo más urgente es convertir `perros_en_espacio` a numérico, tratar los valores fuera de la escala, eliminar duplicados y resolver los faltantes de las variables clave. Luego de esa preparación quedarían unas 338 observaciones utilizables de las 362 originales.

Dos limitaciones deben tenerse presentes: los datos vienen de una sola guardería, por lo que los resultados no se generalizan, y el nivel de estrés depende de la observación de una persona, lo que exige criterios claros para registrarlo. Como los datos son observacionales, el análisis posterior hablará de relación y no de causa.
