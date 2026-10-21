import pandas as pd
import numpy as np
# ============================================================
# SIMULACIÓN DE SOLICITUDES DE CRÉDITO BANCARIO (OLTP)
# ============================================================

np.random.seed(101)

n = 500

df_operativo = pd.DataFrame({

    'id_credito': range(1000, 1000 + n),

    'fecha_solicitud': pd.date_range(
        start='2026-01-01',
        periods=n,
        freq='h'
    ),

    'cliente_nombre': np.random.choice(
        [
            'Juan Pérez',
            'María Gómez',
            'Carlos Ruiz',
            'Ana López',
            'Luis Hernández'
        ],
        n
    ),

    'cliente_ciudad': np.random.choice(
        [
            'Puebla',
            'CDMX',
            'Guadalajara',
            'Monterrey'
        ],
        n
    ),

    'tipo_credito': np.random.choice(
        [
            'Personal',
            'Automotriz',
            'Hipotecario',
            'Empresarial'
        ],
        n
    ),

    'plazo_meses': np.random.choice(
        [12, 24, 36, 48, 60, 120],
        n
    ),

    'tasa_interes': np.random.choice(
        [8.5, 10.5, 12.5, 15.0, 18.0],
        n
    ),

    'monto_solicitado': np.random.choice(
        [
            10000.0,
            25000.0,
            50000.0,
            100000.0,
            250000.0,
            500000.0,
            850000.0
        ],
        n
    ),

    'estatus_credito': np.random.choice(
        [
            'Aprobado',
            'Rechazado',
            'Pendiente'
        ],
        n,
        p=[0.60, 0.25, 0.15]
    )
})


# ============================================================
# 1. CONSTRUCCIÓN DE DIMENSIÓN CLIENTE
# ============================================================

dim_cliente = (
    df_operativo[
        [
            'cliente_nombre',
            'cliente_ciudad'
        ]
    ]
    .drop_duplicates()
    .reset_index(drop=True)
)

dim_cliente['id_cliente_sk'] = (
    dim_cliente.index + 1
)


# ============================================================
# 2. CONSTRUCCIÓN DE DIMENSIÓN TIPO DE CRÉDITO
# ============================================================

dim_tipo_credito = (
    df_operativo[
        [
            'tipo_credito',
            'plazo_meses',
            'tasa_interes'
        ]
    ]
    .drop_duplicates()
    .reset_index(drop=True)
)

dim_tipo_credito['id_tipo_credito_sk'] = (
    dim_tipo_credito.index + 1
)


# ============================================================
# 3. CONSTRUCCIÓN DE DIMENSIÓN TIEMPO
# ============================================================

dim_tiempo = pd.DataFrame({

    'fecha_completa':
        df_operativo[
            'fecha_solicitud'
        ].dt.date.unique()
})

dim_tiempo['fecha_completa'] = pd.to_datetime(
    dim_tiempo['fecha_completa']
)

dim_tiempo['id_tiempo_sk'] = (
    dim_tiempo['fecha_completa']
    .dt.strftime('%Y%m%d')
    .astype(int)
)

dim_tiempo['anio'] = (
    dim_tiempo['fecha_completa']
    .dt.year
)

dim_tiempo['mes'] = (
    dim_tiempo['fecha_completa']
    .dt.month
)

dim_tiempo['dia'] = (
    dim_tiempo['fecha_completa']
    .dt.day
)


# ============================================================
# 4. CONSTRUCCIÓN DE LA TABLA DE HECHOS
# ============================================================

fact_creditos = (
    df_operativo

    .merge(
        dim_cliente,
        on=[
            'cliente_nombre',
            'cliente_ciudad'
        ]
    )

    .merge(
        dim_tipo_credito,
        on=[
            'tipo_credito',
            'plazo_meses',
            'tasa_interes'
        ]
    )
)


# ============================================================
# 5. PREPARACIÓN DE LA FECHA
# ============================================================

fact_creditos['fecha_completa'] = pd.to_datetime(
    fact_creditos[
        'fecha_solicitud'
    ].dt.date
)


# ============================================================
# 6. INCORPORACIÓN DE LA DIMENSIÓN TIEMPO
# ============================================================

fact_creditos = fact_creditos.merge(
    dim_tiempo,
    on='fecha_completa'
)


# ============================================================
# 7. CÁLCULO DEL MONTO APROBADO
# ============================================================

fact_creditos['monto_aprobado'] = np.where(

    fact_creditos['estatus_credito'] == 'Aprobado',

    fact_creditos['monto_solicitado']
    * np.random.uniform(
        0.80,
        1.00,
        len(fact_creditos)
    ),

    0
)

fact_creditos['monto_aprobado'] = (
    fact_creditos[
        'monto_aprobado'
    ].round(2)
)


# ============================================================
# 8. SELECCIÓN FINAL DE LA TABLA DE HECHOS
# ============================================================

fact_table = fact_creditos[
    [
        'id_credito',
        'id_cliente_sk',
        'id_tipo_credito_sk',
        'id_tiempo_sk',
        'monto_solicitado',
        'monto_aprobado',
        'estatus_credito'
    ]
]


# ============================================================
# 9. VISUALIZACIÓN
# ============================================================

print("\n==========================================")
print("       DATOS OPERATIVOS OLTP")
print("==========================================")

print(df_operativo.head())


print("\n==========================================")
print("       DIMENSIÓN CLIENTE")
print("==========================================")

print(dim_cliente)


print("\n==========================================")
print("       DIMENSIÓN TIPO DE CRÉDITO")
print("==========================================")

print(dim_tipo_credito)


print("\n==========================================")
print("       DIMENSIÓN TIEMPO")
print("==========================================")

print(dim_tiempo.head())


print("\n==========================================")
print("       TABLA DE HECHOS")
print("       FACT_CREDITOS")
print("==========================================")

print(fact_table.head())


# ============================================================
# 10. RESUMEN DE INFORMACIÓN
# ============================================================

print("\n==========================================")
print("             RESUMEN")
print("==========================================")

print(
    f"Total de solicitudes: "
    f"{len(fact_table)}"
)

print(
    f"Total solicitado: "
    f"${fact_table['monto_solicitado'].sum():,.2f}"
)

print(
    f"Total aprobado: "
    f"${fact_table['monto_aprobado'].sum():,.2f}"
)


print("\n==========================================")
print("       SOLICITUDES POR ESTATUS")
print("==========================================")

print(
    fact_table[
        'estatus_credito'
    ].value_counts()
)
