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

#include <iostream>

#include "localizacion.h"

namespace rviz_plugin_tutorials
{

using namespace std;
// We start with the constructor, doing the standard Qt thing of
// passing the optional *parent* argument on to the superclass
// constructor.
PanelLocalizacion::PanelLocalizacion(QWidget* parent) :
		rviz::Panel(parent), linear_velocity_(0), angular_velocity_(0)
{
	/*MOD*/

//	boton1 = new QPushButton("Arrancar Turtlebot", this);
//	boton1->setMaximumWidth(150);
//	boton1->setMaximumHeight(35);
	botonAutoLoc = new QPushButton("Iniciar", this);
//	botonAutoLoc->setMaximumWidth(150);
//	botonAutoLoc->setMaximumHeight(35);
	botonAutoLoc->setToolTip(
			"Se cargan los programas encargados de localizar productos en el mapa.");
//	botonAutoLoc->setCursor(QCursor(Qt::PointingHandCursor));

	botonLocProductos = new QPushButton("Enviar", this);
//	botonLocProductos->setMaximumWidth(160);
//	botonLocProductos->setMaximumHeight(35);
	botonLocProductos->setToolTip(
			"Se realiza la localizacion de los productos en el mapa.");
//	botonLocProductos->setCursor(QCursor(Qt::PointingHandCursor));

	botonTeleop = new QPushButton("Teleoperar", this);
//	botonTeleop->setMaximumWidth(100);
//	botonTeleop->setMaximumHeight(35);
	botonTeleop->setToolTip(
			"Control manual del robot.");
//	botonTeleop->setCursor(QCursor(Qt::PointingHandCursor));

//	boton5 = new QPushButton("Cancelar", this);
//	boton5->setMaximumWidth(100);
//	boton5->setMaximumHeight(35);
//	boton5->setToolTip("Control manual del robot");
//	boton5->setCursor(QCursor(Qt::PointingHandCursor));

	botonCancelTeleop = new QPushButton("Cancelar", this);
//	botonCancelTeleop->setMaximumWidth(100);
//	botonCancelTeleop->setMaximumHeight(35);
	botonCancelTeleop->setToolTip("Cancela el control manual.");
//	botonCancelTeleop->setCursor(QCursor(Qt::PointingHandCursor));

//MOD BOTÓN DE SALIDA DE PROGRAMA
//	boton_salida = new QPushButton("Salir", this);
//	boton_salida->setMaximumWidth(150);
//	boton_salida->setMaximumHeight(35);
//	boton_salida->setToolTip("Salir del programa");
//	boton_salida->setCursor(QCursor(Qt::PointingHandCursor));

//	centralWidget = new QWidget();
//	        gridLayoutWidget = new QWidget(centralWidget);
//	        gridLayoutWidget->setGeometry(QRect(10, 30, 411, 411));
//	        gridLayout = new QGridLayout(gridLayoutWidget);
//	        gridLayout->setSpacing(6);
//	        gridLayout->setContentsMargins(11, 11, 11, 11);
//	        gridLayout->setSizeConstraint(QLayout::SetDefaultConstraint);
//	        gridLayout->setHorizontalSpacing(0);
//	        gridLayout->setVerticalSpacing(10);
//	        gridLayout->setContentsMargins(0, 5, 0, 5);
//	        //boton5 = new QPushButton(gridLayoutWidget);
//	        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
//	        sizePolicy.setHorizontalStretch(0);
//	        sizePolicy.setVerticalStretch(0);
//	        sizePolicy.setHeightForWidth(boton5->sizePolicy().hasHeightForWidth());
//	        boton5->setSizePolicy(sizePolicy);
//
//	        gridLayout->addWidget(boton5, 2, 1, 1, 1);
//
//	       // botonTeleop = new QPushButton(gridLayoutWidget);
//	        sizePolicy.setHeightForWidth(botonTeleop->sizePolicy().hasHeightForWidth());
//	        botonTeleop->setSizePolicy(sizePolicy);
//	        botonTeleop->setLayoutDirection(Qt::LeftToRight);
//
//	        gridLayout->addWidget(botonTeleop, 1, 3, 1, 1);
//
//	        //botonLocProductos = new QPushButton(gridLayoutWidget);
//	        sizePolicy.setHeightForWidth(botonLocProductos->sizePolicy().hasHeightForWidth());
//	        botonLocProductos->setSizePolicy(sizePolicy);
//
//	        gridLayout->addWidget(botonLocProductos, 1, 1, 1, 1);
//
//	        //botonCancelTeleop = new QPushButton(gridLayoutWidget);
//	        sizePolicy.setHeightForWidth(botonCancelTeleop->sizePolicy().hasHeightForWidth());
//	        botonCancelTeleop->setSizePolicy(sizePolicy);
//
//	        gridLayout->addWidget(botonCancelTeleop, 2, 3, 1, 1);
//
//	        textBrowser = new QTextBrowser(gridLayoutWidget);
//	        sizePolicy.setHeightForWidth(textBrowser->sizePolicy().hasHeightForWidth());
//	        textBrowser->setSizePolicy(sizePolicy);
//
//	        gridLayout->addWidget(textBrowser, 4, 0, 1, 5);
//
//	        progressBar = new QProgressBar(gridLayoutWidget);
//	        sizePolicy.setHeightForWidth(progressBar->sizePolicy().hasHeightForWidth());
//	        progressBar->setSizePolicy(sizePolicy);
//	        progressBar->setValue(24);
//
//	        gridLayout->addWidget(progressBar, 0, 3, 1, 1);
//
//	        //botonAutoLoc = new QPushButton(gridLayoutWidget);
//	        QSizePolicy sizePolicy1(QSizePolicy::Preferred, QSizePolicy::Preferred);
//	        sizePolicy1.setHorizontalStretch(0);
//	        sizePolicy1.setVerticalStretch(1);
//	        sizePolicy1.setHeightForWidth(botonAutoLoc->sizePolicy().hasHeightForWidth());
//	        botonAutoLoc->setSizePolicy(sizePolicy1);
//	        QPalette palette;
//	        QBrush brush(QColor(255, 0, 0, 255));
//	        brush.setStyle(Qt::SolidPattern);
//	        palette.setBrush(QPalette::Active, QPalette::Button, brush);
//	        palette.setBrush(QPalette::Inactive, QPalette::Button, brush);
//	        palette.setBrush(QPalette::Disabled, QPalette::Button, brush);
//	        botonAutoLoc->setPalette(palette);
//	        botonAutoLoc->setLayoutDirection(Qt::LeftToRight);
//
//	        gridLayout->addWidget(botonAutoLoc, 0, 1, 1, 1);
//
//	        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
//
//	        gridLayout->addItem(horizontalSpacer, 0, 0, 1, 1);
//
//	        horizontalSpacer_3 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
//
//	        gridLayout->addItem(horizontalSpacer_3, 0, 4, 1, 1);
//
//	        horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
//
//	        gridLayout->addItem(horizontalSpacer_2, 0, 2, 1, 1);
//
//	        verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);
//
//	        gridLayout->addItem(verticalSpacer, 3, 2, 1, 1);
//
//	        gridLayout->setRowStretch(0, 1);
//	        gridLayout->setRowStretch(1, 1);
//	        gridLayout->setRowStretch(2, 1);
//	        gridLayout->setRowStretch(3, 5);
//	        gridLayout->setRowStretch(4, 50);
//	        gridLayout->setColumnStretch(0, 3);
//	        gridLayout->setColumnStretch(1, 4);
//	        gridLayout->setColumnStretch(3, 4);
//	        gridLayout->setColumnStretch(4, 3);
//	        pushButton_4 = new QPushButton(centralWidget);
//	        pushButton_4->setGeometry(QRect(160, 0, 99, 27));

	centralWidget = new QWidget();
	gridLayoutWidget = new QWidget(centralWidget);
	gridLayoutWidget->setGeometry(QRect(40, 10, 351, 431));
	gridLayout = new QGridLayout(gridLayoutWidget);
	gridLayout->setSpacing(6);
	gridLayout->setContentsMargins(11, 11, 11, 11);
	gridLayout->setContentsMargins(0, 0, 0, 0);
	groupBox = new QGroupBox(gridLayoutWidget);
	groupBox->setMaximumSize(QSize(300, 100));
	groupBox->setStyleSheet(QLatin1String("			QGroupBox\n"
			"			 {\n"
			"			border: 0.5px solid gray;\n"
			"			border-radius: 2px;\n"
			"			margin-top: 0.5em;\n"
			"			}\n"
			"			QGroupBox::Title\n"
			"			{\n"
			"			subcontrol-origin: margin;\n"
			"			left: 10px;\n"
			"			padding: 0 3px 0 3px;\n"
			"			}"));
	groupBox->setTitle(
				QApplication::translate("MapPanel", "Localizacion productos", 0));
	horizontalLayoutWidget = new QWidget(groupBox);
	horizontalLayoutWidget->setGeometry(QRect(10, 20, 271, 51));
	horizontalLayout = new QHBoxLayout(horizontalLayoutWidget);
	horizontalLayout->setSpacing(6);
	horizontalLayout->setContentsMargins(11, 11, 11, 11);
	horizontalLayout->setContentsMargins(0, 0, 0, 0);

	horizontalLayout->addWidget(botonAutoLoc);

	horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding,
			QSizePolicy::Minimum);

