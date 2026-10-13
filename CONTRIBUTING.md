# Contribución

## Flujo de trabajo

1. Comprobar `git status` y conservar los cambios pendientes antes de sincronizar.
2. Actualizar con `git pull --ff-only` antes de comenzar una sesión.
3. Mantener cada commit centrado en un cambio concreto.
4. Ejecutar las comprobaciones del proyecto antes de publicar.
5. Revisar `git diff --cached` y subir con `git push`.

## Mensajes de commit

Formato: `tipo(alcance): descripción`.

| Tipo | Uso | Ejemplo |
| --- | --- | --- |
| feat | Funcionalidad nueva | `feat(api): agregar consulta de aprendices` |
| fix | Corrección de errores | `fix(models): corregir validación del correo` |
| docs | Documentación | `docs: actualizar instrucciones de instalación` |
| test | Pruebas | `test(models): cubrir actualizaciones parciales` |
| refactor | Reorganización sin cambio funcional | `refactor(db): separar configuración` |
| chore | Mantenimiento | `chore: actualizar exclusiones de Git` |
| ci | Comprobaciones automáticas | `ci: ejecutar pruebas en GitHub` |

Los cambios incompatibles se indican con `!` y una explicación en el cuerpo del commit.

## Código y datos

- Cuatro espacios de sangría en Python y formato consistente con Ruff.
- Dependencias de ejecución en `requirements.txt`; herramientas de desarrollo en `requirements-dev.txt`.
- Variables privadas en `.env`; ejemplos sin contraseñas en `.env.example`.
- Pruebas automáticas con datos ficticios y conexiones simuladas.
- Las demostraciones que escriben en bases de datos se ejecutan manualmente y quedan fuera del descubrimiento de pruebas.
- No publicar entornos virtuales, cachés, credenciales ni datos personales.
- No reescribir commits publicados como práctica habitual entre computadores.
