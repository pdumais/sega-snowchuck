#ifndef MAPDATA_H
#define MAPDATA_H

#include <QObject>
#include <QJsonObject>
#include <QJsonArray>
#include <QImage>
#include <QVector>
#include <QColor>

class MapGroundObject
{
public:
    QImage   img;
    int           y;
};

class MapObject
{
public:
    QImage   img;
    int           y;
    int           x;
    int num;
};

class MapObjectType
{
public:
    QImage img;
    int type;
};

class MapData
{
public:
    MapData(QString fname);

    int     getLevelCount();
    int     getBlockCount(int level);
    int     getObjectsCount(int level);
    int     getBadGuysCount(int level);
    QVector<QColor> getPalette(int level, int palIndex);

    QVector<QVector<MapGroundObject>> getGround(int level);
    QVector<MapObject> getObjects(int level);
    QVector<MapObject> getBadGuys(int level);

    QVector<MapObjectType> getObjectTypes(int level);

    QString getBlockName(int level, int num);

    void updateData(int level, QVector<QVector<MapGroundObject>>& ground, QVector<MapObject>& objects, QVector<MapObject>& badGuys);
    void commit();

private:
    QJsonObject mRoot;
    QJsonObject mLevels;
    QJsonArray mPalettes;
    QJsonArray mSpritesLookup;
};

#endif // MAPDATA_H
