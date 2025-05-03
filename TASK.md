# TASK.md - Proyecto de Cambio de Ropa Virtual

## Tareas Actuales

### Configuración Inicial
- [x] Crear repositorio en GitHub para el proyecto
- [x] Configurar estructura básica del proyecto (frontend/backend)
- [x] Establecer entorno de desarrollo local

### Investigación y Pruebas de API
- [x] Registrar cuenta de desarrollador en Fashn.ai
- [x] Obtener API key para desarrollo
- [x] Realizar pruebas básicas con los endpoints de la API
- [x] Documentar limitaciones y capacidades descubiertas

### Desarrollo Frontend - Fase 1
- [x] Crear wireframes de la interfaz de usuario
- [x] Implementar componente de carga de imágenes
- [x] Desarrollar pantalla de selección de prendas
- [x] Diseñar vista de resultados de cambio de ropa

### Desarrollo Backend - Fase 1
- [x] Configurar servidor para la aplicación
- [x] Implementar rutas para comunicación con la API de Fashn.ai

## Hitos
1. **POC (Prueba de Concepto)**: Implementación básica con la API de Fashn.ai

## Notas y Descubrimientos
- La API de Fashn.ai ofrece capacidades específicas que debemos entender en profundidad
- Necesitamos investigar los tiempos de procesamiento para una mejor experiencia de usuario
- Considerar implementar una cola de procesamiento si la API tiene restricciones de concurrencia
- La API tiene límites de tasa: hasta 50 requests por 60 segundos para /run y 50 requests por 10 segundos para /status
- El procesamiento de imágenes puede tardar hasta 40 segundos según la documentación
