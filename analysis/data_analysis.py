import pandas as pd
from scipy.stats import f_oneway

def latest_readings(data):
    """
    Obtener las últimas lecturas.
    """
    df = pd.DataFrame(data)
    df['created_at'] = pd.to_datetime(df['created_at'])  # Convertir la columna de created_at a datetime
    result = df.sort_values('created_at').groupby(['unit_id', 'device_id']).tail(1)  # Obtener la última lectura
    return result

def sensor_analysis(data):
    """
    Análisis descriptivo de los datos proporcionados.
    """
    df = pd.DataFrame(data)
    df_relevant = df[['device_id', 'unit_id', 'value']]  # Seleccionamos las columnas que vamos a usar
    stats = df_relevant['value'].describe()  # Realizamos una estadísticas descriptiva
    sensor_plus_data = df_relevant['device_id'].value_counts().idxmax()  # Buscamos el sensor que más datos recolectó

    # Formateamos el resultado
    result = "📊 Análisis Descriptivo de Lecturas 📊\n\n"
    result += "🔍 Estadísticas Descriptivas:\n"
    result += f"  - Número de Lecturas: {stats['count']:.0f} lecturas registradas\n"
    result += f"  - Promedio de Valores: {stats['mean']:.2f} - Este es el valor medio de todas las lecturas\n"
    result += f"  - Desviación Estándar: {stats['std']:.2f} - Indica cuánto varían las lecturas respecto al promedio\n"
    result += f"  - Valor Mínimo: {stats['min']:.2f} - La lectura más baja registrada\n"
    result += f"  - Percentil 25: {stats['25%']:.2f} - El 25% de las lecturas son menores que este valor\n"
    result += f"  - Mediana (Percentil 50): {stats['50%']:.2f} - El valor medio que separa las lecturas en dos mitades\n"
    result += f"  - Percentil 75: {stats['75%']:.2f} - El 75% de las lecturas son menores que este valor\n"
    result += f"  - Valor Máximo: {stats['max']:.2f} - La lectura más alta registrada\n\n"
    result += f"📈 El sensor que más datos recolectó fue: {sensor_plus_data}\n"
    return result

def analyze_trends(data):
    """
    Analizar tendencias temporales en los datos proporcionados.
    """
    df = pd.DataFrame(data)
    df_relevant = df[['value', 'unit_id', 'device_id', 'created_at']]  # Seleccionamos las columnas que vamos a usar
    df_relevant['created_at'] = pd.to_datetime(df_relevant['created_at'])  # Convertir la columna de created_at a datetime
    daily_trends = df_relevant.set_index('created_at').groupby(['device_id', 'unit_id']).resample('D').agg({
        'value': ['mean', 'min', 'max', 'std']
    }).reset_index()  # Agrupamos por día, unidad y dispositivo, y calculamos estadística diaria
    
    daily_trends.columns = ['device_id', 'unit_id', 'created_at', 'mean', 'min', 'max', 'std']  # Aplanar el índice jerárquico
    
    overall_trends = daily_trends.groupby(['device_id', 'unit_id']).agg({
        'mean': 'mean',
        'min': 'min',
        'max': 'max',
        'std': 'mean'
    }).reset_index()  # Agrupar por sensor y unidad para obtener estadísticas generales

    # Formateamos los resultados
    result = "Tendencias Temporales por Sensor y Unidad\n\n"
    for _, row in overall_trends.iterrows():
        result += (
            f"Sensor: {row['device_id']}, Unidad: {row['unit_id']}\n"
            f"  - 📅 Promedio Diario: {row['mean']:.2f} - Este es el promedio de las lecturas diarias.\n"
            f"  - 📉 Valor Mínimo Diario: {row['min']:.2f} - La lectura más baja registrada en el día.\n"
            f"  - 📈 Valor Máximo Diario: {row['max']:.2f} - La lectura más alta registrada en el día.\n"
            f"  - 📊 Desviación Estándar Diaria: {row['std']:.2f} - Indica la variabilidad de las lecturas diarias.\n\n"
        )
    return result

def compare_sensors(data):
    """
    Comparar datos entre diferentes sensores para detectar diferencias significativas.
    """
    df = pd.DataFrame(data)
    df_relevant = df[['device_id', 'value']]  # Seleccionamos las columnas que vamos a usar
    grouped = df_relevant.groupby('device_id')['value'].apply(list)  # Agrupar los datos por sensor
    anova_result = f_oneway(*grouped)  # Realizar la prueba ANOVA
    
    # Formateamos el resultado
    result = "📊 Comparación entre Sensores 📊\n\n"
    result += "🔍 Resultados de la Prueba ANOVA:\n"
    result += f"  - Estadístico F: {anova_result.statistic:.2f} - Mide la variabilidad entre los grupos.\n"
    result += f"  - Valor p: {anova_result.pvalue:.2e} - Indica la probabilidad de que las diferencias sean aleatorias.\n\n"

    if anova_result.pvalue < 0.05:
        result += "✅ Conclusión: Hay diferencias significativas entre los sensores.\n\n"
        result += "📋 Detalles por Sensor:\n"
        for sensor, values in grouped.items():
            result += (
                f"  - Sensor {sensor}:\n"
                f"    - Número de Lecturas: {len(values)}\n"
                f"    - Promedio: {pd.Series(values).mean():.2f} - El valor promedio de las lecturas.\n"
                f"    - Desviación Estándar: {pd.Series(values).std():.2f} - Indica la variabilidad de las lecturas.\n\n"
            )
    else:
        result += "❌ Conclusión: No hay diferencias significativas entre los sensores.\n"
    return result