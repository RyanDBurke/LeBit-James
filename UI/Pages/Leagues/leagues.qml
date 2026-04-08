import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    anchors.fill: parent
    color: "#301827"
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
/*
        Text {
            text: leaguesHandler.userRepr
            font.pixelSize: 14
            color: "#fff"
            wrapMode: Text.Wrap
            Layout.maximumWidth: 700
            horizontalAlignment: Text.AlignHCenter
            Layout.alignment: Qt.AlignHCenter
        }*/

        RowLayout {
            Layout.fillWidth: true
            Layout.preferredWidth: 400

            Text {
                visible: leaguesHandler ? leaguesHandler.leagues.length > 0 : false
                text: "Leagues"
                color: "#fff"
                font.family: byteBounce.name
                font.pixelSize: 32
                Layout.fillWidth: true
            }

            Image {
                id: refreshIcon
                source: basePath + "Resources/sprites/refresh-leagues/refresh.png"
                sourceSize.width: 32
                sourceSize.height: 32
                Layout.preferredWidth: 32
                Layout.preferredHeight: 32
                Layout.alignment: Qt.AlignVCenter
                opacity: (leaguesHandler && leaguesHandler.refreshCooldown) ? 0.3 : 1.0
                scale: refreshArea.containsMouse && !(leaguesHandler && leaguesHandler.refreshCooldown) ? 1.2 : 1.0

                Behavior on scale {
                    NumberAnimation { duration: 150; easing.type: Easing.OutQuad }
                }

                Behavior on opacity {
                    NumberAnimation { duration: 300 }
                }

                RotationAnimation on rotation {
                    id: spinAnimation
                    from: 0
                    to: 360
                    duration: 800
                    loops: Animation.Infinite
                    running: leaguesHandler ? leaguesHandler.refreshing : false
                }

                MouseArea {
                    id: refreshArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: (leaguesHandler && leaguesHandler.refreshCooldown) ? Qt.ForbiddenCursor : Qt.PointingHandCursor
                    onClicked: leaguesHandler.refresh()
                }
            }
        }

        ListView {
            id: leagueList
            width: 400
            height: 300
            model: leaguesHandler ? leaguesHandler.leagues : []
            spacing: 5
            delegate: Rectangle {
                id: delegateRect
                width: parent.width
                height: 40
                radius: 5
                border.color: leagueArea.containsMouse ? "#aa6a9d" : "#7a4a6d"
                border.width: 1

                property bool isNew: leaguesHandler ? leaguesHandler.newLeagueIds.indexOf(modelData["league_id"]) !== -1 : false
                property color baseColor: index % 2 === 0 ? "#3a2040" : "#4a2a3d"
                color: leagueArea.containsMouse ? "#6a3a5d" : baseColor

                SequentialAnimation {
                    id: greenShine
                    running: delegateRect.isNew
                    ColorAnimation { target: delegateRect; property: "baseColor"; to: "#2a6a2a"; duration: 300 }
                    PauseAnimation { duration: 1400 }
                    ColorAnimation { target: delegateRect; property: "baseColor"; to: index % 2 === 0 ? "#3a2040" : "#4a2a3d"; duration: 300 }
                    onFinished: leaguesHandler.clearNewLeagueIds()
                }

                Behavior on color {
                    ColorAnimation { duration: 150 }
                }

                Behavior on border.color {
                    ColorAnimation { duration: 150 }
                }

                MouseArea {
                    id: leagueArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                }

                RowLayout {
                    anchors.fill: parent
                    spacing: 10
                    Text {
                        text: modelData["name"] + " | " + modelData["season_year"]
                        color: "#fff"
                        font.family: byteBounce.name
                        font.pixelSize: 20
                        horizontalAlignment: Text.AlignHCenter
                        Layout.fillWidth: true
                        Layout.alignment: Qt.AlignVCenter
                    }
                }
            }
            clip: true
        }
    }

    Text {
        visible: leaguesHandler ? leaguesHandler.leagues.length === 0 : false
        text: "wtf, you have no " + (leaguesHandler ? leaguesHandler.sportName : "") + " fantasy leagues?\n\n\nYou should play, it's fun imo"
        color: "#fff"
        font.family: byteBounce.name
        font.pixelSize: 40
        wrapMode: Text.Wrap
        horizontalAlignment: Text.AlignHCenter
        width: 400
        anchors.centerIn: parent
    }

    Image {
        id: bubbleIcon
        source: basePath + "Resources/sprites/bubble/text-bubble.png"
        width: 150
        height: 63.5
        visible: false
        z: 10

        Text {
            text: "yo, relax"
            color: "#000"
            font.family: byteBounce.name
            font.pixelSize: 20
            anchors.centerIn: parent
            anchors.verticalCenterOffset: -4
        }

        function updatePosition() {
            var mapped = refreshIcon.mapToItem(bubbleIcon.parent, refreshIcon.width, 0)
            bubbleIcon.x = mapped.x - 8
            bubbleIcon.y = mapped.y - bubbleIcon.height - 36
        }

        SequentialAnimation {
            id: bubbleAnim
            running: false
            ScriptAction { script: bubbleIcon.updatePosition() }
            PropertyAction { target: bubbleIcon; property: "visible"; value: true }
            PauseAnimation { duration: 5000 }
            PropertyAction { target: bubbleIcon; property: "visible"; value: false }
        }

        Connections {
            target: leaguesHandler
            function onRefreshCooldownChanged() {
                if (leaguesHandler.refreshCooldown) {
                    bubbleAnim.start()
                }
            }
        }
    }
}
