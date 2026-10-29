DOCUMENTACIÓN TÉCNICA DEL PROYECTO DE ASISTENCIA QR

1. Objetivo del proyecto
   El proyecto consiste en una aplicación web para registrar asistencia mediante un formulario accesible desde un código QR.
   Su finalidad es facilitar el registro de personas sin necesidad de instalar una aplicación móvil. Los usuarios escanean el código QR con la cámara de su celular, acceden a un formulario web, ingresan su nombre y apellido y envían la información.
   El sistema procesa los datos utilizando Python y Flask, valida los campos ingresados y almacena cada registro en un archivo Excel.
Cada asistencia incluye:
   - Identificador único de asistencia.
   - Nombre.
   - Apellido.
   - Fecha del registro.
   - Hora del registro.
El proyecto funciona localmente en un computador que actúa como servidor. Otros dispositivos pueden acceder al formulario siempre que exista conectividad entre ellos y el computador servidor.

2. Estructura del proyecto
   La estructura general es la siguiente:
   proyecto/
   ├── .env
   ├── app.py
   ├── generar_qr.py
   ├── requirements.txt
   ├── templates/
   │   ├── asistencia.html
   │   ├── confirmacion.html
   │   └── qr.html
   ├── data/
   │   └── asistencias.xlsx
   └── static/
      └── codigo_qr.png

   Descripción de los archivos y directorios
   Archivo o carpeta	Función
   .env	             Almacena la configuración de la dirección IP y el puerto.
   app.py	          Contiene la lógica principal del servidor Flask y el registro de asistencias.
   generar_qr.py	    Genera la imagen del código QR con la dirección del formulario.
   requirements.txt   Enumera las bibliotecas de Python necesarias para ejecutar el proyecto.
   templates/	       Contiene las plantillas HTML que se muestran en el navegador.
   asistencia.html	 Presenta el formulario para ingresar los datos de la persona.
   confirmacion.html	 Presenta el resultado del registro de asistencia.
   qr.html	          Presenta la página destinada a mostrar el código QR.
   data/	             Almacena los datos de asistencia.
   asistencias.xlsx	 Archivo Excel donde se guardan los registros.
   static/	          Almacena archivos estáticos utilizados por la aplicación.
   codigo_qr.png	    Imagen del código QR generado por el script.

   Los archivos asistencias.xlsx y codigo_qr.png pueden generarse automáticamente. No es obligatorio que existan antes de ejecutar el proyecto, siempre que se ejecute correctamente el código que los crea.

3. Tecnologías y bibliotecas utilizadas

3.1. Python
   Python es el lenguaje de programación utilizado para desarrollar la aplicación.

   Se encarga de:
   - Ejecutar el servidor web.
   - Procesar la información del formulario.
   - Validar los datos ingresados.
   - Generar identificadores de asistencia.
   - Obtener la fecha y hora.
   - Guardar los registros en Excel.
   - Generar el código QR mediante un script independiente.

3.2. Flask
   Flask es un framework web de Python que permite crear aplicaciones web.
   En este proyecto se utiliza para definir las rutas de acceso, recibir las solicitudes de los navegadores y mostrar las páginas HTML.

   Las rutas principales son:
   - /: muestra el formulario de asistencia.
   - /registrar: recibe y procesa el formulario.
   - /qr: muestra la página del código QR.
   Flask también permite devolver respuestas con códigos HTTP, por ejemplo, un código 400 cuando los datos no cumplen las validaciones.
   3.3. Jinja2
   Jinja2 es el motor de plantillas que utiliza Flask para generar las páginas HTML.
   Permite enviar información desde Python hacia los archivos HTML.
   Por ejemplo, cuando se registra una asistencia correctamente, Flask envía el identificador y el nombre de la persona a confirmacion.html.
   Cuando ocurre un error de validación, puede enviar un mensaje para que aparezca en asistencia.html.
   Jinja2 se instala automáticamente como dependencia de Flask.

3.4. python-dotenv
   La biblioteca python-dotenv permite leer las variables de configuración almacenadas en el archivo .env.

   En este proyecto se utiliza para cargar:
   - IP_LOCAL: dirección IPv4 del computador servidor.
   - PORT: puerto en el que se ejecutará la aplicación.
   Esto evita tener que escribir directamente la IP y el puerto dentro del código fuente.

3.5. pathlib
   La clase Path, de la biblioteca estándar de Python, permite construir y administrar rutas de archivos y carpetas.
   Se utiliza para identificar la ubicación del proyecto y construir rutas como:
   BASE_DIR = Path(__file__).resolve().parent
   Así, el programa puede encontrar los archivos del proyecto independientemente de la carpeta desde la que se ejecute el comando.

