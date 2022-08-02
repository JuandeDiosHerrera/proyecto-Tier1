
#ifndef PANEL_GUIADO_H
#define PANEL_GUIADO_H

#ifndef Q_MOC_RUN

#include <boost/algorithm/string.hpp>

#include <QApplication>
#include <QGroupBox>
#include <QLabel>
#include <QLineEdit>
#include <QProgressBar>
#include <QPushButton>
#include <QTextBrowser>
#include <QVBoxLayout>

#include "programa_central/mensajes.h"
#include "etapa_guiado/Productos.h"
#include <ros/ros.h>
#include <rviz/panel.h>
#include "std_msgs/String.h"
#include <std_srvs/Trigger.h>

#endif

class QLineEdit;

namespace rviz_plugin_tutorials
{

class DriveWidget;

class PanelGuiado: public rviz::Panel
{
	Q_OBJECT
public:
	PanelGuiado(QWidget* parent = 0);

	virtual void load(const rviz::Config& config);
	virtual void save(rviz::Config config) const;

	bool afs;

public Q_SLOTS:

	void manejadorBotonInicio();
	void manejadorBotonObjetivos();
	void manejadorBotonGuiado();

	bool recibeMensajesGuiado(programa_central::mensajes::Request &req, programa_central::mensajes::Response &res);
	void imprimeInstrucciones();

	std::string recibeProductosLista();
	std::vector<std::string> separaElementos(std::string listaProductos);
	std::vector<std::string> limpiaLista(std::vector<std::string> listaSeparada);

	//FUNCIÓN QUE CONTROLA LAS BARRAS DE PROGRESO.
	void info_progreso(const std_msgs::String::ConstPtr& str);

protected Q_SLOTS:

protected:

	//Declaración de los NodeHandlers de ROS.
	ros::NodeHandle nh_topic, nhProgreso;
	ros::NodeHandle nhGuiado;
	ros::Subscriber topicProgreso;

	ros::ServiceClient clientGuiado;

	std_srvs::Trigger service;

	ros::ServiceServer serverMsgGuiado;
	ros::NodeHandle srvMsgGuiado;

	ros::NodeHandle nhLista, nhProductos;
	ros::ServiceClient clienteLista, clienteProductos;
	etapa_guiado::Productos servicioProductos;
	std_srvs::Trigger servicioLista;

	char* userHome;

	QPushButton *botonInicio;
	QPushButton *botonEnviarObjetivos;
	QPushButton *botonGuiado;

	QGroupBox *groupBoxGuiado;
	QGroupBox *groupBoxLista;

	QSpacerItem *verticalSpacer;
	QSpacerItem *verticalSpacer_2;
	QSpacerItem *verticalSpacer_3;
	QSpacerItem *verticalSpacer_4;
	QSpacerItem *verticalSpacer_5;

	QSpacerItem *horizontalSpacer;
	QSpacerItem *horizontalSpacer_2;
	QSpacerItem *horizontalSpacer_3;
	QSpacerItem *horizontalSpacer_4;
	QSpacerItem *horizontalSpacer_5;
	QSpacerItem *horizontalSpacer_6;

	QWidget *centralWidget;
	QWidget *gridLayoutWidget;
	QGridLayout *gridLayout;

	QWidget *horizontalLayoutWidget;
	QHBoxLayout *horizontalLayout;
	QWidget *horizontalLayoutWidget_2;
	QHBoxLayout *horizontalLayout_2;

	QLabel *label;
	QProgressBar *progressBar;
	QLineEdit *lineEdit;
	QTextBrowser *textBrowser;

};

} // fin namespace

#endif // PANEL_GUIADO_H