	horizontalLayout->addItem(horizontalSpacer);

	progressBar = new QProgressBar(horizontalLayoutWidget);
	progressBar->setValue(0);

	horizontalLayout->addWidget(progressBar);

	horizontalLayout->setStretch(0, 5);
	horizontalLayout->setStretch(1, 1);
	horizontalLayout->setStretch(2, 10);

	gridLayout->addWidget(groupBox, 1, 1, 1, 2);

	groupBox_2 = new QGroupBox(gridLayoutWidget);
	groupBox_2->setMaximumSize(QSize(250, 120));
	groupBox_2->setStyleSheet(QLatin1String("	QGroupBox\n"
			"			 {\n"
			"			border: 0.5px solid gray;\n"
			"			border-radius: 2px;\n"
			"			margin-top: 0.5em;\n"
			"			}\n"
			"			QGroupBox::Title\n"
			"			{\n"
			"			subcontrol-origin: margin;\n"
			"			left: 10px;\n"
			"			padding: 0 3px 0 3px;\n"
			"			}"));
	groupBox_2->setTitle(
					QApplication::translate("MapPanel", "Obtener objetivos", 0));
	gridLayoutWidget_3 = new QWidget(groupBox_2);
	gridLayoutWidget_3->setGeometry(QRect(10, 20, 131, 80));
	gridLayout_3 = new QGridLayout(gridLayoutWidget_3);
	gridLayout_3->setSpacing(6);
	gridLayout_3->setContentsMargins(11, 11, 11, 11);
	gridLayout_3->setContentsMargins(0, 0, 0, 0);
	horizontalSpacer_4 = new QSpacerItem(40, 20, QSizePolicy::Expanding,
			QSizePolicy::Minimum);

