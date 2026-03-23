import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    anchors.fill: parent
    color: "#301827"

    FontLoader {
        id: byteBounce
        source: "../../../Resources/fonts/ByteBounce.ttf"
    }

    ListModel {
        id: cachedUsernamesModel
    }

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 20
        visible: loginHandler ? !loginHandler.loading : true

        Image {
            source: "../../../Resources/sprites/lebit/png/lebit-300px.png"
            fillMode: Image.PreserveAspectFit
            Layout.alignment: Qt.AlignHCenter
        }

        TextField {
            id: usernameField
            placeholderText: "Enter username"
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: 500
            color: "white"
            font.family: byteBounce.name
            font.pixelSize: 32
            horizontalAlignment: Text.AlignHCenter
            background: Rectangle {
                color: "#4a2a3d"
                radius: 5
                border.color: "#7a4a6d"
                border.width: 1
            }
            Keys.onReturnPressed: if (loginHandler) loginHandler.submit(usernameField.text)
        }

        // Cached Usernames ListView
        Rectangle {
            Layout.alignment: Qt.AlignHCenter
            Layout.preferredWidth: 500
            Layout.preferredHeight: Math.min(cachedUsernamesModel.count * 45, 200)
            visible: cachedUsernamesModel.count > 0
            color: "#3a1a2d"
            radius: 5
            border.color: "#7a4a6d"
            border.width: 1

            ListView {
                anchors.fill: parent
                anchors.margins: 5
                model: cachedUsernamesModel
                clip: true
                spacing: 5

                delegate: Rectangle {
                    width: parent.width - 10
                    height: 40
                    color: mouseArea.containsMouse ? "#5a3a4d" : "#4a2a3d"
                    radius: 3
                    border.color: "#6a4a5d"
                    border.width: 1

                    MouseArea {
                        id: mouseArea
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: {
                            usernameField.text = model.username
                            usernameField.focus = true
                        }
                    }

                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 8
                        spacing: 10

                        Text {
                            text: model.username
                            color: "white"
                            font.family: byteBounce.name
                            font.pixelSize: 16
                            Layout.fillWidth: true
                        }

                        Image {
                            source: "../../../Resources/sprites/garbage/garbage.png"
                            Layout.preferredWidth: 24
                            Layout.preferredHeight: 24
                            fillMode: Image.PreserveAspectFit
                            opacity: deleteIconMouse.containsMouse ? 1.0 : 0.7

                            MouseArea {
                                id: deleteIconMouse
                                anchors.fill: parent
                                hoverEnabled: true
                                cursorShape: Qt.PointingHandCursor
                                onClicked: {
                                    if (loginHandler) {
                                        loginHandler.removeCachedUsername(model.username)
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

        Text {
            text: loginHandler ? loginHandler.errorMessage : ""
            color: "#ff4444"
            font.family: byteBounce.name
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
            visible: loginHandler ? loginHandler.errorMessage !== "" : false
        }
    }

    Image {
        id: loadingSpinner
        source: "../../../Resources/sprites/basketball/png/bball.png"
        fillMode: Image.PreserveAspectFit
        anchors.centerIn: parent
        visible: loginHandler ? loginHandler.loading : false

        RotationAnimation {
            target: loadingSpinner
            property: "rotation"
            loops: Animation.Infinite
            from: 0
            to: 360
            duration: 2000
            running: loginHandler ? loginHandler.loading : false
        }
    }

    Connections {
        target: loginHandler
        function onErrorMessageChanged() {
            if (loginHandler && loginHandler.errorMessage !== "") {
                usernameField.selectAll()
            }
        }
        function onCachedUsernamesChanged(usernames) {
            cachedUsernamesModel.clear()
            for (let i = 0; i < usernames.length; i++) {
                cachedUsernamesModel.append({ username: usernames[i] })
            }
        }
    }

    Component.onCompleted: {
        if (loginHandler) {
            let usernames = loginHandler.getCachedUsernames()
            for (let i = 0; i < usernames.length; i++) {
                cachedUsernamesModel.append({ username: usernames[i] })
            }
        }
    }
}