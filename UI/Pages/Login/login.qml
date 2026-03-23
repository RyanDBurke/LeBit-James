import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    anchors.fill: parent
    color: "#301827"

    FontLoader {
        id: byteBounce
        source: "../../../Resources/fonts/ByteBounce.ttf"
    }

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 20
        visible: !loginHandler.loading

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
            Keys.onReturnPressed: loginHandler.submit(usernameField.text)
        }

        Text {
            text: loginHandler.errorMessage
            color: "#ff4444"
            font.family: byteBounce.name
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
            visible: loginHandler.errorMessage !== ""
        }
    }

    Image {
        id: loadingSpinner
        source: "../../../Resources/sprites/basketball/png/bball.png"
        fillMode: Image.PreserveAspectFit
        anchors.centerIn: parent
        visible: loginHandler.loading

        RotationAnimation on rotation {
            loops: Animation.Infinite
            from: 0
            to: 360
            duration: 2000
            running: loginHandler.loading
        }
    }
}