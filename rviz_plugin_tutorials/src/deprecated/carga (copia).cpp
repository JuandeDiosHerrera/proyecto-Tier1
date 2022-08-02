#include <stdio.h>

#include <geometry_msgs/Twist.h>

//MOD
#include "std_msgs/String.h"
#include "boost/thread/mutex.hpp"
#include "boost/thread/thread.hpp"
#include "ros/console.h"
#include <ros/ros.h>
#include <std_srvs/Trigger.h>

//MOD

#include "carga.h"

using namespace std;

namespace rviz_plugin_tutorials
{

// We start with the constructor, doing the standard Qt thing of
// passing the optional *parent* argument on to the superclass
// constructor.
PanelCarga::PanelCarga(QWidget* parent) :
		rviz::Panel(parent)
{
	/*MOD*/
    centralWidget = new QWidget();
    gridLayoutWidget = new QWidget(centralWidget);
    gridLayoutWidget->setGeometry(QRect(20, 20, 361, 351));
    gridLayout = new QGridLayout(gridLayoutWidget);
    gridLayout->setSpacing(6);
    gridLayout->setContentsMargins(11, 11, 11, 11);
    gridLayout->setContentsMargins(0, 0, 0, 0);
//    verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);
//
//    gridLayout->addItem(verticalSpacer, 0, 1, 1, 1);
//
//    verticalSpacer_2 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);
//
//    gridLayout->addItem(verticalSpacer_2, 2, 1, 1, 1);
//
//    horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
//
//    gridLayout->addItem(horizontalSpacer, 0, 0, 3, 1);
//
//    horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
//
//    gridLayout->addItem(horizontalSpacer_2, 0, 2, 3, 1);
//
//    groupBox = new QGroupBox(gridLayoutWidget);
//    groupBox->setEnabled(true);
//    QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
//    sizePolicy.setHorizontalStretch(0);
//    sizePolicy.setVerticalStretch(0);
//    sizePolicy.setHeightForWidth(groupBox->sizePolicy().hasHeightForWidth());
//    groupBox->setSizePolicy(sizePolicy);
//    groupBox->setMaximumSize(QSize(300, 100));
//    QFont font;
//    font.setBold(false);
//    font.setItalic(false);
//    font.setUnderline(false);
//    font.setWeight(50);
//    font.setStrikeOut(false);
//    font.setKerning(true);
//    font.setStyleStrategy(QFont::PreferDefault);
//    groupBox->setFont(font);
//    groupBox->setCursor(QCursor(Qt::ArrowCursor));
//    groupBox->setLayoutDirection(Qt::LeftToRight);
//    groupBox->setAutoFillBackground(false);
//    groupBox->setStyleSheet(QLatin1String("			QGroupBox\n"
//"			 {\n"
//"			border: 0.5px solid gray;\n"
//"			border-radius: 2px;\n"
//"			margin-top: 0.5em;\n"
//"			}\n"
//"			QGroupBox::Title\n"
//"			{\n"
//"			subcontrol-origin: margin;\n"
//"			left: 10px;\n"
//"			padding: 0 3px 0 3px;\n"
//"			}"));
//    groupBox->setAlignment(Qt::AlignCenter);
//    horizontalLayoutWidget = new QWidget(groupBox);
//    horizontalLayoutWidget->setGeometry(QRect(10, 20, 271, 51));
//    horizontalLayout = new QHBoxLayout(horizontalLayoutWidget);
//    horizontalLayout->setSpacing(6);
//    horizontalLayout->setContentsMargins(11, 11, 11, 11);
//    horizontalLayout->setContentsMargins(0, 0, 0, 0);
//    pushButton_2 = new QPushButton(horizontalLayoutWidget);
//
//    horizontalLayout->addWidget(pushButton_2);
//
//    horizontalSpacer_3 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
//
//    horizontalLayout->addItem(horizontalSpacer_3);
//
//    progressBar = new QProgressBar(horizontalLayoutWidget);
//    progressBar->setValue(0);
//
//    horizontalLayout->addWidget(progressBar);
//
//    horizontalLayout->setStretch(0, 5);
//    horizontalLayout->setStretch(1, 1);
//    horizontalLayout->setStretch(2, 10);
//
//    gridLayout->addWidget(groupBox, 1, 1, 1, 1);
//
//    verticalSpacer_3 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);
//
//    gridLayout->addItem(verticalSpacer_3, 4, 1, 1, 1);
//
//    textBrowser = new QTextBrowser(gridLayoutWidget);
//    textBrowser->setMaximumSize(QSize(300, 300));
//
//    gridLayout->addWidget(textBrowser, 3, 1, 1, 1);
//
//    gridLayout->setRowStretch(0, 1);
//    gridLayout->setRowStretch(1, 30);
//    gridLayout->setRowStretch(2, 1);
//    gridLayout->setRowStretch(3, 30);
//    gridLayout->setRowStretch(4, 1);
//    gridLayout->setColumnStretch(0, 1);
//    gridLayout->setColumnStretch(1, 13);
//    gridLayout->setColumnStretch(2, 1);

    	setLayout(gridLayout);

    	QTimer* output_timer = new QTimer(this);

    	// Next we make signal/slot connections.
    	//connect( drive_widget_, SIGNAL( outputVelocity( float, float )), this, SLOT( setVel( float, float )));
    //	connect(output_topic_editor_, SIGNAL(editingFinished()), this,
    //			SLOT(updateTopic()));
    //	connect(output_timer, SIGNAL(timeout()), this, SLOT(sendVel()));

    	/*MOD*/
    	connect(pushButton, SIGNAL(clicked()), this, SLOT(manejadorBoton()));
    	/*FIN MOD*/

    	//MOD BOTÓN DE SALIDA DE PROGRAMA
    //	connect(boton_salida, SIGNAL(clicked()), this,
    //			SLOT(manejadorBotonSalida()));
    	// Start the timer.
    	output_timer->start(100);

    	// Make the control widget start disabled, since we don't start with an output topic.
    //	drive_widget_->setEnabled(false);

}

void PanelCarga::manejadorBoton()
{
}

//int main(int argc, char *argv[])
//{
//	ROS_INFO("Iniciando panel");
//	ros::init(argc, argv, "panelCarga"); //Le pasamos el nombre del nodo: panel
//	PanelCarga panel;
//	ros::spin();
//	return 0;
//}

} // end namespace rviz_plugin_tutorials

// Tell pluginlib about this class.  Every class which should be
// loadable by pluginlib::ClassLoader must have these two lines
// compiled in its .cpp file, outside of any namespace scope.
#include <pluginlib/class_list_macros.h>
PLUGINLIB_EXPORT_CLASS(rviz_plugin_tutorials::PanelCarga, rviz::Panel)
// END_TUTORIAL

