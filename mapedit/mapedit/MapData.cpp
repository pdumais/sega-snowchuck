#include "MapData.h"
#include <QFile>
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QDebug>

MapData::MapData(QString fname)
{
    QJsonParseError error;
    QFile file(fname);

    if (!file.open(QIODevice::ReadOnly)) {
        qWarning() << "Failed to open:" << fname;
        return;
    }

    QByteArray data = file.readAll();
    file.close();

    QJsonDocument doc = QJsonDocument::fromJson(data, &error);
    if (error.error != QJsonParseError::NoError) {
        qWarning() << "JSON parse error:" << error.errorString();
        return;
    }


    this->mRoot = doc.object();
    this->mLevels = this->mRoot["l"].toObject();
    this->mPalettes = this->mRoot["p"].toArray();
    this->mSpritesLookup = this->mRoot["sprnames"].toArray();

}

QString MapData::getBlockName(int level, int num)
{

    for (auto key : this->mSpritesLookup[level].toObject().keys())
    {
        if (this->mSpritesLookup[level].toObject().value(key) == num)
        {
            return key;
        }
    }

    return "";
}

QVector<QColor> MapData::getPalette(int level, int palIndex)
{
    QVector<QColor> ret;

    auto pal = this->mPalettes[level].toArray()[0].toArray()[palIndex].toArray();
    for (auto p : pal)
    {
        int val = p.toInt();
        int r = (val>>1)&0x7;
        int g = (val>>5)&0x7;
        int b = (val>>9)&0x7;

        r = r*32;
        g = g*32;
        b = b*32;

        ret.append(QColor(r,g,b));
    }

    return ret;
}

int MapData::getLevelCount()
{
    int count = this->mLevels["max"].toInt()-1;

    return count;
}

int MapData::getBlockCount(int level)
{
    int count = this->mLevels["levels"].toArray()[level].toObject()["cmax"].toInt();
    return count;
}

int MapData::getObjectsCount(int level)
{
    int count = this->mLevels["levels"].toArray()[level].toObject()["tmax"].toInt();
    return count;
}

int MapData::getBadGuysCount(int level)
{
    int count = this->mLevels["levels"].toArray()[level].toObject()["bmax"].toInt();
    return count;
}

QVector<QVector<MapGroundObject>> MapData::getGround(int level)
{
    QVector<QVector<MapGroundObject>> ret;
    QJsonArray ground = this->mLevels["levels"].toArray()[level].toObject()["ground"].toArray();
    for (int i = 0; i < this->getBlockCount(level); i++)
    {
        QVector<MapGroundObject> col;
        for (int c = 0; c < 5; c++)
        {
            MapGroundObject mo;
            int num = ground[i].toObject()["num"].toArray()[c].toInt();
            if (num != 255)
            {
                QString fname = this->getBlockName(level, num);
                mo.img = QImage("../../images/"+fname+".bmp");
            }
            mo.y = ground[i].toObject()["y"].toArray()[c].toInt();
            col.append(mo);
        }
        ret.append(col);
    }
    return ret;
}

QVector<MapObject> MapData::getObjects(int level)
{
    QVector<MapObject> ret;
    QJsonArray objs = this->mLevels["levels"].toArray()[level].toObject()["thing"].toArray();
    for (int i = 0; i < this->getObjectsCount(level); i++)
    {
        MapObject mo;
        auto o = objs[i].toObject();
        mo.x = o["x"].toInt();
        mo.y = o["y"].toInt();
        int num = o["num"].toInt();
        QString fname = this->getBlockName(level, num);
        qDebug() << "Object " << num << " from " << fname;
        mo.img = QImage("../../images/"+fname+".bmp");
        ret.append(mo);
    }

    return ret;

}

QVector<MapObject> MapData::getBadGuys(int level)
{
    QVector<MapObject> ret;
    QJsonArray objs = this->mLevels["levels"].toArray()[level].toObject()["badguys"].toArray();
    for (int i = 0; i < this->getBadGuysCount(level); i++)
    {
        MapObject mo;
        auto o = objs[i].toObject();
        mo.x = o["x"].toInt();
        mo.y = o["y"].toInt();
        int num = o["num"].toInt();
        QString fname = this->getBlockName(level, num);
        qDebug() << "BadGuy " << num << " from " << fname;
        mo.img = QImage("../../images/"+fname+".bmp");
        ret.append(mo);
    }

    return ret;

}

void MapData::updateData(int level, QVector<QVector<MapGroundObject>>& ground, QVector<MapObject>& objects, QVector<MapObject>& badGuys)
{


    auto levels = this->mLevels["levels"].toArray();
    auto levelObject = levels[level].toObject();
    auto groundColumns = levelObject["ground"].toArray();

    int x = 0;
    for (auto col : ground)
    {
        auto jsoncol = groundColumns[x].toObject();
        auto yArray = jsoncol["y"].toArray();
        int y = 0;
        for (auto mo : col)
        {
            yArray[y] = QJsonValue(mo.y);
            y++;
        }
        jsoncol["y"] = yArray;
        groundColumns[x] = jsoncol;
        x++;
    }

    levelObject.insert("ground", groundColumns);
    levels[level] = levelObject;
    this->mLevels.insert("levels", levels);
    this->mRoot.insert("l", this->mLevels);

}

void MapData::commit()
{
    QJsonDocument doc(this->mRoot);
    QFile file("map.json");
    if (file.open(QIODevice::WriteOnly)) {
        file.write(doc.toJson());
        file.close();
    }

}