	gridLayout_3->addItem(horizontalSpacer_4, 0, 0, 1, 1);

//	gridLayout_3->addWidget(boton5, 1, 1, 1, 1);

	gridLayout_3->addWidget(botonLocProductos, 0, 1, 1, 1);

	horizontalSpacer_5 = new QSpacerItem(40, 20, QSizePolicy::Expanding,
			QSizePolicy::Minimum);

	gridLayout_3->addItem(horizontalSpacer_5, 0, 2, 1, 1);

	groupBox->raise();
	groupBox->raise();
	groupBox->raise();
	gridLayoutWidget_3->raise();

	gridLayout->addWidget(groupBox_2, 3, 1, 1, 1);

	groupBox_3 = new QGroupBox(gridLayoutWidget);
	groupBox_3->setMaximumSize(QSize(250, 120));
	groupBox_3->setLayoutDirection(Qt::LeftToRight);
	groupBox_3->setAutoFillBackground(false);
	groupBox_3->setStyleSheet(QLatin1String("	QGroupBox\n"
			"			 {\n"
			"			border: 0.5px solid gray;\n"
			"			border-radius: 2px;\n"
			"			margin-top: 0.5em;\n"
			"			}\n"
			"			QGroupBox::Title\n"
			"			{\n"
			"			subcontrol-origin: margin;\n"
			"			left: 10px;\n"
			"			padding: 0 3px 0 3px;\n"
			"			}"));
	groupBox_3->setTitle(
					QApplication::translate("MapPanel", "Teleoperacion", 0));
	groupBox_3->setInputMethodHints(Qt::ImhNone);
	groupBox_3->setAlignment(Qt::AlignCenter);
	gridLayoutWidget_2 = new QWidget(groupBox_3);
	gridLayoutWidget_2->setGeometry(QRect(10, 20, 131, 80));
	gridLayout_2 = new QGridLayout(gridLayoutWidget_2);
	gridLayout_2->setSpacing(6);
	gridLayout_2->setContentsMargins(11, 11, 11, 11);
	gridLayout_2->setContentsMargins(0, 0, 0, 0);

