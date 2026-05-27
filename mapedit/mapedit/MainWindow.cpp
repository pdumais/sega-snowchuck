#include "MainWindow.h"
#include "ui_MainWindow.h"
#include "palettewidget.h"
#include <QVBoxLayout>
#include <QPushButton>
#include <QIcon>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    auto palw1 = new PaletteWidget(this->ui->framepal);
    auto palw2 = new PaletteWidget(this->ui->framepal);
    auto palw3 = new PaletteWidget(this->ui->framepal);
    auto palw4 = new PaletteWidget(this->ui->framepal);
    palw1->move(0,0);
    palw2->move(0,24);
    palw3->move(0,48);
    palw4->move(0,72);

    this->mpMapView = new MapView(this->ui->frame1);
    QObject::connect(this->mpMapView, &MapView::viewPortChanged,[this](int index)
    {
        this->ui->slider->setMinimum(0);
        this->ui->slider->setMaximum(index);
        this->ui->slider->setValue(0);
    });


    this->mpMapView->show();

    this->mpMapData = new MapData("../../images/edited-map.json");
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
    qDebug() << "Refresh level " << index;
    int cmax = this->mpMapData->getBlockCount(index);
    this->mpMapView->setMap(cmax,this->mpMapData->getGround(index), this->mpMapData->getObjects(index), this->mpMapData->getBadGuys(index));
    auto palw1 = (PaletteWidget*)this->ui->framepal->children()[0];
    auto palw2 = (PaletteWidget*)this->ui->framepal->children()[1];
    auto palw3 = (PaletteWidget*)this->ui->framepal->children()[2];
    auto palw4 = (PaletteWidget*)this->ui->framepal->children()[3];
    palw1->setColours(this->mpMapData->getPalette(index,0));
    palw2->setColours(this->mpMapData->getPalette(index,1));
    palw3->setColours(this->mpMapData->getPalette(index,2));
    palw4->setColours(this->mpMapData->getPalette(index,3));

    const auto children = this->ui->frameobj->findChildren<QPushButton*>(QString(), Qt::FindDirectChildrenOnly);
    for (QPushButton *child : children) delete child;
    int x = 0;
    for (auto mo : this->mpMapData->getObjectTypes(index))
    {
        qDebug() << "Adding object type " << mo.type;
        auto b = new QPushButton(this->ui->frameobj);
        b->setFixedSize(24,24);
        QIcon icon(QPixmap::fromImage(mo.img));
        b->setIcon(icon);
        b->move(x,0);
        b->show();
        QObject::connect(b, &QPushButton::clicked,[this, mo](bool down)
        {
            this->mpMapView->startAddObject(mo.img, mo.type);
        });
        x+=26;
    }
}


void MainWindow::on_slider_valueChanged(int value)
{
    this->mpMapView->setViewPortStartIndex(value);
}


void MainWindow::on_pushButton_clicked()
{
    this->mpMapView->updateMapData(this->ui->comboBox->currentIndex(), this->mpMapData);
}

