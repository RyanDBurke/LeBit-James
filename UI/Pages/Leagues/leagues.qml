import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    anchors.fill: parent
    color: "#301827"
    property var user: null // Set this property from your navigation logic
    readonly property string basePath: "../../../"

    FontLoader {
        id: byteBounce
        source: basePath + "Resources/fonts/ByteBounce.ttf"
    }

    MouseArea {
        anchors.fill: parent
        onClicked: logoutButton.visible = false
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
            onClicked: leaguesHandler.goHome()
        }
    }

    Image {
        id: cogIcon
        source: basePath + "Resources/sprites/settings/png/cog.png"
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

        onClicked: leaguesHandler.logout()
    }

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 20

        Text {
            text: "Your Leagues"
            font.pixelSize: 28
            color: "#fff"
            font.bold: true
            horizontalAlignment: Text.AlignHCenter
            Layout.alignment: Qt.AlignHCenter
        }

        ListView {
            id: leagueList
            width: 400
            height: 300
            model: user && user.leagues ? user.leagues : []
            delegate: Rectangle {
                width: parent.width
                height: 40
                color: index % 2 === 0 ? "#3a2040" : "#4a2a3d"
                radius: 5
                border.color: "#7a4a6d"
                border.width: 1
                RowLayout {
                    anchors.fill: parent
                    spacing: 10
                    Text {
                        text: modelData.name
                        color: "#fff"
                        font.pixelSize: 20
                        Layout.alignment: Qt.AlignVCenter
                    }
                }
            }
            clip: true
        }
    }
}
