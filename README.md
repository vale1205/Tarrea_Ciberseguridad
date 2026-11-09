# Sistema Alumnos

Actividad 3.4.2 de Valentina Saavedra, OCY1102.
API Flask con documentación Doxygen y pipeline Jenkins de cinco etapas:
Build, Test, Generate Documentation, Version Control y Deploy.

## Ejecución y pruebas

```bash
pipenv sync --dev
pipenv run pytest
pipenv run python app.py
```

Las 17 pruebas verifican salud, versión, consultas, creación y validación.
La app usa almacenamiento en memoria y servidor de desarrollo, solo para pruebas.

## Documentación

```bash
mkdir -p reports
APP_VERSION=local doxygen Doxyfile
```

Abrir docs/html/index.html y revisar reports/doxygen_warnings.log.
Jenkins marca UNSTABLE si el registro contiene advertencias, y omite el versionado
y despliegue. Los avisos FAILURE y UNSTABLE aparecen en la consola. No hay correo
o webhook externo configurado.

## Jenkins y GitHub

Configurar Pipeline script from SCM, Git, rama main y Jenkinsfile.
Repositorio: https://github.com/vale1205/Tarrea_Ciberseguridad.git
Guardar usuario y token restringido a este repositorio en la credencial
github-token de Jenkins. Se necesita Contents Read and write. El script utiliza
GIT_ASKPASS; nunca guardar tokens en Git. El pipeline también admite un remoto
local bajo /repos/, utilizado en las evidencias sin credenciales externas.

Pipfile.lock fija versiones y hashes. Se conservaron las dependencias educativas
antiguas de la actividad. No se ejecutó pip-audit ni se afirma que el proyecto
esté libre de vulnerabilidades.

## Trazabilidad

- Fuente del build verificado: de490ee.
- Jenkins: build 1, SUCCESS, 17/17 pruebas, 0 advertencias Doxygen.
- Commit documental: e0116bb.
- Etiqueta anotada: build-1-de490ee.
- Registro: docs/TRAZABILIDAD.md.

La etiqueta apunta al commit documental y el registro conserva el commit fuente.
El README se amplió después del build sin modificar el código ejecutado.
Antes de editar, ejecutar git pull --tags. Si se añade un webhook, configurar la
exclusión de commits con [skip ci] para evitar un ciclo de builds.

## Rutas

| Método | Ruta | Resultado |
|---|---|---|
| GET | /hello?name=Ana | Saludo |
| GET | /health | Estado del proceso |
| GET | /version | Versión del build |
| GET | /alumnos | Lista de alumnos |
| GET | /alumnos/1 | Alumno o error 404 |
| POST | /alumnos | Crea alumno o error 400 |

Para crear, enviar JSON con nombre no vacío y promedio numérico entre 1 y 7.
Carrera es opcional. No se aceptan booleanos como promedio.