	gridLayout_2->addWidget(botonCancelTeleop, 1, 1, 1, 1);

	horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding,
			QSizePolicy::Minimum);

	gridLayout_2->addItem(horizontalSpacer_2, 0, 0, 2, 1);

	gridLayout_2->addWidget(botonTeleop, 0, 1, 1, 1);

	horizontalSpacer_3 = new QSpacerItem(40, 20, QSizePolicy::Expanding,
			QSizePolicy::Minimum);

	gridLayout_2->addItem(horizontalSpacer_3, 0, 2, 2, 1);

	gridLayout->addWidget(groupBox_3, 3, 2, 1, 1);

	verticalSpacer_2 = new QSpacerItem(20, 40, QSizePolicy::Minimum,
			QSizePolicy::Expanding);

	gridLayout->addItem(verticalSpacer_2, 4, 1, 1, 2);

	textBrowser = new QTextBrowser(gridLayoutWidget);

	//MOD 02/10/16 PARA CAMBIAR COLOR DE LETRA Y FONDO
	textBrowser->setObjectName("textBrowser");
	textBrowser->setAccessibleName("textBrowser");
	textBrowser->setAlignment(Qt::AlignJustify);
	textBrowser->setStyleSheet("#textBrowser {color: rgb(255,255,255); background-color: rgb(0,90,195);}");


	gridLayout->addWidget(textBrowser, 5, 1, 1, 2);

	verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum,
			QSizePolicy::Expanding);

	gridLayout->addItem(verticalSpacer, 2, 1, 1, 2);

	horizontalSpacer_6 = new QSpacerItem(40, 20, QSizePolicy::Expanding,
			QSizePolicy::Minimum);

	gridLayout->addItem(horizontalSpacer_6, 0, 0, 6, 1);

	verticalSpacer_3 = new QSpacerItem(20, 40, QSizePolicy::Minimum,
			QSizePolicy::Expanding);

	gridLayout->addItem(verticalSpacer_3, 0, 1, 1, 2);

	horizontalSpacer_7 = new QSpacerItem(40, 20, QSizePolicy::Expanding,
			QSizePolicy::Minimum);

	gridLayout->addItem(horizontalSpacer_7, 0, 3, 6, 1);

	gridLayout->setRowStretch(0, 1);
	gridLayout->setRowStretch(1, 10); //5
	gridLayout->setRowStretch(2, 1); //2
	gridLayout->setRowStretch(3, 12); //7
	gridLayout->setRowStretch(4, 2); //3
	gridLayout->setRowStretch(5, 15); //10
	gridLayout->setColumnStretch(0, 1);
	gridLayout->setColumnStretch(1, 10);
	gridLayout->setColumnStretch(2, 10);
	gridLayout->setColumnStretch(3, 1);

	setLayout(gridLayout);

