#ifndef PALETTEWIDGET_H
#define PALETTEWIDGET_H

#include <QWidget>
#include <QVector>
#include <QColor>

class PaletteWidget : public QWidget
{
    Q_OBJECT
public:
    explicit PaletteWidget(QWidget *parent = nullptr);

    void setColours(QVector<QColor> cols);
protected:
    void paintEvent(QPaintEvent *) override;

private:
    QVector<QColor> mColours;
signals:
};

#endif // PALETTEWIDGET_H
