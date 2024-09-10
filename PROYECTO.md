# Sistema de ligas de equipos de Voley

La idea del presente proyecto se basa en el surgimiento de ligas de voley de equipos más pequeños
a los habituales en la región, donde muchos chicos y chicas concurren, y buscan mejorar sus
habilidades en el deporte y llegar a un lugar en las ligas mayores del mismo. Así como visibilizar
estos clubes menores para que tengan una mayor llegada a la población local y fomentar su
práctica

## Descripción del proyecto

El proyecto consiste en una aplicación web orientada a ligas de Voley que permita no solo
cargar los partidos de las temporada si no, cargar estadísticas de jugadores y de equipos.
Se crearán 3 tipos de usuarios: Directores Técnicos, Asistentes (estos
últimos encargados de actualizar entre otras cosas, las estadísticas de los Jugadores) y
Jugadores.
Los Asistentes se encargarán de dar de alta los equipos, los perfiles de los técnicos y
actualizar los cambios de todos los usuarios entre los equipos en una temporada de una
liga. Una Liga consiste de un torneo (puede ser dividido por categoría o edad de jugadores)
que tiene distintas temporadas generalmente dividida por el año en que transcurre (por
ejemplo: temporada 2018, 2019, etc).
Tanto los Asistentes como los Directores Técnicos se encargarán de los resultados de los partidos que se podrán ver en
una página donde se calcularán las posiciones cada vez que estos sean cargados.
Los Usuarios Asistentes podrán cargar los equipos puestos en cancha en los sets de cada
partido y los cambios hechos. Al mismo tiempo, podrán agregar
estadísticas de los jugadores como por ejemplo: cantidad de remates fallidos y completos,
remates cruzados o derechos, defensas, bloqueos, saques, etc. Esto permitirá mostrar los
puntos fuertes del jugador, así como también los puntos a mejorar o hacia qué tipo de juego
tiende (ofensivo o defensivo).

## Modelo de Dominio

![MD-TPI-Soporte.jpg](images%2FMD-TPI-Soporte.jpg)

## Bosquejo de Arquitectura

![MD-TPI-Soporte-Página-2.jpg](images%2FMD-TPI-Soporte-P%E1gina-2.jpg)

## Requerimientos

### Funcionales

- El Usuario podrá cargar las estadísticas de los jugadores.
- El Administrador podrá cargar los resultados de los partidos.
- El Sistema calculará los porcentajes de las habilidades de los jugadores.
- El Sistema calculará las posiciones de los equipos según los puntajes cargados.
- El Usuario podrá ver las estadísticas de los jugadores.
- El Usuario podrá cambiar de equipo en caso de ser necesario.
- El Usuario podrá ver las estadísticas del equipo según los partidos jugados.

### No Funcionales

- La cuenta de un usuario contará con una opción de recuperación de usuario basado en el envío de mail a su correo principal.
- La cuenta de Usuario deberá contar con una contraseña con más de 8 caracteres y debe tener al menos un valor alfanumérico.
- El sistema debe funcionar para al menos 200 personas al mismo tiempo.

### Portability

**Obligatorios**

- El sistema debe funcionar correctamente en múltiples navegadores (Sólo Web).
- El sistema debe ejecutarse desde un único archivo .py llamado app.py (Sólo Escritorio).

### Security

**Obligatorios**

- Todas las contraseñas deben guardarse con encriptado criptográfico (SHA o equivalente).
- Todas los Tokens / API Keys o similares no deben exponerse de manera pública.

### Maintainability

**Obligatorios**

- El sistema debe diseñarse con la arquitectura en 3 capas. (Ver [checklist_capas.md](checklist_capas.md))
- El sistema debe utilizar control de versiones mediante GIT.
- El sistema debe estar programado en Python 3.8 o superior.

### Reliability

### Scalability

**Obligatorios**

- El sistema debe funcionar desde una ventana normal y una de incógnito de manera independiente (Sólo Web).
  - Aclaración: No se debe guardar el usuario en una variable local, deben usarse Tokens, Cookies o similares.

### Performance

**Obligatorios**

- El sistema debe funcionar en un equipo hogareño estándar.

### Reusability

### Flexibility

**Obligatorios**

- El sistema debe utilizar una base de datos SQL o NoSQL

## Stack Tecnológico

Definir que tecnologías se van a utilizar en cada capa y una breve descripción sobre por qué se escogió esa tecnologia.

### Capa de Datos

Definir que base de datos, ORM y tecnologías se utilizaron y por qué.

### Capa de Negocio

Definir que librerías e integraciones con terceros se utilizaron y por qué. En caso de consumir APIs, definir cúales se usaron.

### Capa de Presentación

Definir que framework se utilizó y por qué.