//	textBrowser->append("Hola");
//	textBrowser->append("Que tal.");

	//MOD2
	pub_topic = nh_topic.advertise < std_msgs::String
			> ("interface_central_comm", 20, true);
	sub_topic = nh_sub.subscribe("central_node_comm", 1000,
			&PanelLocalizacion::info_progreso, this);

//	client1 = nh1.serviceClient<std_srvs::Trigger>("arranca_etapa_1");
	clientAutoLoc = nhAutoLoc.serviceClient<std_srvs::Trigger>("autolocalizacion_locProductos");
	clientLocProductos = nhLocProductos.serviceClient<std_srvs::Trigger>("recibir_objetivos");
	clientTeleop = nhTeleop.serviceClient<std_srvs::Trigger>("arranca_teleop");
//	client5 = nh5.serviceClient<std_srvs::Trigger>("arranca_teleop");
	clientCancelTeleop = nhCancelTeleop.serviceClient<std_srvs::Trigger>("cancela_teleop");
//	client_salir = nh_salir.serviceClient<std_srvs::Trigger>("cierra_programa");



	serverMsgLocProd = srvMsgLocProd.advertiseService("recibe_mensajes_locProductos", &PanelLocalizacion::recibeMensajesLocProd, this);

	// Create a timer for sending the output.  Motor controllers want to
	// be reassured frequently that they are doing the right thing, so
	// we keep re-sending velocities even when they aren't changing.
	//
	// Here we take advantage of QObject's memory management behavior:
	// since "this" is passed to the new QTimer as its parent, the
	// QTimer is deleted by the QObject destructor when this PanelLocalizacion
	// object is destroyed.  Therefore we don't need to keep a pointer
	// to the timer.
	QTimer* output_timer = new QTimer(this);

	// Next we make signal/slot connections.
	//connect( drive_widget_, SIGNAL( outputVelocity( float, float )), this, SLOT( setVel( float, float )));
//	connect(output_topic_editor_, SIGNAL(editingFinished()), this,
//			SLOT(updateTopic()));
//	connect(output_timer, SIGNAL(timeout()), this, SLOT(sendVel()));

	/*MOD*/
//	connect(boton1, SIGNAL(clicked()/*released()*/), this,
//			SLOT(manejadorBoton1()));
	connect(botonAutoLoc, SIGNAL(clicked()), this, SLOT(manejadorbotonAutoLoc()));
	connect(botonLocProductos, SIGNAL(clicked()), this, SLOT(manejadorbotonLocProductos()));
	connect(botonTeleop, SIGNAL(clicked()), this, SLOT(manejadorbotonTeleop()));
	//connect(boton5, SIGNAL(clicked()), this, SLOT(manejadorBoton5()));
	connect(botonCancelTeleop, SIGNAL(clicked()), this, SLOT(manejadorbotonCancelTeleop()));
	/*FIN MOD*/

	//MOD BOTÓN DE SALIDA DE PROGRAMA
//	connect(boton_salida, SIGNAL(clicked()), this,
//			SLOT(manejadorBotonSalida()));
	// Start the timer.
	output_timer->start(100);

	// Make the control widget start disabled, since we don't start with an output topic.
//	drive_widget_->setEnabled(false);
}

