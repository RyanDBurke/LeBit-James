import QtQuick
import QtQuick.Controls

ApplicationWindow {
    visible: true
    width: 800
    height: 800
    minimumWidth: 400
    minimumHeight: 400
    title: "LeBit James"
    readonly property string basePath: "../../../"
    //flags: Qt.FramelessWindowHint | Qt.Window

    FontLoader {
        id: byteBounce
        source: basePath + "Resources/fonts/ByteBounce.ttf"
    }

    Rectangle {
        id: welcomeContent
        anchors.fill: parent
        color: "#301827"
        visible: true

        Image {
            source: basePath + "Resources/sprites/lebit/png/lebit-300px.png"
            fillMode: Image.PreserveAspectFit
            anchors.centerIn: parent
        }

        Text {
            text: "click anywhere to continue"
            color: "white"
            font.family: byteBounce.name
            font.pixelSize: 20
            font.italic: true
            anchors.horizontalCenter: parent.horizontalCenter
            y: parent.height * 0.66

            SequentialAnimation on opacity {
                loops: Animation.Infinite
                NumberAnimation { to: 0; duration: 800 }
                NumberAnimation { to: 1; duration: 800 }
            }
        }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                welcomeContent.visible = false
                loginLoader.active = true
            }
        }
    }

    Loader {
        id: loginLoader
        anchors.fill: parent
        active: !welcomeContent.visible && !(loginHandler && loginHandler.loginSuccess)
        source: "../Login/login.qml"
    }

    Loader {
        id: homeLoader
        anchors.fill: parent
        active: loginHandler ? loginHandler.loginSuccess : false
        source: navigator ? navigator.currentPage : ""
    }
}