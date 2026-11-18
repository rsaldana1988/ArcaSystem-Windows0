# ArcaSystem — Fase 1: estructura funcional

Esta entrega es una **base ejecutable**, no el sistema completo. Incluye login, estructura de menú, dashboard inicial, modelos de datos, administración Django y API de resumen. Los módulos avanzados (SMS reales, QR, 2FA, PWA, integraciones, reportes exportables, aprobaciones y auditoría automática) están pendientes.

## Inicio rápido Windows
1. Instala Python 3.12 o 3.13 y marca Add Python to PATH.
2. Extrae el ZIP y ejecuta `INICIAR_WINDOWS.bat` (instala dependencias y crea tablas).
3. En otra terminal dentro de la carpeta ejecuta `.venv\Scripts\python.exe manage.py createsuperuser`.
4. Abre `http://127.0.0.1:8000/admin/`, entra con el superusuario, crea una **Church** y después un **ChurchUser** que relacione tu usuario con la iglesia.
5. Abre `http://127.0.0.1:8000/` para ver el dashboard.

Por defecto se usa SQLite para probar inmediatamente. Para MySQL instala y configura un servidor, crea la base `arcasystem`, instala el driver compatible y define las variables DB_ENGINE=mysql, DB_NAME, DB_USER, DB_PASSWORD, DB_HOST y DB_PORT.

**Advertencia:** la configuración predeterminada es solo para desarrollo local. Antes de producción se requiere SECRET_KEY segura, DEBUG=0, HTTPS, políticas de acceso por iglesia en todas las vistas/admin, pruebas, backups, endurecimiento y revisión de seguridad. No subir datos reales sensibles ni exponer el servidor a Internet con esta configuración.