//MOD BOTÓN DE SALIDA DE PROGRAMA
//void PanelLocalizacion::manejadorBotonSalida()
//{
//	//USANDO SERVICIOS
////	if (client_salir.call(service))
////		ROS_INFO("Llamada a salir realizada con exito.");
////	else
////		ROS_ERROR("Fallo al llamar al servicio cierra_programa.");
//
//	//EL PROPIO BOTÓN SE ENCARGA DE CERRAR EL PROGRAMA
//	ROS_INFO("Cerrando RVIZ y la red de ROS...");
//	system("rosnode kill /cierre_xterm");
//	system("rosnode kill /RVIZ");
//	system("rosnode kill /nodo_central");
//
//	//USANDO TOPICS
////	std_msgs::String mensaje;
////	ROS_INFO("Mandando mensaje de salida al nodo central");
////	mensaje.data = "salir";
////	pub_topic.publish(mensaje);
//}

void PanelLocalizacion::manejadorBoton1()
{
	//USANDO SERVICIOS
//	if (client1.call(service))
//		ROS_INFO("Llamada 1 realizada con exito.");
//	else
//		ROS_ERROR("Fallo al llamar al servicio arranca_etapa_1.");

	//USANDO TOPICS
//	std_msgs::String mensaje;
//	ROS_INFO("Mandando mensaje 1 al nodo central");
//	mensaje.data = "mensaje1";
//	pub_topic.publish(mensaje);
}

void PanelLocalizacion::manejadorbotonAutoLoc()
{
	//USANDO SERVICIOS
	if (clientAutoLoc.call(service))
		ROS_INFO("Llamada 2 realizada con exito.");
	else
		ROS_ERROR("Fallo al llamar al servicio autolocalizacion_locProductos.");

	//USANDO TOPICS
//	std_msgs::String mensaje;
//	ROS_INFO("Mandando mensaje 2 al nodo central");
//	mensaje.data = "mensaje2";
//	pub_topic.publish(mensaje);
}

void PanelLocalizacion::manejadorbotonLocProductos()
{
	//USANDO SERVICIOS

	//MOD 02/10/16
	textBrowser->clear();
	//textBrowser->append("Buscando productos...");

	if (clientLocProductos.call(service))
		ROS_INFO("Llamada a recibirObjetivos realizada con exito.");
	else
		ROS_ERROR("Fallo al llamar al servicio recibir_objetivos.");

	//USANDO TOPICS
//	std_msgs::String mensaje;
//	ROS_INFO("Mandando mensaje 3 al nodo central");
//	mensaje.data = "mensaje3";
//	pub_topic.publish(mensaje);
}

void PanelLocalizacion::manejadorbotonTeleop()
{
	//USANDO SERVICIOS
	if (clientTeleop.call(service))
		ROS_INFO("Llamada 4 realizada con exito.");
	else
		ROS_ERROR("Fallo al llamar al servicio arranca_teleop.");

	//USANDO TOPICS
//	std_msgs::String mensaje;
//	ROS_INFO("Mandando mensaje 4 al nodo central");
//	mensaje.data = "mensaje4";
//	pub_topic.publish(mensaje);
}

void PanelLocalizacion::manejadorBoton5()
{
	//USANDO SERVICIOS
	if (client5.call(service))
		ROS_INFO("Llamada 5 realizada con exito.");
	else
		ROS_ERROR("Fallo al llamar al servicio arranca_etapa_5.");

	//USANDO TOPICS
//	std_msgs::String mensaje;
//	ROS_INFO("Mandando mensaje 5 al nodo central");
//	mensaje.data = "mensaje5";
//	pub_topic.publish(mensaje);
}

void PanelLocalizacion::manejadorbotonCancelTeleop()
{
	//USANDO SERVICIOS
	if (clientCancelTeleop.call(service))
		ROS_INFO("Llamada 6 realizada con exito.");
	else
		ROS_ERROR("Fallo al llamar al servicio cancela_teleop.");

	//USANDO TOPICS
//	std_msgs::String mensaje;
//	ROS_INFO("Mandando mensaje 6 al nodo central");
//	mensaje.data = "mensaje6";
//	pub_topic.publish(mensaje);
}

