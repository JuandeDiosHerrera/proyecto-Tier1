
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

class PanelCarga: public rviz::Panel
{
	Q_OBJECT

public:
	PanelCarga(QWidget* parent = 0);

	virtual void load(const rviz::Config& config);
	virtual void save(rviz::Config config) const;

	bool afs;

	// Next come a couple of public Qt slots.
public Q_SLOTS:

	void manejadorBotonCarga();
	void manejadorBotonSalir();

	void imprimeInstrucciones();

	void obtenerBateriaTurtlebot(const diagnostic_msgs::DiagnosticArray::ConstPtr& diagnostico);
	void obtenerBateriaPortatil(const smart_battery_msgs::SmartBatteryStatus::ConstPtr& diagnostico);

	bool recibeMensajesCarga(programa_central::mensajes::Request &req, programa_central::mensajes::Response &res);

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

	ros::ServiceServer serverCarga;
	ros::NodeHandle srvCarga;

	ros::NodeHandle nhLista, nhProductos;
	ros::ServiceClient clienteLista, clienteProductos;
	std_srvs::Trigger servicioLista;

    QPushButton *botonCargar;
    QPushButton *botonSalir;

	QGroupBox *groupBoxBaterias;
	QGroupBox *groupBoxTurtlebot;
	QGroupBox *groupBoxPortatil;
	QGroupBox *groupBoxOrdenes;

	QProgressBar *bateriaPortatil;
	QProgressBar *bateriaTurtlebot;

	QWidget *centralWidget;

	QWidget *gridLayoutWidget;
	QGridLayout *gridLayout;

	QWidget *horizontalLayoutWidget_main;
	QHBoxLayout *horizontalLayout_main;
	QWidget *horizontalLayoutWidget;
	QHBoxLayout *horizontalLayout;
	QWidget *horizontalLayoutWidget_1;
	QHBoxLayout *horizontalLayout_1;
	QWidget *horizontalLayoutWidget_2;
	QHBoxLayout *horizontalLayout_2;

	QSpacerItem *horizontalSpacer;
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
