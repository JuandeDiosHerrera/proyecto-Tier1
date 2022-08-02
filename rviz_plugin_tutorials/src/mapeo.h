
#ifndef PANEL_MAPEO_H
#define PANEL_MAPEO_H

#ifndef Q_MOC_RUN

#include <fstream>

#include "programa_central/mensajes.h"

//FICHEROS DE CABECERA DE QT
#include <QApplication>
#include <QGroupBox>
#include <QLabel>
#include <QProgressBar>
#include <QPushButton>
#include <QTextBrowser>
//Por la siguiente línea funcionan los spacers y los layouts.
//Si se comenta, da errores en la compilación.
#include <QVBoxLayout>

//FICHEROS DE CABECERA DE ROS
#include <ros/ros.h>
#include <rviz/panel.h>
#include "std_msgs/String.h"
#include <std_srvs/Trigger.h>

#endif

namespace rviz_plugin_tutorials
{


class PanelMapeo: public rviz::Panel
{
	Q_OBJECT

public:

	PanelMapeo(QWidget* parent = 0);

	virtual void load(const rviz::Config& config);
	virtual void save(rviz::Config config) const;

	bool afs;

//SLOTS QT PÚBLICOS.
public Q_SLOTS:

	//DECLARACIÓN DE LOS MANEJADORES DE CADA BOTÓN
	void manejadorbotonInicio();
	void manejadorbotonExplorar();
	void manejadorbotonTeleop();
	void manejadorbotonCancelExp();
	void manejadorbotonCancelTeleop();

	//DECLARACIÓN DE FUNCIÓN QUE RECIBE MENSAJES DE OTROS NODOS
	bool recibeMensajesMapeo(programa_central::mensajes::Request &req, programa_central::mensajes::Response &res);

	//DECLARACIÓN DE FUNCIÓN QUE IMPRIME INSTRUCCIONES EN EL MOSTRADOR DE TEXTO
	void imprimeInstrucciones();

	//DECLARACIÓN DE FUNCIÓN QUE CONTROLA LAS BARRAS DE PROGRESO.
	void info_progreso(const std_msgs::String::ConstPtr& str);

//SLOTS QT INTERNOS.
protected Q_SLOTS:

//VARIABLES PROTEGIDAS.
protected:

	//DECLARACIÓN DE LOS NODEHANDLERS DE ROS.
	ros::NodeHandle nhMapeo, nhExploracion, nhTeleop, nhCancelTeleop, nh_CancelExplora;
	ros::NodeHandle nhProgreso;
	ros::Subscriber topicProgreso;

	//DECLARACIÓN DE LOS ELEMENTOS PARA LOS SERVICIOS
	std_srvs::Trigger service;
	ros::ServiceClient clientMapeo, clientExploracion, clientTeleop, clientCancelTeleop, clientCancelExplora;
	ros::ServiceServer serverMsgMapeo;
	ros::NodeHandle srvMsgMapeo;

	//DECLARACIÓN DE LA VARIABLE QUE CONTENDRÁ LA DIRECCIÓN $HOME DEL USUARIO
    char* userHome;

    //DECLARACIÓN DE BOTONES
	QPushButton* botonInicio;
	QPushButton* botonExplorar;
	QPushButton* botonTeleop;
	QPushButton* botonCancelExp;
	QPushButton* botonCancelTeleop;

	//DECLARACIÓN DE LAS CAJAS DE GRUPO
	QGroupBox *groupBoxMapeo;
	QGroupBox *groupBoxExploracion;
	QGroupBox *groupBoxTeleop;

	//DECLARACIÓN DE LOS LAYOUT DE CELDAS
	QWidget *gridLayoutWidget;
	QGridLayout *gridLayout;
	QWidget *gridLayoutWidget_2;
	QGridLayout *gridLayout_2;
	QWidget *gridLayoutWidget_3;
	QGridLayout *gridLayout_3;

	//DECLARACIÓN DE LOS LAYOUT HORIZONTALES
	QHBoxLayout *horizontalLayout;
	QWidget *horizontalLayoutWidget;

	//DECLARACIÓN DE LOS ELEMENTOS DE ESPACIADO HORIZONTALES
	QSpacerItem *horizontalSpacer;
	QSpacerItem *horizontalSpacer_2;
	QSpacerItem *horizontalSpacer_3;
	QSpacerItem *horizontalSpacer_4;
	QSpacerItem *horizontalSpacer_5;
	QSpacerItem *horizontalSpacer_6;
	QSpacerItem *horizontalSpacer_7;

	//DECLARACIÓN DE LOS ELEMENTOS DE ESPACIADO VERTICALES
	QSpacerItem *verticalSpacer;
	QSpacerItem *verticalSpacer_2;
	QSpacerItem *verticalSpacer_3;
	QSpacerItem *verticalSpacer_5;

	//DECLARACIÓN DE ETIQUETA, BARRA DE PROGRESO, MOSTRADOR DE TEXTO Y WIDGET PRINCIPAL
	QLabel *label;
	QProgressBar* progressBar;
	QTextBrowser *textBrowser;
	QWidget *centralWidget;
};
} //fin de namespace rviz_plugin_tutorials

#endif //PANEL_MAPEO_H
