#include "MapView.h"
#include <QPainter>
#include <QPaintEvent>
#include <QLabel>
#include <QPixmap>
#include "ClickableQLabel.h"
#include <QDebug>
#include "ClickableQLabel.h"

const int tileZoom = 2;
const int numHTiles = 25;

MapView::MapView(QWidget *parent): QWidget{parent}
{
    this->setFocusPolicy(Qt::StrongFocus);
    this->mCurrentViewIndex = 0;
    this-> mSelectedBlock = BlockSelection{0,0, false};
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
        label->setMouseTracking(true);

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
    this->mObjectToAdd = new QLabel(this);
    this->mObjectToAdd->move(0,0);
    this->mObjectToAdd->setFixedSize(24*tileZoom, 24*tileZoom);
    this->mObjectToAdd->hide();
    this->mObjectToAdd->setAttribute(Qt::WA_TransparentForMouseEvents);
    this->setMouseTracking(true);
}

void MapView::mouseMoveEvent(QMouseEvent *event)
{
    QPoint pos = event->pos();
    int x = (pos.x()/(24*tileZoom))*24*tileZoom;
    int y = ((pos.y()/tileZoom) & 0xFFFFFFF8)*tileZoom;

    if (!this->mObjectToAdd->isHidden())
    {
        // Adding an object
        if (x > 0 && x < (numHTiles*24*tileZoom) && y > 0)
        {
            this->mObjectToAdd->move(x,y);
        }
    }
    else
    {
        if (this->mSelectedObject.valid)
        {
            // TODO: Move object. Can we just move the qlabel directly and commit to mo (and redraw) once user clicks?
            //auto mo = &ground[this->mSelectedObject.x][this->mSelectedObject.slot];
            //mo->y
        }

    }

    QWidget::mouseMoveEvent(event);
}

void MapView::mousePressEvent(QMouseEvent *event)
{
    QPoint pos = event->pos();
    int x = ((pos.x())/(24*tileZoom))*24;
    int y = (pos.y()/tileZoom) & 0xFFFFFFF8;

    x += (this->mCurrentViewIndex*24);
    if (!this->mObjectToAdd->isHidden())
    {
        MapObject mo;
        mo.img =  this->mObjectToAdd->pixmap(Qt::ReturnByValueConstant()).toImage();
        mo.x = x;
        mo.y = y;
        mo.num = this->mObjectToAdd->property("num").toInt();
        this->mObjects.append(mo);
        this->mObjectToAdd->hide();
        this->_clearWindow();
        this->_redraw();
    }
}


void MapView::setMap(int length,QVector<QVector<MapGroundObject>> ground, QVector<MapObject> objects, QVector<MapObject> badGuys)
{
    this->mObjectToAdd->hide();
    this->mBlockCount = length;
    this->ground = ground;
    this->mObjects = objects;
    this->mBadGuys = badGuys;

    this->mCurrentViewIndex = 0;
    this->_clearWindow();
    this->_redraw();
    emit this->viewPortChanged(this->mBlockCount);
}

void MapView::deleteCurrentBlock()
{
    if (this->mSelectedObject.valid)
    {
        qDebug() << this->mObjects.length();
        int idx = this->mSelectedObject.slot;
        this->mObjects.remove(idx);
        this->mSelectedObject.valid = false;
        qDebug() << this->mObjects.length();
    }
    else if (this->mSelectedBlock.valid)
    {
        int x = this->mSelectedBlock.x;
        int y = this->mSelectedBlock.slot;
        auto mo = &ground[x][y];
        if (mo->img.isNull()) return;
    
        this->mSelectedBlock.valid = false;
        mo->img = QImage();
    }
    else
    {
        return;
    }

    this->_clearWindow();
    this->_redraw();

}

