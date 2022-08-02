
#ifndef PANEL_LOCALIZACION_H
#define PANEL_LOCALIZACION_H

#ifndef Q_MOC_RUN

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

class PanelLocalizacion: public rviz::Panel
{
	Q_OBJECT
public:

	PanelLocalizacion(QWidget* parent = 0);

	virtual void load(const rviz::Config& config);
	virtual void save(rviz::Config config) const;

	bool afs;

//SLOTS QT PÚBLICOS.
public Q_SLOTS:

	//DECLARACIÓN DE LOS MANEJADORES DE CADA BOTÓN
	void manejadorbotonInicio();
	void manejadorbotonLocProductos();
	void manejadorbotonTeleop();
	void manejadorbotonCancelTeleop();

	//DECLARACIÓN DE FUNCIÓN QUE RECIBE MENSAJES DE OTROS NODOS
	bool recibeMensajesLocProd(programa_central::mensajes::Request &req, programa_central::mensajes::Response &res);

	//DECLARACIÓN DE FUNCIÓN QUE IMPRIME INSTRUCCIONES EN EL MOSTRADOR DE TEXTO
	void imprimeInstrucciones();

	//DECLARACIÓN DE FUNCIÓN QUE CONTROLA LAS BARRAS DE PROGRESO.
	void info_progreso(const std_msgs::String::ConstPtr& str);

//SLOTS QT INTERNOS.
protected Q_SLOTS:

//VARIABLES PROTEGIDAS.
protected:

	//DECLARACIÓN DE LOS NODEHANDLERS DE ROS.
	ros::NodeHandle nhAutoLoc, nhLocProductos, nhTeleop, nhCancelTeleop;
	ros::NodeHandle nhProgreso;
	ros::Subscriber topicProgreso;

	//DECLARACIÓN DE LOS ELEMENTOS PARA LOS SERVICIOS
	std_srvs::Trigger service;
	ros::ServiceClient clientAutoLoc, clientLocProductos, clientTeleop, clientCancelTeleop;
	ros::ServiceServer serverMsgLocProd;
	ros::NodeHandle srvMsgLocProd;

	//DECLARACIÓN DE LA VARIABLE QUE CONTENDRÁ LA DIRECCIÓN $HOME DEL USUARIO
	char* userHome;

	//DECLARACIÓN DE BOTONES
	QPushButton* botonInicio;
	QPushButton* botonLocProductos;
	QPushButton* botonTeleop;
	QPushButton* botonCancelTeleop;

	//DECLARACIÓN DE LAS CAJAS DE GRUPO
	QGroupBox *groupBoxLocProd;
	QGroupBox *groupBoxObjetivos;
	QGroupBox *groupBoxTeleop;

	//DECLARACIÓN DE LOS LAYOUT DE CELDAS (elementos de diseño y organización en celdas)
	QWidget *gridLayoutWidget;
	QGridLayout *gridLayout;
	QWidget *gridLayoutWidget_2;
	QGridLayout *gridLayout_2;
	QWidget *gridLayoutWidget_3;
	QGridLayout *gridLayout_3;

	//DECLARACIÓN DE LOS LAYOUT HORIZONTALES (elementos de diseño y organización de 1 fila y n columnas)
	QWidget *horizontalLayoutWidget;
	QHBoxLayout *horizontalLayout;

	//DECLARACIÓN DE LOS ELEMENTOS DE ESPACIADO HORIZONTALES
	QSpacerItem *horizontalSpacer;
	QSpacerItem *horizontalSpacer_2;
	QSpacerItem *horizontalSpacer_3;
	QSpacerItem *horizontalSpacer_4;
	QSpacerItem *horizontalSpacer_5;

	//DECLARACIÓN DE LOS ELEMENTOS DE ESPACIADO VERTICALES
	QSpacerItem *verticalSpacer;
	QSpacerItem *verticalSpacer_2;
	QSpacerItem *verticalSpacer_3;
	QSpacerItem *verticalSpacer_5;
	QSpacerItem *horizontalSpacer_6;
	QSpacerItem *horizontalSpacer_7;

	//DECLARACIÓN DE ETIQUETA, BARRA DE PROGRESO, MOSTRADOR DE TEXTO Y WIDGET PRINCIPAL
	QLabel *label;
	QProgressBar* progressBar;
	QTextBrowser *textBrowser;
	QWidget *centralWidget;

};

} //fin de namespace rviz_plugin_tutorials

#endif //PANEL_LOCALIZACION_H
