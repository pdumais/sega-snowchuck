#ifndef MAPDATA_H
#define MAPDATA_H

#include <QObject>
#include <QJsonObject>
#include <QImage>
#include <QVector>

class MapGroundObject
{
public:
    QImage   img;
    int           y;
};

class MapData
{
public:
    MapData(QString fname);

    int     getLevelCount();
    int     getBlockCount(int level);

    QVector<QVector<MapGroundObject>> getGround(int level);

private:
    QJsonObject mRoot;
};

#endif // MAPDATA_H
