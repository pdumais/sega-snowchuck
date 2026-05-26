#ifndef MAPVIEW_H
#define MAPVIEW_H

#include <QObject>
#include <QWidget>
#include "MapData.h"
#include <QLabel>

class MapView : public QWidget
{
    Q_OBJECT
public:
    explicit MapView(QWidget *parent = nullptr);

    void setMap(int lenght, QVector<QVector<MapGroundObject>> ground, QVector<MapObject> objects, QVector<MapObject> badGuys);
    void setViewPortStartIndex(int index);
    void updateMapData(int level, MapData* pMapData);

protected:
    void wheelEvent(QWheelEvent *event) override;

private:
    struct BlockSelection {
        int x;
        int slot;
    };
    int mBlockCount;
    QVector<QVector<MapGroundObject>> ground;
    QVector<MapObject> mObjects;
    QVector<MapObject> mBadGuys;
    QVector<QLabel*> mColumns;
    QVector<QLabel*> mSlots;

    void _clearWindow();
    void _redraw();
    int mCurrentViewIndex;
    BlockSelection mSelectedBlock;

signals:
    void viewPortChanged(int index);
};

#endif // MAPVIEW_H
