#include "MapView.h"
#include <QPainter>
#include <QPaintEvent>

const float zoom = 3.0f;

MapView::MapView(QWidget *parent): QWidget{parent}
{
    setAutoFillBackground(true);
    setFixedSize(1*24, (224+(5*24))*zoom);
    this-> mSelectedBlock = QPoint(0,0);
}

void MapView::setMap(int length,QVector<QVector<MapGroundObject>> ground)
{
    this->mBlockCount = length;
    setFixedSize(length*24*zoom, (224+(5*24))*zoom);
    this-> ground = ground;
}

void MapView::paintEvent(QPaintEvent *event)
{
    QWidget::paintEvent(event);

    QPainter painter(this);
    painter.setRenderHint(QPainter::Antialiasing, false);

    const int w = width();
    const int h = height();

    // Fill background (optional)
    painter.fillRect(rect(), Qt::white);


    // Draw vertical grid lines every 24 pixels
    painter.scale(zoom, zoom);
    QPen gridPen(Qt::black);
    gridPen.setWidth(1);
    painter.setPen(gridPen);
    painter.fillRect(0,0,w-1,224,QColor(0, 0, 0));
    painter.fillRect(0,224,w-1,h-1,QColor(0xA0, 0xA0, 0xA0));
    painter.drawRect(0, 0, w - 1, h - 1);


    // Now width/height must be converted to logical coords
    const int logicalW = width() / zoom;
    const int logicalH = height() / zoom;

    // Draw vertical lines every 24 logical pixels
    for (int x = 0; x < this->mBlockCount; x ++)
    {
        painter.drawLine(x*24, 0, x*24, logicalH);
        painter.drawText(x*24,10, QString::number(x));
        for (int n = 0; n < 5; n++)
        {
            auto mo = ground[x][n];
            if (mo.y < 200)
            {
                painter.drawImage(24*x,mo.y,mo.img);
            }
            painter.drawImage(24*x,200+(24*(5-n)),mo.img);
            painter.drawRect(24*x,200+(24*(5-n)),24,24);
        }
    }

    QPen selectedPen(Qt::red);
    selectedPen.setWidth(1);
    painter.setPen(selectedPen);
    int x = this-> mSelectedBlock.x();
    int y = this-> mSelectedBlock.y();
    auto mo = ground[x][y];
    if (mo.y < 200)
    {
        painter.drawRect(x*24, mo.y, 24, 24);
    }

    painter.drawRect(x*24, 200+(5-y)*24, 24, 24);
}

void MapView::mousePressEvent(QMouseEvent *event)
{
    // Convert screen coords → image coords
    int x = event->pos().x() / zoom;
    int y = event->pos().y() / zoom;

    if (x < 0 || y < 224)
        return;

    this->mSelectedBlock = QPoint(x/24, 5-((y-200)/24));

    update(); // trigger repaint
}
