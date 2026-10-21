import pandas as pd
import numpy as np

# ============================================================
# SIMULACIÓN DE INGESTA OPERATIVA (OLTP)
# ============================================================

np.random.seed(101)

n = 500

df_operativo = pd.DataFrame({
    'id_transaccion': range(1000, 1000 + n),

    'fecha_hora': pd.date_range(
        start='2026-01-01',
        periods=n,
        freq='h'
    ),

    'cliente_nombre': np.random.choice(
        ['Juan Pérez', 'María Gómez', 'Carlos Ruiz'],
        n
    ),

    'cliente_ciudad': np.random.choice(
        ['Puebla', 'CDMX', 'Guadalajara'],
        n
    ),

    'producto_nombre': np.random.choice(
        ['Laptop Dell', 'Mouse Logi', 'Monitor LG'],
        n
    ),

    'categoria_prod': np.random.choice(
        ['Cómputo', 'Accesorios', 'Pantallas'],
        n
    ),

    'precio_unitario': np.random.choice(
        [15000.0, 350.0, 4500.0],
        n
    ),

    'cantidad': np.random.randint(
        1,
        5,
        n
    )
})


# ============================================================
# 1. CONSTRUCCIÓN DE DIMENSIÓN CLIENTE
# ============================================================

dim_cliente = (
    df_operativo[
        ['cliente_nombre', 'cliente_ciudad']
    ]
    .drop_duplicates()
    .reset_index(drop=True)
)

# Surrogate Key
dim_cliente['id_cliente_sk'] = (
    dim_cliente.index + 1
)


# ============================================================
# 2. CONSTRUCCIÓN DE DIMENSIÓN PRODUCTO
# ============================================================

dim_producto = (
    df_operativo[
        [
            'producto_nombre',
            'categoria_prod',
            'precio_unitario'
        ]
    ]
    .drop_duplicates()
    .reset_index(drop=True)
)

dim_producto['id_producto_sk'] = (
    dim_producto.index + 1
)


# ============================================================
# 3. CONSTRUCCIÓN DE DIMENSIÓN TIEMPO
# ============================================================

dim_tiempo = pd.DataFrame({
    'fecha_completa':
        df_operativo['fecha_hora'].dt.date.unique()
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
    dim_tiempo['fecha_completa'].dt.year
)

dim_tiempo['mes'] = (
    dim_tiempo['fecha_completa'].dt.month
)

dim_tiempo['dia'] = (
    dim_tiempo['fecha_completa'].dt.day
)


# ============================================================
# 4. CONSTRUCCIÓN DE LA TABLA DE HECHOS
# ============================================================

fact_ventas = df_operativo.merge(
    dim_cliente,
    on=[
        'cliente_nombre',
        'cliente_ciudad'
    ]
)

fact_ventas = fact_ventas.merge(
    dim_producto,
    on=[
        'producto_nombre',
        'categoria_prod',
        'precio_unitario'
    ]
)

# Crear fecha para relacionarla con Dim_Tiempo
fact_ventas['fecha_completa'] = pd.to_datetime(
    fact_ventas['fecha_hora'].dt.date
)

fact_ventas = fact_ventas.merge(
    dim_tiempo,
    on='fecha_completa'
)


# ============================================================
# CALCULAR MONTO TOTAL
# ============================================================

fact_ventas['monto_total'] = (
    fact_ventas['cantidad'] *
    fact_ventas['precio_unitario']
)


# ============================================================
# SELECCIÓN FINAL DE LA FACT TABLE
# ============================================================

fact_table = fact_ventas[
    [
        'id_transaccion',
        'id_cliente_sk',
        'id_producto_sk',
        'id_tiempo_sk',
        'cantidad',
        'monto_total'
    ]
]


# ============================================================
# MOSTRAR RESULTADOS
# ============================================================

print("=" * 70)
print("TABLA DE HECHOS (FACT_VENTAS)")
print("=" * 70)

print(
    fact_table.head(10).to_string(index=False)
)

print()

print("=" * 70)
print("DIMENSIONES")
print("=" * 70)

print(
    f"Filas: {fact_table.shape[0]}"
)

print(
    f"Columnas: {fact_table.shape[1]}"
)

print()

print("=" * 70)
print("TIPOS DE DATOS")
print("=" * 70)

print(fact_table.dtypes)


# ============================================================
# GUARDAR FACT TABLE
# ============================================================

fact_table.to_csv(
    'fact_ventas.csv',
    index=False
)

print()

print("=" * 70)
print("ARCHIVO GENERADO")
print("=" * 70)

print("fact_ventas.csv")