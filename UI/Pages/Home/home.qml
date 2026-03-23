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

    MouseArea {
        anchors.fill: parent
        onClicked: logoutButton.visible = false
    }

    Image {
        id: homeIcon
        source: "../../../Resources/sprites/home/png/home.png"
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

    Image {
        id: aboutIcon
        source: "../../../Resources/sprites/about/png/about.png"
        width: 32
        height: 32
        anchors.top: parent.top
        anchors.right: cogIcon.left
        anchors.topMargin: 15
        anchors.rightMargin: 10
        scale: aboutArea.containsMouse ? 1.2 : 1.0

        Behavior on scale {
            NumberAnimation { duration: 150; easing.type: Easing.OutQuad }
        }

        MouseArea {
            id: aboutArea
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            onClicked: loginHandler.goAbout()
        }
    }

    Image {
        id: cogIcon
        source: "../../../Resources/sprites/settings/png/cog.png"
        width: 32
        height: 32
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.topMargin: 15
        anchors.rightMargin: 15
        scale: cogArea.containsMouse ? 1.2 : 1.0

        Behavior on scale {
            NumberAnimation { duration: 150; easing.type: Easing.OutQuad }
        }

        MouseArea {
            id: cogArea
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            onClicked: logoutButton.visible = !logoutButton.visible
        }
    }

    Button {
        id: logoutButton
        visible: false
        anchors.top: cogIcon.bottom
        anchors.right: cogIcon.right
        anchors.topMargin: 5

        contentItem: Text {
            text: "Log Out"
            color: "#ff4444"
            font.family: byteBounce.name
            font.pixelSize: 18
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        background: Rectangle {
            color: logoutButton.pressed ? "#5a3a4d" : "#4a2a3d"
            radius: 5
            border.color: "#7a4a6d"
            border.width: 1
        }

        onClicked: loginHandler.logout()
    }

    RowLayout {
        anchors.centerIn: parent
        spacing: 40

        Image {
            id: basketballCard
            source: "../../../Resources/sprites/basketball-card/png/basketball-card-300px.png"
            fillMode: Image.PreserveAspectFit
            scale: basketballArea.containsMouse ? 1.1 : 1.0

            Behavior on scale {
                NumberAnimation { duration: 200; easing.type: Easing.OutQuad }
            }

            MouseArea {
                id: basketballArea
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                propagateComposedEvents: true
                onClicked: function(mouse) { mouse.accepted = false }
            }
        }

        Image {
            id: footballCard
            source: "../../../Resources/sprites/football-card/png/football-card-300px.png"
            fillMode: Image.PreserveAspectFit
            scale: footballArea.containsMouse ? 1.1 : 1.0

            Behavior on scale {
                NumberAnimation { duration: 200; easing.type: Easing.OutQuad }
            }

            MouseArea {
                id: footballArea
                anchors.fill: parent
                hoverEnabled: true
                cursorShape: Qt.PointingHandCursor
                propagateComposedEvents: true
                onClicked: function(mouse) { mouse.accepted = false }
            }
        }
    }
}
