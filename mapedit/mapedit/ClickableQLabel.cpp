#include "ClickableQLabel.h"
#include <QMouseEvent>

ClickableQLabel::ClickableQLabel(QWidget *parent): QLabel(parent)
{

}

void ClickableQLabel::mousePressEvent(QMouseEvent *event)
{
    if (event->button() == Qt::LeftButton)
    {
        emit this->clicked(this);
    }

    //QLabel::mousePressEvent(event);
}
