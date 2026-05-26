#include "palettewidget.h"
#include <QLabel>
#include <QPainter>

PaletteWidget::PaletteWidget(QWidget *parent)
    : QWidget{parent}
{
    this->setFixedSize(16*24,24);
    for (int i = 0; i < 16; i++)
    {
        this->mColours.append(Qt::white);
    }
}

void PaletteWidget::setColours(QVector<QColor> cols)
{
    this->mColours = cols;
    this->update();
}

void PaletteWidget::paintEvent(QPaintEvent *)
{
    QPainter p(this);

    int x = 0;
    for (QColor col : this->mColours)
    {
        p.fillRect(x,0,24,24, col);
        x+=24;
    }

    //p.setPen(Qt::black);
    //p.drawRect(rect().adjusted(0, 0, -1, -1));
}
