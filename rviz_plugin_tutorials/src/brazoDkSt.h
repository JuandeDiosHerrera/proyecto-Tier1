
#ifndef PANEL_CARGA_H
#define PANEL_CARGA_H

#ifndef Q_MOC_RUN

#include <QApplication>
#include <QGroupBox>
#include <QLabel>
#include <QProgressBar>
#include <QPushButton>
#include <QTextBrowser>
#include <QVBoxLayout>

#include <diagnostic_msgs/DiagnosticArray.h>
#include <ros/ros.h>
#include <rviz/panel.h>
#include <smart_battery_msgs/SmartBatteryStatus.h>
#include <std_srvs/Trigger.h>

#include "programa_central/mensajes.h"

#endif

namespace rviz_plugin_tutorials
{

class PanelBrazo: public rviz::Panel
{
	Q_OBJECT

public:
	PanelBrazo(QWidget* parent = 0);

	virtual void load(const rviz::Config& config);
	virtual void save(rviz::Config config) const;

	bool recibeMensajesBrazo(programa_central::mensajes::Request &req, programa_central::mensajes::Response &res);

	bool afs;

	// Next come a couple of public Qt slots.
public Q_SLOTS:

	void manejadorBotonMov1();
	void manejadorBotonMov2();
	void manejadorBotonMov3();
	void manejadorBotonMov4();

	void imprimeInstrucciones();

	// Here we declare some internal slots.
protected Q_SLOTS:

	// Then we finish up with protected member variables.
protected:

	//Control de batería del turtlebot y del portátil
	ros::NodeHandle cbTurtle, cbPortatil;
	ros::Subscriber batTurtlebot;
	ros::Subscriber batPortatil;
	float nivelTurtlebot;
	int nivelPortatil;

	std_srvs::Trigger service;

	ros::ServiceServer serverBrazo;
	ros::NodeHandle srvBrazo;

	ros::NodeHandle nhLista, nhProductos;
	ros::ServiceClient clienteLista, clienteProductos;
	std_srvs::Trigger servicioLista;

    QPushButton *botonMov1;
    QPushButton *botonMov2;
    QPushButton *botonMov3;
    QPushButton *botonMov4;

	QGroupBox *groupBoxMovs1;
	QGroupBox *groupBoxMovs2;

	QWidget *centralWidget;

	QWidget *gridLayoutWidget;
	QGridLayout *gridLayout;

	QWidget *horizontalLayoutWidget_1;
	QHBoxLayout *horizontalLayout_1;
	QWidget *horizontalLayoutWidget_2;
	QHBoxLayout *horizontalLayout_2;

	QSpacerItem *horizontalSpacer;
	QSpacerItem *horizontalSpacer_1;
	QSpacerItem *horizontalSpacer_2;
	QSpacerItem *horizontalSpacer_2_0;
	QSpacerItem *horizontalSpacer_3;
	QSpacerItem *horizontalSpacer_4;
	QSpacerItem *horizontalSpacer_5;
	QSpacerItem *horizontalSpacer_6;

	QSpacerItem *verticalSpacer;
	QSpacerItem *verticalSpacer_2;
	QSpacerItem *verticalSpacer_3;
	QSpacerItem *verticalSpacer_4;
	QSpacerItem *verticalSpacer_5;

	QLabel *label;
	QTextBrowser *textBrowser;

	char* userHome;
};

} // fin namespace

#endif // PANEL_CARGA_H
