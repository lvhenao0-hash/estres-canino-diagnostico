"""Genera datos de EJEMPLO (simulados) para el diagnóstico de calidad.

Los datos NO son reales: sirven para practicar el diagnóstico mientras se
recolectan las observaciones reales en la guardería. Se incluyen a propósito
algunos problemas de calidad (faltantes, tipos mal definidos, valores
imposibles y duplicados) para poder diagnosticarlos.
Uso:  python scripts/generar_datos_ejemplo.py
"""
from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

N_PERROS = 60

# ---------- Dataset 1: ficha de ingreso de cada perro ----------
perros = pd.DataFrame({
    "perro_id": [f"P{i:03d}" for i in range(1, N_PERROS + 1)],
    "edad_anios": rng.integers(1, 13, N_PERROS).astype(float),
    "sexo": rng.choice(["Macho", "Hembra"], N_PERROS),
    "primera_vez_guarderia": rng.choice(["Si", "No"], N_PERROS, p=[0.4, 0.6]),
    "fecha_ingreso": pd.to_datetime("2026-09-01")
        + pd.to_timedelta(rng.integers(0, 40, N_PERROS), unit="D"),
    "dias_estadia_total": rng.integers(2, 11, N_PERROS),
})
perros["fecha_ingreso"] = perros["fecha_ingreso"].dt.strftime("%d/%m/%Y")

# problemas intencionales
perros.loc[rng.choice(N_PERROS, 5, replace=False), "edad_anios"] = np.nan
perros.loc[rng.choice(N_PERROS, 4, replace=False), "primera_vez_guarderia"] = np.nan
perros.loc[7, "edad_anios"] = -3
perros.loc[21, "edad_anios"] = 45
perros.loc[[12, 33], "sexo"] = ["macho ", "HEMBRA"]            # categorías inconsistentes
perros = pd.concat([perros, perros.iloc[[4]]], ignore_index=True)  # duplicado exacto

# ---------- Dataset 2: observaciones diarias ----------
filas = []
oid = 1
for _, p in perros.drop_duplicates("perro_id").iterrows():
    for dia in range(1, int(p["dias_estadia_total"]) + 1):
        n_espacio = int(rng.integers(3, 21))
        base = 0.08 * n_espacio + (0.5 if p["primera_vez_guarderia"] == "Si" else 0) - 0.05 * dia
        nivel = int(np.clip(round(base + rng.normal(0, 0.6)), 0, 3))
        filas.append({
            "obs_id": oid, "perro_id": p["perro_id"], "dia_estadia": dia,
            "perros_en_espacio": n_espacio,
            "jadeo": int(rng.random() < 0.15 + 0.12 * nivel),
            "temblor": int(rng.random() < 0.05 + 0.10 * nivel),
            "ladrido_excesivo": int(rng.random() < 0.10 + 0.15 * nivel),
            "rechazo_alimento": int(rng.random() < 0.05 + 0.12 * nivel),
            "nivel_estres": nivel,
        })
        oid += 1
obs = pd.DataFrame(filas)
obs["perros_en_espacio"] = obs["perros_en_espacio"].astype(object)

idx = rng.choice(len(obs), 25, replace=False)
obs.loc[idx[:12], "perros_en_espacio"] = np.nan
obs.loc[idx[12:18], "nivel_estres"] = np.nan
obs.loc[idx[18], "nivel_estres"] = 5                    # fuera de la escala 0-3
obs.loc[idx[19], "nivel_estres"] = -1
obs.loc[idx[20], "dia_estadia"] = 0                     # día imposible
obs.loc[idx[21], "perros_en_espacio"] = 120             # atípico
obs.loc[idx[22], "perros_en_espacio"] = "12 perros"     # texto en columna numérica
obs.loc[idx[23], "perros_en_espacio"] = "ocho"
obs.loc[idx[24], "perro_id"] = "P999"                   # perro sin ficha de ingreso
obs.loc[idx[:3], "jadeo"] = np.nan
obs = pd.concat([obs, obs.iloc[[10, 55]]], ignore_index=True)  # duplicados

perros.to_csv(RAW / "perros_ingreso.csv", index=False)
obs.to_csv(RAW / "observaciones_estres.csv", index=False)
print("Archivos generados en", RAW)
