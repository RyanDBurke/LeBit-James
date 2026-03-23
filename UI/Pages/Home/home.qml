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
            }
        }
    }
}
