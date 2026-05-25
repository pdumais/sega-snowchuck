#ifndef CLICKABLEQLABEL_H
#define CLICKABLEQLABEL_H

#include <QObject>
#include <QLabel>

class ClickableQLabel: public QLabel
{
    Q_OBJECT
public:
    explicit ClickableQLabel(QWidget *parent = nullptr);

protected:
    void mousePressEvent(QMouseEvent *event) override;

signals:
    void clicked(ClickableQLabel* label);
};

#endif // CLICKABLEQLABEL_H
