import pandas as pd
from scipy.stats import f_oneway

def sensor_analysis(data):
    """
    Análisis descriptivo de los datos proporcionados
    """

    df = pd.DataFrame(data)

    # Seleccionar las columnas relevantes
    df_relevant = df[['device_id', 'unit_id', 'value']]

    # Obtener estadísticas descriptivas
    stats = df_relevant['value'].describe()

    # Encontrar el sensor que más datos recolectó
    sensor_plus_data = df_relevant['device_id'].value_counts().idxmax()

    # Formatear el resultado
    result = "Análisis descriptivo de lecturas:\n\n"
    result += "Estadísticas descriptivas:\n"
    result += f"  - Número de lecturas: {stats['count']:.0f}\n"
    result += f"  - Promedio de valores: {stats['mean']:.2f}\n"
    result += f"  - Desviación estándar: {stats['std']:.2f}\n"
    result += f"  - Valor mínimo: {stats['min']:.2f}\n"
    result += f"  - Porcentaje 25: {stats['25%']:.2f}\n"
    result += f"  - Porcentaje 50: {stats['50%']:.2f}\n"
    result += f"  - Porcentaje 75: {stats['75%']:.2f}\n"
    result += f"  - Valor máximo: {stats['max']:.2f}\n\n"
    result += f"El sensor que más datos recolectó fue: {sensor_plus_data}\n"

    return result

def analyze_trends(data):
    """
    Analizar tendencias temporales en los datos proporcionados
    """

    df = pd.DataFrame(data)

    # Seleccionar las columnas relevantes
    df_relevant = df[['created_at', 'value', 'unit_id', 'device_id']]

    # Convertir la columna de created_at a datetime
    df_relevant['created_at'] = pd.to_datetime(df_relevant['created_at'])

    # Agrupar por día, unidad y dispositivo, y calcular estadísticas diarias
    daily_trends = df_relevant.set_index('created_at').groupby(['device_id', 'unit_id']).resample('D').agg({
        'value': ['mean', 'min', 'max', 'std']
    }).reset_index()

    # Aplanar el índice jerárquico
    daily_trends.columns = ['device_id', 'unit_id', 'created_at', 'mean', 'min', 'max', 'std']

    # Formatear el resultado
    result = "Tendencias temporales por sensor y unidad:\n\n"
    for (device_id, unit_id), group in daily_trends.groupby(['device_id', 'unit_id']):
        result += f"Sensor: {device_id}, Unidad: {unit_id}\n"
        result += group[['created_at', 'mean', 'min', 'max', 'std']].to_string(index=False, header=['Fecha', 'Promedio', 'Mínimo', 'Máximo', 'Desviación Estándar'])
        result += "\n\n"

    return result

def compare_sensors(data):
    """
    Comparar datos entre diferentes sensores para detectar diferencias significativas
    """

    df = pd.DataFrame(data)

    # Seleccionar las columnas relevantes
    df_relevant = df[['device_id', 'value']]

    # Agrupar los datos por sensor
    grouped = df_relevant.groupby('device_id')['value'].apply(list)

    # Realizar la prueba ANOVA para detectar diferencias significativas
    anova_result = f_oneway(*grouped)

    # Formatear el resultado
    result = "Comparación entre sensores:\n\n"
    result += "Resultados de la prueba ANOVA:\n"
    result += f"  - Estadístico F: {anova_result.statistic:.2f}\n"
    result += f"  - Valor p: {anova_result.pvalue:.2e}\n\n"

    if anova_result.pvalue < 0.05:
        result += "Conclusión: Hay diferencias significativas entre los sensores.\n\n"
        result += "Detalles por sensor:\n"
        for sensor, values in grouped.items():
            result += f"  - Sensor {sensor}: {len(values)} lecturas, promedio {pd.Series(values).mean():.2f}, desviación estándar {pd.Series(values).std():.2f}\n"
    else:
        result += "Conclusión: No hay diferencias significativas entre los sensores.\n"

    return result