**Morixe – Saracco**

## 1. Claridad y estructura del repositorio

**Fortalezas**:

* README en formato Markdown, con estructura clara, breve y orientada al usuario para que pueda hacer funcionar el repositorio lo antes posible.
* Se identifican claramente los tres archivos principales y su propósito.
* Buen uso de negritas y secciones numeradas para guiar al usuario paso a paso.

**A mejorar**:

* El README es algo escueto en cuanto a la descripción técnica del funcionamiento de los algoritmos. No explica cómo funciona Halftone ni K-Means internamente.
* No hay imágenes de ejemplo ni referencias visuales a los resultados. Es muy importante inlcuir estas imagenes para que el usuario pueda tener una referencia del buen funcionamiento o el esperado a la hora de ejecutarlo.
* Falta estructura de carpetas para resultados (`outputs/`) y entradas de referencia (`inputs/`, si se usara).
* En proximas entregas de proyectos, incluyan `requirements.txt` para facilitar instalación de dependencias.

---

## 2. Código: `main.py`

**Positivo**:

* Flujo de entrada bien planteado: validación de ruta de imagen, selección de método y ejecución.
* Validaciones mínimas incluidas, especialmente para la existencia de la imagen.
* Modularidad aceptable: el `main.py` actúa como coordinador y delega el procesamiento a funciones externas.

**Áreas a pulir**:

* El código principal no está encapsulado en una función `main()`. En proximos trabajos toda la logica principal tiene que ir en una funcion principal que se ejecute una sola vez. Esto mejora y permite modularizar el codigo.
* Los inputs podrían validarse con funciones auxiliares para mayor claridad.
* El nombre de la imagen generada es siempre `"resultado.png"` en todos los casos, lo que sobrescribe resultados anteriores y no permite analizar multiples salidas en una sola sentada. Se puede solucionar colocando simplemente un nombre que consista en el nombre de la imagen de entrada sumado a los parametros empleados en el filtrado seleccionado por el usuario. 

---

## 3. Código: `funciones_halftone.py`

**Puntos fuertes**:

* Buen nivel de segmentación funcional: cada parte del proceso (grilla, radio, dibujo, guardado) está desacoplada.
* Algoritmo implementado correctamente, respetando la lógica de puntos variables según intensidad.
* Comentarios explicativos adecuados y útiles.

**Aspectos criticables**:

* La función `halftone()` tiene dependencias internas fuertes con el input: pregunta directamente por valores en lugar de recibirlos como parámetros. Esto reduce la reutilización.
* Falta control de errores si se pasan valores inválidos por fuera del flujo normal (ej. `angulos` con menos de 3 valores).
* No se contempla mostrar la imagen procesada, solo se guarda.

---

## 4. Código: `funciones_kmeans.py`

**Puntos positivos**:

* Implementación manual del algoritmo, sin uso de librerías externas.
* Correcta utilización de estructuras como diccionarios para representar los clusters.
* Se aplica una lógica clara de inicialización aleatoria, asignación y actualización de centroides.

**Mejoras posibles**:

* La distancia entre colores se calcula de forma reiterada en bucles, sin vectorización, lo cual puede ser ineficiente para imágenes grandes.
* La función `calcular_centroide_mas_cercano()` se repite innecesariamente: se vuelve a llamar en `pintar_por_grupos`, duplicando cálculos.
* No se prevé el caso de que un cluster quede vacío (aunque es poco probable, es importante considerarlo).
* Como en Halftone, todo se guarda como `"resultado.png"` sin opción de personalización o distinción.
* No funciona bien lo del porcentaje, corta en 9%.

---

## 5. Interacción con el usuario

**Observaciones**:

* El programa guía bien al usuario, con mensajes claros y manejo básico de errores.
* Los valores por defecto están bien implementados.
* No hay mensajes finales que indiquen claramente la ubicación o nombre del archivo generado.
* No se muestra la imagen procesada al usuario ni se guarda la versión comparativa (original vs. modificada).
* Falta confirmación de éxito o no al finalizar, algo tan simple como: `"Imagen guardada como resultado.png"` ayudaría.

---

## 6. Recomendaciones generales

* Para los trabajos que tengan que realizar de aca en adelante, conviene encapsular todo el flujo principal en una función `main()` y luego implementar lo que vimos en clase `if __name__ == "__main__":`.
* Usar `os.makedirs("outputs", exist_ok=True)` y guardar cada imagen con un nombre distintivo (por ejemplo: `"halftone_p10_15-45-0.png"`).
* Unificar criterios de estilo: nombres de funciones en snake\_case, variables en minúscula.
* Separar funciones de entrada del usuario de la lógica de procesamiento (no mezclar input() dentro de funciones de filtro).
* Añadir opción para visualizar la imagen generada (`.show()`), si el entorno lo permite.
---

## Conclusión

El trabajo está correctamente resuelto y demuestra comprensión básica de los algoritmos y su aplicación. Se valoran la simplicidad y la claridad general del flujo de usuario. Excelente trabajo!!