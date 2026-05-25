#include "MapView.h"
#include <QPainter>
#include <QPaintEvent>
#include <QLabel>
#include <QPixmap>
#include "ClickableQLabel.h"
#include <QDebug>
#include "ClickableQLabel.h"

const int tileZoom = 3;
const int numHTiles = 25;

MapView::MapView(QWidget *parent): QWidget{parent}
{
    //setAutoFillBackground(true);
    this->mCurrentViewIndex = 0;
    this-> mSelectedBlock = QPoint(0,0);
    this->setFixedSize(tileZoom*24*numHTiles,(224+5*(24+2))*tileZoom);
    this->move(0,0);

    for (int i = 0; i < numHTiles; ++i)
    {
        QLabel *label = new QLabel(this);
        label->setGeometry(i * (24*tileZoom), 0, (24*tileZoom), 224*tileZoom);
        label->setStyleSheet(
            "background-color: rgb(0,0,255);"
            "border: 1px solid black;"
        );

        this->mColumns.append(label);

        QLabel *labelSlot = new ClickableQLabel(this);
        labelSlot->setFixedSize(24*tileZoom, (24+2)*5*tileZoom);
        labelSlot->move(i * (24*tileZoom),(220+4)*tileZoom);
        labelSlot->setStyleSheet(
            "background-color: rgb(210,210,210);"
            "border: 1px solid black;"
        );

        this->mSlots.append(labelSlot);
    }

}

void MapView::setMap(int length,QVector<QVector<MapGroundObject>> ground)
{
    this->mBlockCount = length;
    this-> ground = ground;
    this->mCurrentViewIndex = 0;
    this->_clearWindow();
    this->_redraw();
    emit this->viewPortChanged(this->mBlockCount);
}

void MapView::_clearWindow()
{
    for (QWidget *col : mColumns)
    {
        const auto children = col->findChildren<QLabel*>(QString(), Qt::FindDirectChildrenOnly);

        for (QLabel *child : children)
        {
            delete child;
        }
    }
    for (QWidget *col : mSlots)
    {
        const auto children = col->findChildren<QLabel*>(QString(), Qt::FindDirectChildrenOnly);

        for (QLabel *child : children)
        {
            delete child;
        }
    }
}

void MapView::_redraw()
{
    for (int i = 0; i < this->mColumns.length(); i++)
    {

        int tileIndex = i + this->mCurrentViewIndex;
        int maxIndex = ground.length();
        if (tileIndex >= maxIndex)
        {
            continue;
        }

        for (int n = 0; n < 5; n++)
        {

            auto mo = ground[tileIndex][n];
            QLabel *tile = new QLabel(this->mColumns[i]);
            tile->move(0,mo.y*tileZoom);
            tile->setFixedSize(24*tileZoom, 24*tileZoom);
            if (mo.y < 200)
            {
                tile->setPixmap(QPixmap::fromImage(mo.img.scaled(24*tileZoom,24*tileZoom)));
            }
            tile->setStyleSheet("border-left: 1px solid black;");
            tile->show();

            ClickableQLabel *slot = new ClickableQLabel(this->mSlots[i]);
            int slotY = (4-n)*24;

            slot->move(0,slotY*tileZoom);
            slot->setFixedSize(24*tileZoom, 24*tileZoom);
            slot->setPixmap(QPixmap::fromImage(mo.img.scaled(24*tileZoom,24*tileZoom)));
            slot->setStyleSheet("border-left: 1px solid black;");
            slot->show();
            QObject::connect(slot, &ClickableQLabel::clicked,[this](ClickableQLabel* lbl)
            {
                qDebug() << "Click";
            });
        }
    }
}

void MapView::setViewPortStartIndex(int index)
{
    this->mCurrentViewIndex = index;
    this->_clearWindow();
    this->_redraw();
}


