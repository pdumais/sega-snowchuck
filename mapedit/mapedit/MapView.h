#ifndef MAPVIEW_H
#define MAPVIEW_H

#include <QObject>
#include <QWidget>
#include "MapData.h"

class MapView : public QWidget
{
    Q_OBJECT
public:
    explicit MapView(QWidget *parent = nullptr);

    void setMap(int lenght, QVector<QVector<MapGroundObject>> ground);
protected:
    void paintEvent(QPaintEvent *event) override;
    void mousePressEvent(QMouseEvent *event) override;

private:
    int mBlockCount;
    QVector<QVector<MapGroundObject>> ground;
    QPoint mSelectedBlock;
signals:

};

#endif // MAPVIEW_H
