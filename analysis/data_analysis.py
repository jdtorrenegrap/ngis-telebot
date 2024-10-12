import pandas as pd
from scipy.stats import f_oneway

def latest_readings(data):
    """
    Obtener las últimas lecturas
    """
    df = pd.DataFrame(data)
    # Convertir la columna de created_at a datetime
    df['created_at'] = pd.to_datetime(df['created_at'])
    # Obtenemos la última lectura
    result = df.sort_values('created_at').groupby(['unit_id', 'device_id']).tail(1)
    return result

def sensor_analysis(data):
    """
    Análisis descriptivo de los datos proporcionados
    """
    df = pd.DataFrame(data)
     # Seleccionamos las columnas que vamos a usar
    df_relevant = df[['device_id', 'unit_id', 'value']]
    # Realizamos una estadísticas descriptiva
    stats = df_relevant['value'].describe()
    # Buscamos el sensor que más datos recolectó
    sensor_plus_data = df_relevant['device_id'].value_counts().idxmax()

    # Formateaamos el resultado
    result = "📊 Análisis Descriptivo de Lecturas 📊\n\n"
    result += "🔍 Estadísticas Descriptivas:\n"
    result += f"  - Número de Lecturas: {stats['count']:.0f}\n"
    result += f"  - Promedio de Valores: {stats['mean']:.2f}\n"
    result += f"  - Desviación Estándar: {stats['std']:.2f}\n"
    result += f"  - Valor Mínimo: {stats['min']:.2f}\n"
    result += f"  - Percentil 25: {stats['25%']:.2f}\n"
    result += f"  - Mediana (Percentil 50): {stats['50%']:.2f}\n"
    result += f"  - Percentil 75: {stats['75%']:.2f}\n"
    result += f"  - Valor Máximo: {stats['max']:.2f}\n\n"
    result += f"📈 El sensor que más datos recolectó fue: {sensor_plus_data}\n"
    return result

def analyze_trends(data):
    """
    Analizar tendencias temporales en los datos proporcionados
    """

    df = pd.DataFrame(data)
    # Seleccionamos las columnas que vamos a usar
    df_relevant = df[['value', 'unit_id', 'device_id', 'created_at']]
    # Convertir la columna de created_at a datetime
    df_relevant['created_at'] = pd.to_datetime(df_relevant['created_at'])
    # Agrupamos por día, unidad y dispositivo, y calculamos estadística diaria
    daily_trends = df_relevant.set_index('created_at').groupby(['device_id', 'unit_id']).resample('D').agg({
        'value': ['mean', 'min', 'max', 'std']
    }).reset_index()

    # Aplanar el índice jerárquico
    daily_trends.columns = ['device_id', 'unit_id', 'created_at', 'mean', 'min', 'max', 'std']

    # Agrupar por sensor y unidad para obtener estadísticas generales
    overall_trends = daily_trends.groupby(['device_id', 'unit_id']).agg({
        'mean': 'mean',
        'min': 'min',
        'max': 'max',
        'std': 'mean'
    }).reset_index()

    # Formateamos los resultados
    result = "📈 Tendencias Temporales por Sensor y Unidad 📈\n\n"
    for _, row in overall_trends.iterrows():
        result += (
            f"🔹 Sensor: {row['device_id']}, Unidad: {row['unit_id']}\n"
            f"  - Promedio Diario: {row['mean']:.2f}\n"
            f"  - Valor Mínimo Diario: {row['min']:.2f}\n"
            f"  - Valor Máximo Diario: {row['max']:.2f}\n"
            f"  - Desviación Estándar Diaria: {row['std']:.2f}\n\n"
        )

    return result
def compare_sensors(data):
    """
    Comparar datos entre diferentes sensores para detectar diferencias significativas
    """

    df = pd.DataFrame(data)
    # Seleccionamos las columnas que vamos a usar
    df_relevant = df[['device_id', 'value']]
    # Agrupar los datos por sensor
    grouped = df_relevant.groupby('device_id')['value'].apply(list)
    # Realizar la prueba ANOVA para detectar diferencias significativas
    anova_result = f_oneway(*grouped)
    # Formateamos el resultado
    result = "📊 Comparación entre Sensores 📊\n\n"
    result += "🔍 Resultados de la Prueba ANOVA:\n"
    result += f"  - Estadístico F: {anova_result.statistic:.2f}\n"
    result += f"  - Valor p: {anova_result.pvalue:.2e}\n\n"

    if anova_result.pvalue < 0.05:
        result += "✅ Conclusión: Hay diferencias significativas entre los sensores.\n\n"
        result += "📋 Detalles por Sensor:\n"
        for sensor, values in grouped.items():
            result += (
                f"  - Sensor {sensor}:\n"
                f"    - Número de Lecturas: {len(values)}\n"
                f"    - Promedio: {pd.Series(values).mean():.2f}\n"
                f"    - Desviación Estándar: {pd.Series(values).std():.2f}\n"
            )
    else:
        result += "❌ Conclusión: No hay diferencias significativas entre los sensores.\n"

    return result