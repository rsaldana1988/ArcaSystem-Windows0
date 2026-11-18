"""ArcaSystem: escritorio Windows, servidor local privado y ventana PyWebView."""
import os
import sys
import pathlib
import threading
import socket
import traceback
import logging
import time

# PyInstaller --windowed establece stdout/stderr a None.
if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w', encoding='utf-8')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w', encoding='utf-8')

ROOT = pathlib.Path(sys.executable if getattr(sys, 'frozen', False) else __file__).resolve().parent
LOG_FILE = ROOT / 'ArcaSystem_inicio_error.log'


def log_error(exc):
    with LOG_FILE.open('a', encoding='utf-8') as f:
        f.write('\n' + time.strftime('%Y-%m-%d %H:%M:%S') + '\n')
        traceback.print_exception(type(exc), exc, exc.__traceback__, file=f)


def show_error(message):
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(None, message, 'ArcaSystem - Error al iniciar', 0x10)
    except Exception:
        pass


def local_wsgi(app, root):
    from urllib.parse import unquote
    from wsgiref.util import FileWrapper
    from whitenoise import WhiteNoise
    wrapped = WhiteNoise(app, root=str(root / 'staticfiles'))
    wrapped.add_files(str(root / 'static'), prefix='static/')
    def handler(environ, start_response):
        path = unquote(environ.get('PATH_INFO', ''))
        if path.startswith('/media/'):
            media_root = (root / 'media').resolve()
            target = (media_root / path[len('/media/'):]).resolve()
            if not target.is_relative_to(media_root) or not target.is_file():
                start_response('404 Not Found', [('Content-Type', 'text/plain')])
                return [b'Not Found']
            import mimetypes
            start_response('200 OK', [('Content-Type', mimetypes.guess_type(str(target))[0] or 'application/octet-stream')])
            return FileWrapper(open(target, 'rb'))
        return wrapped(environ, start_response)
    return handler


def main():
    os.chdir(ROOT)
    sys.path.insert(0, str(ROOT))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arcasystem.settings')
    os.environ.setdefault('DJANGO_DEBUG', '0')
    from django.core.management import execute_from_command_line
    from django.core.wsgi import get_wsgi_application
    from waitress import create_server
    import webview

    execute_from_command_line(['manage.py', 'migrate', '--noinput', '--verbosity', '0'])
    try:
        execute_from_command_line(['manage.py', 'import_arcasystem_logo', '--verbosity', '0'])
    except Exception as exc:
        log_error(exc)
    application = local_wsgi(get_wsgi_application(), ROOT)

    # Seleccionar un puerto libre en loopback; no exponer la aplicación a la red.
    server = create_server(application, host='127.0.0.1', port=0, threads=6)
    port = server.effective_port
    thread = threading.Thread(target=server.run, daemon=True, name='ArcaSystemLocalServer')
    thread.start()
    if not thread.is_alive():
        raise RuntimeError('No fue posible iniciar el servidor local.')
    icon = ROOT / 'ArcaSystem.ico'
    window = webview.create_window('ArcaSystem | Puerto de Salvación', f'http://127.0.0.1:{port}/', width=1280, height=800, min_size=(950, 600))
    try:
        webview.start(gui='edgechromium', debug=False)
    finally:
        server.close()


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        log_error(exc)
        show_error('No se pudo iniciar ArcaSystem.\n\n' + str(exc) + '\n\nDetalles: ' + str(LOG_FILE))
        sys.exit(1)