// Save all configuration data from this panel to the given
// Config object.  It is important here that you call save()
// on the parent class so the class id and panel name get saved.
void PanelLocalizacion::save(rviz::Config config) const
{
	rviz::Panel::save(config);
}

// Load all configuration data for this panel from the given Config object.
void PanelLocalizacion::load(const rviz::Config& config)
{
	rviz::Panel::load(config);
}

//MÉTODO QUE MODIFICA EL VALOR DE LA BARRA DE PROGRESO
void PanelLocalizacion::info_progreso(const std_msgs::String::ConstPtr& str)
{
	if (strcmp(str->data.c_str(), "Progreso localizacion: Fase 0") == 0)
	{
		progressBar->setValue(22);
	}
	if (strcmp(str->data.c_str(), "Progreso localizacion: Fase 1") == 0)
	{
		progressBar->setValue(35);
	}
	if (strcmp(str->data.c_str(), "Progreso localizacion: Fase 2") == 0)
	{
		progressBar->setValue(87);
	}
	if (strcmp(str->data.c_str(), "Progreso localizacion: Fase 3") == 0)
	{
		progressBar->setValue(100);
	}
}


bool PanelLocalizacion::recibeMensajesLocProd(programa_central::mensajes::Request &req, programa_central::mensajes::Response &res)
{
	//cout << "Yo, panel mapeo, he recibido: " << req.mensaje << endl;
//	int i = 0;
//	for(i; i<50; i++)
	switch(req.cmd)
	{
		//Limpieza de pantalla
		case 0:
			textBrowser->clear();
			break;
		//Mensajes normales
		case 1:
			textBrowser->setTextColor(QColor(255,255,255,255));
			textBrowser->append(req.mensaje.c_str());
			break;
		//Instrucciones
		case 2:
			textBrowser->setTextColor(QColor(255,255,255,255));
			imprimeInstrucciones();
			break;
		//Errores
		case 3:
			textBrowser->setTextColor(QColor(255,0,0,255));
			textBrowser->append(req.mensaje.c_str());
			textBrowser->setTextColor(QColor(255,255,255,255));
			break;
		//Exitos
		case 4:
			textBrowser->setTextColor(QColor(0,255,0,255));
			textBrowser->append(req.mensaje.c_str());
			textBrowser->setTextColor(QColor(255,255,255,255));
			break;
	}
	return true;
}

void PanelLocalizacion::imprimeInstrucciones()
{
	textBrowser->append("INSTRUCCIONES");
	textBrowser->append("---------------------------------------------------------------------");
	textBrowser->append("Ahora puede enviar objetivos al robot. Para ello, siga los siguientes pasos:\n");
	textBrowser->append("1. Pulse el boton \"2D Nav Goal\" de la parte superior de la interfaz cada vez que quiera mandarle un objetivo al turtlebot.\n");
	textBrowser->append("2. Marque en el mapa los objetivos que quiere pasarle al turtlebot.\n");
	textBrowser->append("3. Una vez haya marcado todos los objetivos pulse el boton \"Enviar\" de \"Obtener Objetivos\".");
	textBrowser->append("---------------------------------------------------------------------\n");
}



//int main(int argc, char *argv[])
//{
//	ROS_INFO("Iniciando panel");
//	ros::init(argc, argv, "PanelLocalizacion"); //Le pasamos el nombre del nodo: panel
//	PanelLocalizacion panel;
//	ros::spin();
//	return 0;
//}

int main()
{
	ROS_INFO("Iniciando panel");
	PanelLocalizacion panel;
	ros::spin();
	return 0;
}

} // end namespace rviz_plugin_tutorials

// Tell pluginlib about this class.  Every class which should be
// loadable by pluginlib::ClassLoader must have these two lines
// compiled in its .cpp file, outside of any namespace scope.
#include <pluginlib/class_list_macros.h>
PLUGINLIB_EXPORT_CLASS(rviz_plugin_tutorials::PanelLocalizacion, rviz::Panel)
// END_TUTORIAL
