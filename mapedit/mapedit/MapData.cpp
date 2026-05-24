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

}

int MapData::getLevelCount()
{
    int count = this->mRoot["max"].toInt()-1;

    return count;
}

int MapData::getBlockCount(int level)
{
    int count = this->mRoot["levels"].toArray()[level].toObject()["cmax"].toInt();
    return count;
}

QVector<QVector<MapGroundObject>> MapData::getGround(int level)
{
    QVector<QVector<MapGroundObject>> ret;
    QJsonArray ground = this->mRoot["levels"].toArray()[level].toObject()["ground"].toArray();
    for (int i = 0; i < this->getBlockCount(level); i++)
    {
        QVector<MapGroundObject> col;
        for (int c = 0; c < 5; c++)
        {
            MapGroundObject mo;
            int num = ground[i].toObject()["num"].toArray()[c].toInt();
            if (num != 255)
            {
                mo.img = QImage("../../images/cube"+QString::number(num)+".bmp");
            }
            mo.y = ground[i].toObject()["y"].toArray()[c].toInt();
            col.append(mo);
        }
        ret.append(col);
    }
    return ret;
}
