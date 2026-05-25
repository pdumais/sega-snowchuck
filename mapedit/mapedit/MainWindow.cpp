#include "MainWindow.h"
#include "ui_MainWindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    this->mpMapView = new MapView(this->ui->frame1);
    QObject::connect(this->mpMapView, &MapView::viewPortChanged,[this](int index)
    {
        this->ui->slider->setMaximum(index);
    });


    this->mpMapView->show();

    this->mpMapData = new MapData("../../images/levels.json");
    for (int i = 0; i < this->mpMapData->getLevelCount(); i ++)
    {
        this->ui->comboBox->addItem("Level "+QString::number(i+1));
    }
    this->ui->comboBox->setCurrentIndex(0);
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_comboBox_currentIndexChanged(int index)
{
    int cmax = this->mpMapData->getBlockCount(index);
    this->mpMapView->setMap(cmax,this->mpMapData->getGround(index));
}


void MainWindow::on_slider_valueChanged(int value)
{
    this->mpMapView->setViewPortStartIndex(value);
}

