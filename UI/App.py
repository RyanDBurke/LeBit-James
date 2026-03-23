import os
import sys
import threading

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtCore import QMetaObject, Qt

from UI.Pages.Login.login import Login


class App:
    @staticmethod
    def start(on_username=None):
        os.environ["QT_QUICK_CONTROLS_STYLE"] = "Basic"
        app = QGuiApplication(sys.argv)

        engine = QQmlApplicationEngine()
        engine.quit.connect(app.quit)

        # Set up login handler before loading QML so context property is available
        login = Login(engine)

        def handle_username(username):
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
                    QMetaObject.invokeMethod(login, "onLoginFailed", Qt.ConnectionType.QueuedConnection)

            threading.Thread(target=fetch, daemon=True).start()

        login.usernameSubmitted.connect(handle_username)

        engine.load('UI/Pages/Welcome/welcome.qml')
        if not engine.rootObjects():
            sys.exit(-1)

        sys.exit(app.exec())
