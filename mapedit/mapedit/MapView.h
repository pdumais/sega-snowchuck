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
    void startAddObject(QImage img, int type);
    void stopAddObject();


protected:
    void wheelEvent(QWheelEvent *event) override;
    void mouseMoveEvent(QMouseEvent *event) override;
    void mousePressEvent(QMouseEvent *event) override;
    void keyPressEvent(QKeyEvent *event) override;

private:
    struct BlockSelection {
        int x;
        int slot;
        bool valid;
    };
    int mBlockCount;
    QVector<QVector<MapGroundObject>> ground;
    QVector<MapObject> mObjects;
    QVector<MapObject> mBadGuys;
    QVector<QLabel*> mColumns;
    QVector<QLabel*> mSlots;
    BlockSelection mSelectedBlock;
    BlockSelection mSelectedObject;
    QLabel* mObjectToAdd;

    void _clearWindow();
    void _redraw();
    void deleteCurrentBlock();
    int mCurrentViewIndex;
    

signals:
    void viewPortChanged(int index);
};

#endif // MAPVIEW_H