void MapView::keyPressEvent(QKeyEvent *event)
{
    if (event->key() == Qt::Key_Escape) {
        this->stopAddObject();
        event->accept();
        return;
    }
    if (event->key() == Qt::Key_Delete) {
        this->deleteCurrentBlock();
        event->accept();
        return;
    }
    QWidget::keyPressEvent(event);
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
void MapView::wheelEvent(QWheelEvent *event)
{
    QPoint numPixels = event->pixelDelta();
    if (!this->mSelectedBlock.valid) return;

    int x = this->mSelectedBlock.x;
    int y = this->mSelectedBlock.slot;
    auto mo = &ground[x][y];
    if (mo->img.isNull()) return;
    if (mo->y > 200) return;

    if (numPixels.y() < 0 && mo->y < 200)
    {
        mo->y = (mo->y+8)&0xFFFFFFF8;
    }
    if (numPixels.y() > 0 && mo->y > 0)
    {
        mo->y = (mo->y-8)&0xFFFFFFF8;
    }
    this->_clearWindow();
    this->_redraw();
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
            if (!mo.img.isNull()) slot->setPixmap(QPixmap::fromImage(mo.img.scaled(24*tileZoom,24*tileZoom)));
            slot->setStyleSheet("border-left: 1px solid black;");
            slot->show();
            QObject::connect(slot, &ClickableQLabel::clicked,[this,n,tileIndex](ClickableQLabel* lbl)
            {
                qDebug() << "Click: " << tileIndex << " " << n;
                this->mSelectedBlock = BlockSelection{tileIndex,n, true};
                this->mSelectedObject = BlockSelection{0,0,false};
                this->_clearWindow();
                this->_redraw();
            });

            if (this->mSelectedBlock.slot == n && this->mSelectedBlock.x == tileIndex && this->mSelectedBlock.valid)
            {
                slot->setStyleSheet("border: 2px solid red;");
                tile->setStyleSheet("border: 2px solid red;");
            }
        }
    }

    for (int idx = 0; idx < this->mObjects.length(); idx++)
    {
        auto o = this->mObjects[idx];
        //qDebug() << "idx: " << idx << ", Index: " << this->mObjects.indexOf(o);
        int x = o.x - (this->mCurrentViewIndex*24);
        int col = x/24;
        x = x%24;

        if (col < 0) continue;
        if (col >= this->mColumns.length()) continue;

        ClickableQLabel *tile = new ClickableQLabel(this->mColumns[col]);
        tile->move(x,o.y*tileZoom);
        tile->setFixedSize(24*tileZoom, 24*tileZoom);
        if (!o.img.isNull()) tile->setPixmap(QPixmap::fromImage(o.img.scaled(24*tileZoom,24*tileZoom)));
        tile->setStyleSheet("border-left: 1px solid black;");
        tile->show();
        QObject::connect(tile, &ClickableQLabel::clicked,[this,idx](ClickableQLabel* lbl)
        {
            this->mSelectedBlock = BlockSelection{0,0,false};
            this->mSelectedObject = BlockSelection{0, idx, true};
            this->_clearWindow();
            this->_redraw();
        });
        if (this->mSelectedObject.slot == idx && this->mSelectedObject.valid)
        {
            tile->setStyleSheet("border: 2px solid red;");
        }
    }

    for (auto o : this->mBadGuys)
    {
        int x = o.x - (this->mCurrentViewIndex*24);
        int col = x/24;
        x = x%24;

        if (col < 0) continue;
        if (col >= this->mColumns.length()) continue;

        QLabel *tile = new QLabel(this->mColumns[col]);
        tile->move(x,o.y*tileZoom);
        tile->setFixedSize(24*tileZoom, 24*tileZoom);
        if (!o.img.isNull()) tile->setPixmap(QPixmap::fromImage(o.img.scaled(24*tileZoom,24*tileZoom)));
        tile->setStyleSheet("border-left: 1px solid black;");
        tile->show();
    }

}

void MapView::setViewPortStartIndex(int index)
{
    this->mCurrentViewIndex = index;
    this->_clearWindow();
    this->_redraw();
}

void MapView::updateMapData(int level, MapData* pMapData)
{
    pMapData->updateData(level, this->ground, this->mObjects, this->mBadGuys);
    pMapData->commit();
}



void MapView::startAddObject(QImage img, int type)
{
    this->mObjectToAdd->setPixmap(QPixmap::fromImage(img.scaled(24*tileZoom,24*tileZoom)));
    this->mObjectToAdd->show();
    this->mObjectToAdd->move(0,0);
    this->mObjectToAdd->setProperty("num",type);


}

void MapView::stopAddObject()
{
    this->mObjectToAdd->hide();
}
