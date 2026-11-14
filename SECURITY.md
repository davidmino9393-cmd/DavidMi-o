# Seguridad y privacidad de la publicación

## Qué se publica

Una demo simplificada con datos inventados y ejecución manual. No se publica el workflow de una empresa, una copia de su base de datos ni su historial de cambios. El código de la muestra se preparó de forma independiente y no configura servicios reales.

## Qué debe quedar fuera

- Credenciales, claves API, tokens de acceso, contraseñas y claves privadas.
- Archivos de configuración de servicios, archivos de entorno y archivos de secretos.
- Clientes, contactos, teléfonos, correos, facturas, comprobantes e historiales reales.
- IDs y enlaces de hojas de cálculo, cuentas, instancias, webhooks y servicios internos.
- Exportaciones de credenciales, respaldos, volcados SQL, ejecuciones guardadas y logs.
- Capturas con nombres de cuentas, barras de direcciones, datos de clientes o credenciales visibles.
- El historial Git del proyecto operativo y reportes privados de revisión.

Las exportaciones de n8n pueden incluir nombres y referencias de credenciales. Algunos parámetros pueden contener encabezados de autenticación. Que un archivo sea JSON no lo vuelve apto para publicar.

Referencia: [ayuda oficial de n8n sobre exportaciones](https://support.n8n.io/article/migrating-from-cloud-to-self-hosted).

## Antes de subir o actualizar

1. Trabajar exclusivamente con la carpeta de esta demo.
2. Ejecutar las pruebas y `node tools/verify-publication.mjs`.
3. Revisar también de manera manual el contenido y la lista de archivos que se va a subir.
4. Usar un repositorio o una rama de portfolio separados del sistema de cobranzas. No importar sus archivos ni sus commits.
5. Añadir únicamente los archivos revisados; no forzar archivos ignorados.
6. Revisar el diff antes del commit y el historial antes del primer push.
7. Activar autenticación de dos factores o passkeys en GitHub y conceder a las herramientas el mínimo acceso necesario.
8. Revisar la visibilidad del correo de los commits y usar el correo privado de GitHub si se quiere preservar el correo personal.
9. Mantener los controles de detección de secretos y protección de subidas cuando estén disponibles.
10. Revisar también los textos y capturas que se publiquen en LinkedIn o en issues.

El archivo `.gitignore` limita las inclusiones normales, pero no borra archivos ya registrados, no bloquea un añadido forzado y no reemplaza una revisión.

## Si una clave se publica por accidente

Revocar o rotar la credencial en el servicio correspondiente. Borrar el archivo del último commit no invalida una clave y puede dejarla accesible en commits anteriores, clones o copias. Después, revisar el alcance de la exposición y la limpieza del historial según la documentación oficial.

- [GitHub: quitar datos sensibles de un repositorio](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- [GitHub: detección de secretos](https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning)
- [GitHub: configurar autenticación de dos factores](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication)

## Límites de esta revisión

Los controles locales buscan patrones conocidos y verifican la estructura de esta demo. No son una auditoría del servidor de n8n, de las cuentas conectadas, de sus permisos ni de su infraestructura. La copia operativa no se ejecuta ni se modifica como parte de esta preparación.

El workflow público no tiene Schedule, Webhook ni conexiones externas. Su clasificación, sus bloqueos y sus vistas previas se comprueban en Node.js. La importación y ejecución dentro de una instancia de n8n no se presentan como verificadas.

Al reportar un problema, no publicar claves, contactos ni ejemplos tomados de una empresa real.
