import QtQuick
import QtQuick.Layouts

Rectangle {
    anchors.fill: parent
    color: "#301827"
    readonly property string basePath: "../../../"

    FontLoader {
        id: byteBounce
        source: basePath + "Resources/fonts/ByteBounce.ttf"
    }

    Image {
        id: homeIcon
        source: basePath + "Resources/sprites/home/png/home.png"
        width: 32
        height: 32
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.topMargin: 15
        anchors.leftMargin: 15
        scale: homeArea.containsMouse ? 1.2 : 1.0

        Behavior on scale {
            NumberAnimation { duration: 150; easing.type: Easing.OutQuad }
        }

        MouseArea {
            id: homeArea
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            onClicked: loginHandler.goHome()
        }
    }

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 20
        width: parent.width * 0.8

        Image {
            source: basePath + "Resources/sprites/author/author.png"
            fillMode: Image.PreserveAspectFit
            scale: 0.7
            Layout.alignment: Qt.AlignHCenter
        }

        Text {
            text: "About"
            color: "white"
            font.family: byteBounce.name
            font.pixelSize: 48
            Layout.alignment: Qt.AlignHCenter
        }

        Text {
            text: "Created by a perennial fantasy sports consolation bracket winner and software engineer. " +
                  "I figured if I was going to lose my fantasy matchups every week I might as well make it look cool."
            color: "#c0a0b0"
            font.family: byteBounce.name
            font.pixelSize: 24
            wrapMode: Text.WordWrap
            horizontalAlignment: Text.AlignHCenter
            Layout.alignment: Qt.AlignHCenter
            Layout.fillWidth: true
        }

        Text {
            text: "Version 0.1.0"
            color: "#907080"
            font.family: byteBounce.name
            font.pixelSize: 20
            Layout.alignment: Qt.AlignHCenter
        }

        RowLayout {
            Layout.alignment: Qt.AlignHCenter
            spacing: 20

            Image {
                id: githubIcon
                source: basePath + "Resources/sprites/github/github.png"
                sourceSize.width: 36
                sourceSize.height: 36
                scale: githubArea.containsMouse ? 1.2 : 1.0

                Behavior on scale {
                    NumberAnimation { duration: 150; easing.type: Easing.OutQuad }
                }

                MouseArea {
                    id: githubArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: Qt.openUrlExternally("https://github.com/RyanDBurke")
                }
            }

            Image {
                id: websiteIcon
                source: basePath + "Resources/sprites/website/website.png"
                sourceSize.width: 36
                sourceSize.height: 36
                scale: websiteArea.containsMouse ? 1.2 : 1.0

                Behavior on scale {
                    NumberAnimation { duration: 150; easing.type: Easing.OutQuad }
                }

                MouseArea {
                    id: websiteArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: Qt.openUrlExternally("https://ryandburke.github.io/")
                }
            }
        }
    }
}
