#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "MapData.h"
#include "MapView.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void on_comboBox_currentIndexChanged(int index);

    void on_slider_valueChanged(int value);

    void on_pushButton_clicked();

private:
    Ui::MainWindow *ui;
    MapData* mpMapData;
    MapView *mpMapView;
};
#endif // MAINWINDOW_H