3.6. openpyxl
   openpyxl es la biblioteca que permite trabajar con archivos de Excel con extensión .xlsx.
   En este proyecto permite:
   - Crear el archivo Excel.
   - Crear la hoja de asistencias.
   - Definir los encabezados.
   - Abrir el archivo existente.
   - Agregar nuevas filas.
   - Guardar los cambios.
   No es necesario tener Microsoft Excel instalado para que Python pueda crear y modificar el archivo.

3.7. qrcode
   La biblioteca qrcode permite generar códigos QR a partir de texto.
   En este proyecto, el texto que se convierte en QR es la dirección web del formulario.
   Por ejemplo: http://192.111.1.20:5000/
   La biblioteca genera una imagen que se guarda en static/codigo_qr.png.

3.8. Otras bibliotecas
   Biblioteca	Función
   os	            Lee las variables de entorno.
   datetime	      Obtiene la fecha y la hora del registro.
   uuid	         Genera valores que sirven para identificar cada asistencia.
   threading.Lock	Coordina el acceso al Excel entre hilos del mismo proceso.
   Workbook	      Crea libros de Excel.
   load_workbook	Abre libros de Excel existentes.
   os, datetime, uuid, pathlib y threading forman parte de la biblioteca estándar de Python. No requieren instalación independiente.

4. Configuración mediante el archivo .env
   El archivo .env contiene la configuración utilizada por la aplicación.
   Su contenido es:
   IP_LOCAL=111.111.1.20
   PORT=5000
   La dirección IP del ejemplo debe reemplazarse por la IPv4 real del computador en el que se ejecutará el proyecto.

   ¿Qué significa cada variable?
   IP_LOCAL. Representa la dirección IPv4 del computador servidor dentro de la red local. Permite construir la dirección que se utilizará para acceder al formulario desde otros dispositivos, como un celular.
   PORT. Define el puerto TCP que utilizará Flask para recibir las solicitudes.


5. Consideraciones técnicas y limitaciones
   - Conectividad: el computador servidor y el celular deben poder comunicarse por la red. Estar conectados al mismo Wi-Fi suele ser suficiente, pero algunas redes aíslan los dispositivos.
   - Dirección IP: si cambia la IPv4 del computador, se debe actualizar .env y regenerar el QR.
   - Firewall: Windows puede bloquear las conexiones entrantes. Se debe autorizar el acceso únicamente en redes de confianza y conforme a las políticas de seguridad aplicables.
   - Archivo Excel: resulta práctico para un prototipo o un volumen pequeño de registros, pero no ofrece las garantías de concurrencia y administración de una base de datos.
   - Bloqueo de Excel: si el archivo está abierto y bloqueado por otra aplicación, el guardado puede fallar.


6. Finalidad general
   El proyecto busca simplificar la toma de asistencia mediante la combinación de una aplicación web, un código QR y un archivo Excel.

   Su arquitectura integra conceptos importantes de desarrollo de software: configuración mediante variables de entorno, manejo de solicitudes HTTP, validación de formularios, generación de identificadores, gestión de archivos y automatización de tareas.

   Es una solución local que puede utilizarse como prototipo funcional y como base para futuras mejoras, como la incorporación de una base de datos, reportes, autenticación de usuarios o administración de eventos.


7. Paso a paso de la ejecución del código

   Se configura la dirección del computador donde funcionará el sistema.
   Se genera un código QR con la dirección del formulario.
   Se inicia la aplicación.
   El usuario escanea el código QR desde su celular.
   Se abre el formulario de asistencia.
   El usuario ingresa su nombre y apellido.
   El sistema valida la información.
   Si los datos son correctos, registra la asistencia en un archivo Excel.
   Se muestra una pantalla de confirmación con el identificador de la asistencia.


8. ¿Qué hace cada archivo del proyecto?

   .env — Configuración
      Guarda la dirección IP del computador y el puerto que utiliza la aplicación. Permite cambiar estos valores sin modificar el código Python.

   app.py — Funcionamiento principal
      Inicia el servidor, muestra el formulario, recibe los datos, valida la información, registra la asistencia en Excel y presenta la confirmación.

   generar_qr.py — Generación del QR
      Lee la configuración del archivo .env, crea el código QR con la dirección del formulario y guarda la imagen en la carpeta static.

   templates/asistencia.html — Formulario
      Es la página que permite al usuario ingresar su nombre y apellido.

   templates/confirmacion.html — Confirmación
      Presenta el resultado del registro y recibe desde Python el identificador de asistencia y el nombre de la persona.

   templates/qr.html — Página del QR
      Permite mostrar una página destinada al código QR. La plantilla debe tener configurada la referencia a la imagen para que esta aparezca.

   data/asistencias.xlsx — Almacenamiento
      Guarda los registros con el identificador, nombre, apellido, fecha y hora.

   static/codigo_qr.png — Imagen del QR
      Contiene el código QR que los usuarios pueden escanear para abrir el formulario.