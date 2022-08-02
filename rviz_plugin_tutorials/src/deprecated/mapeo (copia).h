#ifndef PANEL_MAPEO_H
#define PANEL_MAPEO_H

#ifndef Q_MOC_RUN
# include <ros/ros.h>

# include <rviz/panel.h>

#include <QPushButton>

#include <std_srvs/Trigger.h>
#include "std_msgs/String.h"

//Añadidos por mí --> ui
#include <QGroupBox>
#include <QLocale>
#include <QVariant>
#include <QAction>
#include <QApplication>
#include <QButtonGroup>
#include <QFrame>

#include <QHeaderView>
#include <QWidget>

#include <QPainter>
#include <QLineEdit>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QTimer>

#include <QPushButton>
#include <QProgressBar>

#include <QSpacerItem>

/* 19/07/16 */
#include <QMainWindow>
#include <QMenuBar>
#include <QStatusBar>
#include <QTextBrowser>
#include <QToolBar>
//FIN Añadidos por mí --> ui

#include <signal.h>

#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <string>
#include <cstdlib>

#include "programa_central/mensajes.h"

#endif

class QLineEdit;

namespace rviz_plugin_tutorials
{

class DriveWidget;

// BEGIN_TUTORIAL
// Here we declare our new subclass of rviz::Panel.  Every panel which
// can be added via the Panels/Add_New_Panel menu is a subclass of
// rviz::Panel.
class PanelMapeo: public rviz::Panel
{
// This class uses Qt slots and is a subclass of QObject, so it needs
// the Q_OBJECT macro.
	Q_OBJECT
public:
	// QWidget subclass constructors usually take a parent widget
	// parameter (which usually defaults to 0).  At the same time,
	// pluginlib::ClassLoader creates instances by calling the default
	// constructor (with no arguments).  Taking the parameter and giving
	// a default of 0 lets the default constructor work and also lets
	// someone using the class for something else to pass in a parent
	// widget as they normally would with Qt.
	PanelMapeo(QWidget* parent = 0);

	// Now we declare overrides of rviz::Panel functions for saving and
	// loading data from the config file.
	virtual void load(const rviz::Config& config);
	virtual void save(rviz::Config config) const;

	// Next come a couple of public Qt slots.
public Q_SLOTS:

	/*MOD*/
	void manejadorBoton1();
	void manejadorBoton2();
	void manejadorBoton3();
	void manejadorBoton4();
	void manejadorBoton5();
	void manejadorBoton5_1();

	void manejadorSIGINT(int sig);
	void manejadorSIGSEGV(int sig);
	void manejadorSIGTERM(int sig);
	void manejadorSIGHUP(int sig);
	void manejadorSIGQUIT(int sig);
	void manejadorSIGKILL(int sig);
	void manejadorSIGABRT(int sig);

	bool recibeMensajesMapeo(programa_central::mensajes::Request &req, programa_central::mensajes::Response &res);
	void imprimeInstrucciones();

	//FUNCIÓN QUE CONTROLA LAS BARRAS DE PROGRESO.
	void info_progreso(const std_msgs::String::ConstPtr& str);

	//MOD BOTÓN DE SALIDA DE PROGRAMA
	//void manejadorBotonSalida();

	/*FIN MOD*/

	// Here we declare some internal slots.
protected Q_SLOTS:

	// Then we finish up with protected member variables.
protected:

	//Declaración de los NodeHandlers de ROS.
	ros::NodeHandle nh_topic, nh_sub;
	ros::NodeHandle nh1, nhMapeo, nhExploracion, nhTeleop, nhCancelTeleop, nh_salir;
	ros::Publisher pub_topic;
	ros::Subscriber sub_topic;

	ros::ServiceClient client1, clientMapeo, clientExploracion, clientTeleop, clientCancelTeleop,
			client_salir;

	std_srvs::Trigger service;


	ros::ServiceServer serverMsgMapeo;
	ros::NodeHandle srvMsgMapeo;

	// The latest velocity values from the drive widget.
	float linear_velocity_;
	float angular_velocity_;

	/*MOD*/
	QPushButton* boton1;
	QPushButton* boton2;
	QPushButton* boton3;
	QPushButton* boton4;
	QPushButton* boton5;
	QPushButton* boton5_1;

	QPushButton* pushButton_4;

	QProgressBar* progressBar;
	QProgressBar* bar2;
	QProgressBar* bar3;
	QProgressBar* bar4;

	QGridLayout *gridLayout;

	QWidget *centralWidget;
	QWidget *gridLayoutWidget;
	QGroupBox *groupBox;
	QWidget *horizontalLayoutWidget;
	QHBoxLayout *horizontalLayout;
	QSpacerItem *horizontalSpacer;
	QGroupBox *groupBox_2;
	QWidget *gridLayoutWidget_3;
	QGridLayout *gridLayout_3;
	QSpacerItem *horizontalSpacer_4;
	QSpacerItem *horizontalSpacer_5;
	QGroupBox *groupBox_3;
	QWidget *gridLayoutWidget_2;
	QGridLayout *gridLayout_2;
	QSpacerItem *horizontalSpacer_2;
	QSpacerItem *horizontalSpacer_3;
	QSpacerItem *verticalSpacer_2;
	QTextBrowser *textBrowser;
	QSpacerItem *verticalSpacer;
	QSpacerItem *horizontalSpacer_6;
	QSpacerItem *verticalSpacer_3;
	QSpacerItem *horizontalSpacer_7;
	QMenuBar *menuBar;
	QToolBar *mainToolBar;
	QStatusBar *statusBar;

	QGroupBox *groupBox2;
	QGroupBox *groupBox3;
	QGroupBox *groupBox4;
	QGroupBox *groupBox5;

    QSpacerItem *verticalSpacer_5;
    QLabel *label;

	//MOD BOTÓN DE SALIDA DE PROGRAMA
	QPushButton* boton_salida;

	/*FIN MOD*/

	// END_TUTORIAL
};

} // end namespace rviz_plugin_tutorials

#endif // PANEL_MAPEO_H
