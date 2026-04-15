import pandas as pd
import json
import os

print("🚀 Generando datos actualizados...")

# 1. CUMPLEAÑOS
df_alumnos = pd.read_excel("datos_privados/Alumnos.xlsx", sheet_name="export-2")
df_alumnos['fecha'] = pd.to_datetime(df_alumnos['Data de Nascimento']).dt.strftime('%d/%m')

eventos = []
for _, row in df_alumnos.iterrows():
    nombre = str(row['Nome']).strip()
    turma = str(row['Turmas']).strip()
    eventos.append({
        "fecha": row['fecha'],
        "tipo": "cumpleaños",
        "descripcion": f"Aniversário de {nombre} {turma}"
    })
print(f" • {len(eventos)} cumpleaños cargados")

# 2. DÍAS ESPECIALES
df_especiales = pd.read_excel("datos_privados/Menu del dia.xlsx", sheet_name="DiasEspeciales")
for _, row in df_especiales.iterrows():
    dia_raw = row.iloc[0]
    if pd.isna(dia_raw): continue
    if isinstance(dia_raw, pd.Timestamp) or 'datetime' in str(type(dia_raw)).lower():
        fecha = dia_raw.strftime('%d/%m')
    else:
        try:
            fecha = pd.to_datetime(dia_raw, unit='D', origin='1899-12-30').strftime('%d/%m')
        except:
            try:
                fecha = pd.to_datetime(dia_raw).strftime('%d/%m')
            except:
                fecha = str(dia_raw).strip()[:5]
    desc = str(row.iloc[1]).strip()
    if fecha and desc and desc != "nan" and desc != "":
        eventos.append({"fecha": fecha, "tipo": "especial", "descripcion": desc})
print(f" • {len([e for e in eventos if e['tipo'] == 'especial'])} días especiales cargados")

# 3. MENÚ
df_menu = pd.read_excel("datos_privados/Menu del dia.xlsx", sheet_name="MenuSimple")
menu = {}
for _, row in df_menu.iterrows():
    dia_raw = row.iloc[0]
    if pd.isna(dia_raw): continue
    try:
        fecha = pd.to_datetime(dia_raw, unit='D', origin='1899-12-30').strftime('%d/%m')
    except:
        try:
            fecha = pd.to_datetime(dia_raw).strftime('%d/%m')
        except:
            fecha = str(dia_raw).strip()[:5]
    desc = str(row.iloc[1]).strip()
    if desc and desc != "nan" and len(desc) > 10:
        menu[fecha] = desc
print(f" • {len(menu)} días de menú cargados")

# 4. FOTOS Y VÍDEOS
imagenes = ["fotos/" + f for f in os.listdir("fotos") if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.webm', '.mov', '.avi'))]
print(f" • {len(imagenes)} archivos en galería (fotos + vídeos)")

# 5. MENSAJE PERSONALIZADO
mensaje_hoy = ""
try:
    df_mensaje = pd.read_excel("datos_privados/Menu del dia.xlsx", sheet_name="MensajeDia")
    hoy_str = pd.to_datetime('today').strftime('%d/%m')
    for _, row in df_mensaje.iterrows():
        dia_raw = row.iloc[0]
        if pd.isna(dia_raw): continue
        if isinstance(dia_raw, pd.Timestamp) or 'datetime' in str(type(dia_raw)).lower():
            fecha = dia_raw.strftime('%d/%m')
        else:
            try:
                fecha = pd.to_datetime(dia_raw, unit='D', origin='1899-12-30').strftime('%d/%m')
            except:
                fecha = pd.to_datetime(dia_raw).strftime('%d/%m')
        texto = str(row.iloc[1]).strip()
        if fecha == hoy_str and texto and texto != "nan":
            mensaje_hoy = texto
            break
    with open("mensaje_dia.json", "w", encoding="utf-8") as f:
        json.dump(mensaje_hoy, f, ensure_ascii=False)
    print(" • Mensaje personalizado cargado" if mensaje_hoy else " • No hay mensaje personalizado hoy → se usa Wikipedia")
except:
    print(" • No existe hoja MensajeDia o hay un error")

# GUARDAR JSONs
with open("eventos.json", "w", encoding="utf-8") as f:
    json.dump(eventos, f, ensure_ascii=False, indent=2)
with open("menu.json", "w", encoding="utf-8") as f:
    json.dump(menu, f, ensure_ascii=False, indent=2)
with open("fotos.json", "w", encoding="utf-8") as f:
    json.dump(imagenes, f, ensure_ascii=False, indent=2)

print("✅ TODO GENERADO CORRECTAMENTE")
