import logging
import os
import pathlib
import sys
import threading
from typing import Any, Callable

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtCore import QMetaObject, Qt

from UI.Pages.Login.login import Login

logger = logging.getLogger(__name__)


class App:
    @staticmethod
    def start(on_username: Callable[[str], Any] | None = None) -> None:
        """Start the application. This method never returns; it calls sys.exit."""
        os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"
        app = QGuiApplication(sys.argv)

        engine = QQmlApplicationEngine()
        engine.quit.connect(app.quit)

        # Set up login handler before loading QML so context property is available
        login = Login(engine)

        def handle_username(username):
            # on_username runs on a background thread so it can't touch Qt objects or shared mutable state.
            # or else we get annoying race conditions
            def fetch():
                try:
                    result = None
                    if on_username:
                        result = on_username(username)
                    if result is not None:
                        QMetaObject.invokeMethod(login, "onLoginSuccess", Qt.ConnectionType.QueuedConnection)
                    else:
                        QMetaObject.invokeMethod(login, "onLoginFailed", Qt.ConnectionType.QueuedConnection)
                except Exception:
                    logger.exception("Login fetch failed")
                    QMetaObject.invokeMethod(login, "onLoginFailed", Qt.ConnectionType.QueuedConnection)

            threading.Thread(target=fetch, daemon=True).start()

        login.usernameSubmitted.connect(handle_username)

        qml_path = pathlib.Path(__file__).parent / "Pages/Welcome/welcome.qml"
        engine.load(str(qml_path))
        if not engine.rootObjects():
            sys.exit(-1)

        sys.exit(app.exec())
