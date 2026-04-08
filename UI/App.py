import ctypes
import logging
import os
import pathlib
import sys
import threading
from typing import Any, Callable

from PyQt6.QtGui import QGuiApplication, QIcon, QPixmap
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtCore import QMetaObject, Qt

from UI.Pages.Login.login import Login

logger = logging.getLogger(__name__)

LOGIN_SUCCESS = "onLoginSuccess"
LOGIN_FAILED = "onLoginFailed"

# Tell Windows this is its own app so the taskbar uses our icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("lebitjames.app")

class App:
    @staticmethod
    def start(on_username: Callable[[str], Any] | None = None) -> None:
        """Start the application. This method never returns; it calls sys.exit."""
        os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"
        app = QGuiApplication(sys.argv)

        # set application icon
        icon_path = str(pathlib.Path(__file__).parent.parent / "Resources/sprites/basketball/png/bball-1500px.png")
        pixmap = QPixmap(icon_path)
        pixmap = pixmap.scaled(pixmap.width() * 2, pixmap.height() * 2, transformMode=Qt.TransformationMode.SmoothTransformation)
        app.setWindowIcon(QIcon(pixmap))

        engine = QQmlApplicationEngine()
        engine.quit.connect(app.quit)

        # Set up handlers before loading QML so context properties are available
        login = Login(engine)

        def process_login(username):
            """
            on_username runs on a background thread so it can't touch Qt objects or shared mutable state or else
            we get nasty race conditions
            """
            def fetch():
                try:
                    result = None
                    if on_username:
                        result = on_username(username)
                    if result is not None:
                        QMetaObject.invokeMethod(login, LOGIN_SUCCESS, Qt.ConnectionType.QueuedConnection)
                    else:
                        QMetaObject.invokeMethod(login, LOGIN_FAILED, Qt.ConnectionType.QueuedConnection)
                except Exception:
                    logger.exception("Login fetch failed")
                    QMetaObject.invokeMethod(login, LOGIN_FAILED, Qt.ConnectionType.QueuedConnection)

            threading.Thread(target=fetch, daemon=True).start()

        login.usernameSubmitted.connect(process_login)

        qml_path = pathlib.Path(__file__).parent / "Pages/Welcome/welcome.qml"
        engine.load(str(qml_path))
        if not engine.rootObjects():
            sys.exit(-1)

        sys.exit(app.exec())
