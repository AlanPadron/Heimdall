import statistics
import logging

# Configuramos un logger para esta capa de dominio
logger = logging.getLogger(__name__)

class AnomalyDetector:
    """
    Servicio de Dominio encargado de analizar si una lectura se desvía 
    del comportamiento normal utilizando Z-Score.
    """
    def __init__(self, threshold: float = 3.0):
        # El threshold define cuántas desviaciones estándar permitimos
        self.threshold = threshold 

    def is_anomalous(self, current_value: float, history: list[float]) -> bool:
        """
        Calcula si el valor actual es una anomalía basándose en el historial.
        """
        # Validación: Necesitamos un mínimo de datos para que la estadística sea válida
        if not history or len(history) < 5:
            logger.info(f"Historial insuficiente ({len(history)} datos). Omitiendo detección.")
            return False
            
        try:
            mean = statistics.mean(history)
            stdev = statistics.stdev(history)
            
            # Si no hay variación en el historial, cualquier cambio mínimo no debería 
            # disparar una alerta de división por cero.
            if stdev == 0:
                return current_value != mean
                
            # Cálculo del Z-Score: (Valor - Media) / Desviación Estándar
            z_score = abs(current_value - mean) / stdev
            
            logger.info(f"Análisis: Valor={current_value}, Media={mean:.2f}, Z-Score={z_score:.2f}")
            
            return z_score > self.threshold
            
        except Exception as e:
            logger.error(f"Error en el cálculo estadístico: {e}")
            return False