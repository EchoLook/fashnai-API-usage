# Instrucciones de Configuración

## Configuración del Entorno

1. Crea un entorno virtual de Python:
```bash
python -m venv venv
```

2. Activa el entorno virtual:
- En Windows:
  ```bash
  venv\Scripts\activate
  ```
- En Linux/Mac:
  ```bash
  source venv/bin/activate
  ```

3. Instala las dependencias con versiones específicas:
```bash
pip install -r requirements.txt
```

4. Crea un archivo `.env` con tu clave API de Fashn.ai:
```
FASHN_API_KEY=your_api_key_here
```

## Ejecutando la Aplicación

Una vez que la configuración esté completa, puedes ejecutar la aplicación:

```bash
streamlit run app.py
```

La interfaz de Streamlit debería abrirse en tu navegador web predeterminado en http://localhost:8501.

## Solución de Problemas

Si encuentras errores:

1. **Dependencias faltantes**: Asegúrate de estar usando las versiones exactas en requirements.txt
2. **Problemas con la clave API**: Verifica que tu clave API esté correctamente configurada en el archivo .env
3. **Problemas con el formato de imagen**: Asegúrate de que tus imágenes estén en un formato estándar (JPG, PNG)
4. **Errores de red**: Verifica tu conexión a internet, ya que la aplicación necesita comunicarse con la API de Fashn.ai
5. **Problemas con la cámara web**: Si la cámara no funciona, asegúrate de:
   - Haber concedido permisos de cámara a tu navegador
   - Estar usando un navegador moderno y actualizado (Chrome, Firefox, Edge)
   - Que tu cámara web esté funcionando correctamente con otras aplicaciones

## Compatibilidad de Versiones

- Se recomienda Python 3.7+
- La aplicación fue probada con las versiones exactas de dependencias en requirements.txt

## Uso de la Aplicación

1. Carga una foto de una persona usando el botón de carga o toma una foto con la cámara web
2. Carga una foto de una prenda de ropa usando el botón de carga o toma una foto con la cámara web
3. Selecciona la categoría de ropa apropiada (o déjala como "auto")
4. Haz clic en "Generate Try-On" para procesar las imágenes
5. Espera a que aparezca el resultado (puede tomar hasta 40 segundos)
6. La imagen resultante mostrará la prenda de ropa virtualmente probada en la persona
7. Utiliza el botón "Download Result" para guardar la imagen generada

## Consejos para Mejores Resultados

1. **Calidad de imagen**: Para mejores resultados, usa imágenes claras y bien iluminadas
2. **Pose de la persona**: Las imágenes frontales funcionan mejor para la mayoría de las prendas
3. **Tipo de prenda**: Selecciona correctamente la categoría de la prenda para mejorar el resultado
4. **Al usar la cámara**: Busca buena iluminación y un fondo simple si es posible 