# Online Conversion Tool

La herramienta de conversión de archivos expone un API para realizar conversiones entre diferentes formatos de video. El listado completo de métodos expuestos, así como su documentación se pueden encontrar en el siguiente link [Documentación API Postman](https://documenter.getpostman.com/view/29467035/2s9YRCVAme).

## Componentes

La herramienta de conversión está compuesta por 4 componentes principales:

### Base de datos postgres
Este componente es fundamental para la persistencia de los datos de la aplicación. La base de datos Postgres almacena toda la información necesaria para el funcionamiento de la herramienta.

### Redis
Redis es un componente esencial que respalda la funcionalidad de la cola de tareas o actúa como un bróker para Celery.

### Online Conversion Tool
Esta aplicación, desarrollada en Flask Python, expone una API Rest que se utiliza para llevar a cabo las funciones de autenticación, registro y administración de las tareas de conversión. Es la interfaz principal a través de la cual los usuarios interactúan con la herramienta de conversión.

### Async Video Processor
Esta aplicación de consola Python juega un papel crucial en la infraestructura. Escucha una cola de tareas de Celery y se encarga de llevar a cabo la conversión de codificación de los videos de manera asincrónica. Garantiza que las tareas se procesen en segundo plano, sin afectar la experiencia del usuario.

## ¿Cómo instalar y ejecutar la aplicación?

### Requisitos

* Tener instalado una instancia de Docker en su máquina, Si aún no lo tiene instalado puede acceder al siguiente recurso [Instalación de Docker](https://jpadillaa.hashnode.dev/docker-instalacion-de-docker)
* Tener disponibles los puertos 8000, 6379 y 15432 para ejecutar la apliación, puede personalizar esos puertos en el archivo `docker-compose.yaml`

### Pasos para la instalación

1. Si aún no está familiarizado con los comandos de Docker, puede consultar [Comandos Básicos Docker](https://jpadillaa.hashnode.dev/docker-comandos-basicos-de-docker) para obtener más información. Descargue o clone este repositorio y ejecute el siguiente comando para construir la imagen Docker para **Online Conversion Tool**:

```
docker build -t online-conversion-tool .
```

_Imagen 1: Resultado de la generación de la imagen Docker online-conversion-tool_

Después de ejecutar este comando, debería obtener un resultado similar al que se muestra en la Imagen 1.

2. Descargue y clone el siguiente repositorio: [AsyncVideoProcessor](https://github.com/MISW-4204-2023/AsyncVideoProcessor). Luego, ejecute el siguiente comando para crear la imagen Docker para **Async Video Processor**

```
docker build -t async-video-processor .
```

_Imagen 2: Resultado de la ejecución del comando que genera la imagen docker async-video-processor_

3. Utilizar Docker Compose para crear los pods de aplicación. Descargue o clone este repositorio y asegúrese de haber completado los dos primeros pasos. Luego, ejecute el siguiente comando para utilizar Docker Compose y crear los pods que ejecutarán la aplicación:

```
docker-compose up -d
```

_Imagen 3: Resultado de la ejecución del docker compose_

_Imagen 4: Imagen de la herramienta de docker con los pods corriendo_

**Nota:** En algunos casos, es posible que la imagen de Online Conversion Tool genere un error en la primera ejecución debido a que no encuentra la base de datos. En ese caso, simplemente vuelva a levantar Docker Compose con el comando anterior. Si todo se ha realizado correctamente, podrá acceder a los servicios a través del puerto 8000 o el puerto que haya configurado en el archivo docker-compose.yaml.