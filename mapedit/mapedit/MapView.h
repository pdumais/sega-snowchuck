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

    void setMap(int lenght, QVector<QVector<MapGroundObject>> ground);
    void setViewPortStartIndex(int index);

protected:

private:
    int mBlockCount;
    QVector<QVector<MapGroundObject>> ground;
    QVector<QLabel*> mColumns;
    QVector<QLabel*> mSlots;
    QPoint mSelectedBlock;

    void _clearWindow();
    void _redraw();
    int mCurrentViewIndex;

signals:
    void viewPortChanged(int index);
};

#endif // MAPVIEW_H
