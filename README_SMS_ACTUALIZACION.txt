ARCA SYSTEM - ACTUALIZACIÓN SMS

Se conserva la base de datos recibida y los módulos existentes.
Nuevo módulo SMS: campañas, destinatarios, plantillas, exclusiones e indicadores.
No envía SMS reales ni confirma entregas. Para ello hace falta integrar un proveedor y configurar credenciales, consentimiento, costos, webhooks y tareas programadas.
Inicio habitual: INICIAR_ARCASYSTEM.bat. El iniciador debe aplicar las migraciones Django.
Antes de actualizar, haz una copia externa de db.sqlite3 y media.
La carpeta .venv se ha omitido del ZIP por ser regenerable y específica de Windows.
