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

#include "mapeo.h"

using namespace std;

namespace rviz_plugin_tutorials
{

// We start with the constructor, doing the standard Qt thing of
// passing the optional *parent* argument on to the superclass
// constructor.
PanelMapeo::PanelMapeo(QWidget* parent) :
		rviz::Panel(parent), linear_velocity_(0), angular_velocity_(0)
{
	/*MOD*/

//	boton1 = new QPushButton("Arrancar Turtlebot", this);
//	boton1->setMaximumWidth(150);
//	boton1->setMaximumHeight(35);
	boton2 = new QPushButton("Inicio", this);
//	boton2->setMaximumWidth(150);
//	boton2->setMaximumHeight(35);
	boton2->setToolTip(
			"Se cargan los programas de mapeo y se realiza el mapeado inicial.");
//	boton2->setCursor(QCursor(Qt::PointingHandCursor));

	boton3 = new QPushButton("Explorar", this);
//	boton3->setMaximumWidth(160);
//	boton3->setMaximumHeight(35);
	boton3->setToolTip(
			"Se escanea la zona y se guarda el mapa en este ordenador.");
//	boton3->setCursor(QCursor(Qt::PointingHandCursor));

	boton4 = new QPushButton("Teleoperar", this);
//	boton4->setMaximumWidth(100);
//	boton4->setMaximumHeight(35);
	boton4->setToolTip(
			"Control manual del robot.");
//	boton4->setCursor(QCursor(Qt::PointingHandCursor));

	boton5 = new QPushButton("Cancelar", this);
//	boton5->setMaximumWidth(100);
//	boton5->setMaximumHeight(35);
	boton5->setToolTip("");
//	boton5->setCursor(QCursor(Qt::PointingHandCursor));

	boton5_1 = new QPushButton("Cancelar", this);
//	boton5_1->setMaximumWidth(100);
//	boton5_1->setMaximumHeight(35);
	boton5_1->setToolTip("Cancela el control manual.");
//	boton5_1->setCursor(QCursor(Qt::PointingHandCursor));

//MOD BOTÓN DE SALIDA DE PROGRAMA
//	boton_salida = new QPushButton("Salir", this);
//	boton_salida->setMaximumWidth(150);
//	boton_salida->setMaximumHeight(35);
//	boton_salida->setToolTip("Salir del programa");
//	boton_salida->setCursor(QCursor(Qt::PointingHandCursor));

	centralWidget = new QWidget();

    verticalLayoutWidget = new QWidget(centralWidget);
    verticalLayoutWidget->setGeometry(QRect(40, 10, 351, 481));

    verticalLayout = new QVBoxLayout(verticalLayoutWidget);
    verticalLayout->setSpacing(6);
    verticalLayout->setContentsMargins(11, 11, 11, 11);
    verticalLayout->setContentsMargins(0, 0, 0, 0);
    verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);
    verticalLayout->addItem(verticalSpacer);

    label = new QLabel(verticalLayoutWidget);
//    QSizePolicy sizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);
//    sizePolicy.setHorizontalStretch(0);
//    sizePolicy.setVerticalStretch(0);
//    sizePolicy.setHeightForWidth(label->sizePolicy().hasHeightForWidth());
//    label->setSizePolicy(sizePolicy);
    label->setPixmap(QPixmap(QString::fromUtf8("/home/adri/catkin_ws/src/rviz_plugin_tutorials/icons/classes/comerzzia_logo.png")));
    label->setAlignment(Qt::AlignCenter);
    verticalLayout->addWidget(label);

    verticalSpacer_2 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);
    verticalLayout->addItem(verticalSpacer_2);

    horizontalLayout_2 = new QHBoxLayout();
    horizontalLayout_2->setSpacing(6);
    horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
    horizontalLayout_2->addItem(horizontalSpacer_2);

    groupBox = new QGroupBox(verticalLayoutWidget);
    QSizePolicy sizePolicy1(QSizePolicy::Expanding, QSizePolicy::Fixed);
    sizePolicy1.setHorizontalStretch(0);
    sizePolicy1.setVerticalStretch(0);
    sizePolicy1.setHeightForWidth(groupBox->sizePolicy().hasHeightForWidth());
    groupBox->setSizePolicy(sizePolicy1);
//    groupBox->setMaximumSize(QSize(300, 100));
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
    				QApplication::translate("MapPanel", "Mapeado", 0));
    groupBox->setAlignment(Qt::AlignLeading|Qt::AlignLeft|Qt::AlignVCenter);
    horizontalLayoutWidget = new QWidget(groupBox);
    horizontalLayoutWidget->setGeometry(QRect(10, 20, 271, 51));
    horizontalLayout = new QHBoxLayout(horizontalLayoutWidget);
    horizontalLayout->setSpacing(6);
    horizontalLayout->setContentsMargins(11, 11, 11, 11);
    horizontalLayout->setContentsMargins(0, 0, 0, 0);

    horizontalLayout->addWidget(boton2);

    horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
    horizontalLayout->addItem(horizontalSpacer);

    progressBar = new QProgressBar(horizontalLayoutWidget);
    progressBar->setValue(0);
    horizontalLayout->addWidget(progressBar);

    horizontalLayout->setStretch(0, 5);
    horizontalLayout->setStretch(1, 1);
    horizontalLayout->setStretch(2, 10);

    horizontalLayout_2->addWidget(groupBox);

    horizontalSpacer_3 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
    horizontalLayout_2->addItem(horizontalSpacer_3);

    horizontalLayout_2->setStretch(0, 1);
    horizontalLayout_2->setStretch(1, 20);
    horizontalLayout_2->setStretch(2, 1);
    verticalLayout->addLayout(horizontalLayout_2);

    verticalSpacer_3 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);
    verticalLayout->addItem(verticalSpacer_3);

    horizontalLayout_3 = new QHBoxLayout();
    horizontalLayout_3->setSpacing(6);
    horizontalSpacer_4 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
    horizontalLayout_3->addItem(horizontalSpacer_4);

    groupBox_2 = new QGroupBox(verticalLayoutWidget);
    groupBox_2->setMaximumSize(QSize(250, 110));
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
					QApplication::translate("MapPanel", "Exploracion", 0));
    gridLayoutWidget_3 = new QWidget(groupBox_2);
    gridLayoutWidget_3->setGeometry(QRect(10, 20, 131, 80));
    gridLayout_3 = new QGridLayout(gridLayoutWidget_3);
    gridLayout_3->setSpacing(6);
    gridLayout_3->setContentsMargins(11, 11, 11, 11);
    gridLayout_3->setContentsMargins(0, 0, 0, 0);
    horizontalSpacer_6 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
    gridLayout_3->addItem(horizontalSpacer_6, 0, 0, 2, 1);
    gridLayout_3->addWidget(boton3, 0, 1, 1, 1);
    gridLayout_3->addWidget(boton5, 1, 1, 1, 1);

    horizontalSpacer_7 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
    gridLayout_3->addItem(horizontalSpacer_7, 0, 2, 2, 1);

    horizontalLayout_3->addWidget(groupBox_2);

    groupBox_3 = new QGroupBox(verticalLayoutWidget);
    groupBox_3->setMaximumSize(QSize(250, 110));
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
	groupBox_2->setTitle(
					QApplication::translate("MapPanel", "Teleoperacion", 0));
    groupBox_3->setAlignment(Qt::AlignCenter);
    gridLayoutWidget_2 = new QWidget(groupBox_3);
    gridLayoutWidget_2->setGeometry(QRect(10, 20, 131, 80));
    gridLayout_2 = new QGridLayout(gridLayoutWidget_2);
    gridLayout_2->setSpacing(6);
    gridLayout_2->setContentsMargins(11, 11, 11, 11);
    gridLayout_2->setContentsMargins(0, 0, 0, 0);
    gridLayout_2->addWidget(boton4, 0, 1, 1, 1);

    horizontalSpacer_8 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
    gridLayout_2->addItem(horizontalSpacer_8, 0, 0, 2, 1);

    gridLayout_2->addWidget(boton5_1, 1, 1, 1, 1);

    horizontalSpacer_9 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
    gridLayout_2->addItem(horizontalSpacer_9, 0, 2, 2, 1);

    horizontalLayout_3->addWidget(groupBox_3);

    horizontalSpacer_5 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
    horizontalLayout_3->addItem(horizontalSpacer_5);

    horizontalLayout_3->setStretch(0, 1);
    horizontalLayout_3->setStretch(1, 10);
    horizontalLayout_3->setStretch(2, 10);
    horizontalLayout_3->setStretch(3, 1);

    verticalLayout->addLayout(horizontalLayout_3);

    verticalSpacer_4 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

    verticalLayout->addItem(verticalSpacer_4);

	textBrowser->setObjectName("textBrowser");
	textBrowser->setAccessibleName("textBrowser");
    textBrowser->setAlignment(Qt::AlignJustify);
//			textBrowser->setStyleSheet("#textBrowser {color: rgb(0,0,0); background-color: rgb(255,255,255);}");
    textBrowser->setStyleSheet("#textBrowser {color: rgb(255,255,255); background-color: rgb(0,10,145);}");

    verticalLayout->addWidget(textBrowser);

    verticalLayout->setStretch(0, 1);
    verticalLayout->setStretch(1, 30);
    verticalLayout->setStretch(2, 2);
    verticalLayout->setStretch(3, 30);
    verticalLayout->setStretch(4, 2);
    verticalLayout->setStretch(5, 30);
    verticalLayout->setStretch(6, 2);
    verticalLayout->setStretch(7, 40);

	setLayout(verticalLayout);

//	textBrowser->append("Hola, Don Pepito. Hola, Don Jose. ¿Paso usted por mi casa? Por su casa yo pase. ¿Vio usted a mi abuela? Asu abuela yo la vi. Adios, Don Pepito. Adios, Don Jose.");
//	textBrowser->clear();
//	textBrowser->append("Que tal.\nYo bien, gracias.");

	//MOD2
	pub_topic = nh_topic.advertise < std_msgs::String
			> ("interface_central_comm", 20, true);
	sub_topic = nh_sub.subscribe("central_node_comm", 1000,
			&PanelMapeo::info_progreso, this);

	client1 = nh1.serviceClient<std_srvs::Trigger>("arranca_etapa_1");
	clientMapeo = nhMapeo.serviceClient<std_srvs::Trigger>("arranca_mapeo_ini");
	clientExploracion = nhExploracion.serviceClient<std_srvs::Trigger>("arranca_exploracion");
	clientTeleop = nhTeleop.serviceClient<std_srvs::Trigger>("arranca_teleop");
	clientCancelTeleop = nhCancelTeleop.serviceClient<std_srvs::Trigger>("cancela_teleop");
	client_salir = nh_salir.serviceClient<std_srvs::Trigger>("cierra_programa");


	serverMsgMapeo = srvMsgMapeo.advertiseService("recibe_mensajes_mapeo", &PanelMapeo::recibeMensajesMapeo, this);

	// Create a timer for sending the output.  Motor controllers want to
	// be reassured frequently that they are doing the right thing, so
	// we keep re-sending velocities even when they aren't changing.
	//
	// Here we take advantage of QObject's memory management behavior:
	// since "this" is passed to the new QTimer as its parent, the
	// QTimer is deleted by the QObject destructor when this PanelMapeo
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
	connect(boton2, SIGNAL(clicked()), this, SLOT(manejadorBoton2()));
	connect(boton3, SIGNAL(clicked()), this, SLOT(manejadorBoton3()));
	connect(boton4, SIGNAL(clicked()), this, SLOT(manejadorBoton4()));
	connect(boton5, SIGNAL(clicked()), this, SLOT(manejadorBoton5()));
	connect(boton5_1, SIGNAL(clicked()), this, SLOT(manejadorBoton5_1()));
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
//void PanelMapeo::manejadorBotonSalida()
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

void PanelMapeo::manejadorBoton1()
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

void PanelMapeo::manejadorBoton2()
{
	//USANDO SERVICIOS
	if (clientMapeo.call(service))
		ROS_INFO("Llamada 2 realizada con exito.");
	else
		ROS_ERROR("Fallo al llamar al servicio arranca_mapeo_ini.");

	//USANDO TOPICS
//	std_msgs::String mensaje;
//	ROS_INFO("Mandando mensaje 2 al nodo central");
//	mensaje.data = "mensaje2";
//	pub_topic.publish(mensaje);
}

void PanelMapeo::manejadorBoton3()
{
	//USANDO SERVICIOS
	if (clientExploracion.call(service))
		ROS_INFO("Llamada 3 realizada con exito.");
	else
		ROS_ERROR("Fallo al llamar al servicio arranca_exploracion.");

	//USANDO TOPICS
//	std_msgs::String mensaje;
//	ROS_INFO("Mandando mensaje 3 al nodo central");
//	mensaje.data = "mensaje3";
//	pub_topic.publish(mensaje);
}

void PanelMapeo::manejadorBoton4()
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

void PanelMapeo::manejadorBoton5()
{
	//USANDO SERVICIOS
//	if (clientTeleop.call(service))
//		ROS_INFO("Llamada 5 realizada con exito.");
//	else
//		ROS_ERROR("Fallo al llamar al servicio arranca_teleop v2.");

	//USANDO TOPICS
//	std_msgs::String mensaje;
//	ROS_INFO("Mandando mensaje 5 al nodo central");
//	mensaje.data = "mensaje5";
//	pub_topic.publish(mensaje);
}

void PanelMapeo::manejadorBoton5_1()
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
void PanelMapeo::save(rviz::Config config) const
{
	rviz::Panel::save(config);
}

// Load all configuration data for this panel from the given Config object.
void PanelMapeo::load(const rviz::Config& config)
{
	rviz::Panel::load(config);
}

//MÉTODO QUE MODIFICA EL VALOR DE LAS DIFERENTES BARRAS DE PROGRESO
void PanelMapeo::info_progreso(const std_msgs::String::ConstPtr& str)
{
	if (strcmp(str->data.c_str(), "Progreso mapeo: Fase 0") == 0)
	{
		progressBar->setValue(21);
	}
	if (strcmp(str->data.c_str(), "Progreso mapeo: Fase 1") == 0)
	{
		progressBar->setValue(27);
	}
	if (strcmp(str->data.c_str(), "Progreso mapeo: Fase 1.1") == 0)
	{
		progressBar->setValue(34);
	}
	if (strcmp(str->data.c_str(), "Progreso mapeo: Fase 2") == 0)
	{
		progressBar->setValue(59);
	}
	if (strcmp(str->data.c_str(), "Progreso mapeo: Fase 2.1") == 0)
	{
		progressBar->setValue(63);
	}
	if (strcmp(str->data.c_str(), "Progreso mapeo: Fase 3") == 0)
	{
		progressBar->setValue(69);
	}
	if (strcmp(str->data.c_str(), "Progreso mapeo: Fase 3.1") == 0)
	{
		progressBar->setValue(73);
	}
	if (strcmp(str->data.c_str(), "Progreso mapeo: Fase 4") == 0)
	{
		progressBar->setValue(88);
	}
	if (strcmp(str->data.c_str(), "Progreso mapeo: Fase 5") == 0)
	{
		progressBar->setValue(100);
	}
}

void manejadorSIGINT(int sig)
	{
		fstream filein("/home/adri/catkin_ws/src/programa_central/files/signalINT.txt");
		filein << "SIGINT";
	//	fclose(filein);
	}
	void manejadorSIGSEGV(int sig)
	{
		fstream filein("/home/adri/catkin_ws/src/programa_central/files/signalSEGV.txt");
		filein << "SIGSEGV";
	}
	void manejadorSIGTERM(int sig)
	{
		fstream filein("/home/adri/catkin_ws/src/programa_central/files/signalTERM.txt");
		filein << "SIGTERM";
	}
	void manejadorSIGHUP(int sig)
	{
		fstream filein("/home/adri/catkin_ws/src/programa_central/files/signalHUP.txt");
		filein << "SIGHUP";
	}
	void manejadorSIGQUIT(int sig)
	{
		fstream filein("/home/adri/catkin_ws/src/programa_central/files/signalQUIT.txt");
		filein << "SIGQUIT";
	}
	void manejadorSIGKILL(int sig)
	{
		fstream filein("/home/adri/catkin_ws/src/programa_central/files/signalKILL.txt");
		filein << "SIGKILL";
	}
	void manejadorSIGABRT(int sig)
	{
		fstream filein("/home/adri/catkin_ws/src/programa_central/files/signalABRT.txt");
		filein << "SIGABRT";
	}

bool PanelMapeo::recibeMensajesMapeo(programa_central::mensajes::Request &req, programa_central::mensajes::Response &res)
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

void PanelMapeo::imprimeInstrucciones()
{
	textBrowser->append("INSTRUCCIONES");
	textBrowser->append("---------------------------------------------------------------------");
	textBrowser->append("Elija si desea explorar automaticamente el mapa o dirigir al turtlebot de manera manual:\n");
	textBrowser->append("a) Pulse el boton \"Explorar\" de la seccion \"Exploracion\" para realizar la exploracion automatica. Pulse \"Cancelar\" para cancelar la exploracion.\n");
	textBrowser->append("b) Pulse el boton \"Teleoperar\" de la seccion \"Teleoperacion\" para realizar la exploracion manual. Pulse \"Cancelar\" para cancelar el control manual.\n");
	textBrowser->append("Si desea guardar el mapa, pase a la etapa de localizacion de productos.");
	textBrowser->append("---------------------------------------------------------------------\n");
}


int main(int argc, char *argv[])
{
	ROS_INFO("Iniciando panel");
	ros::init(argc, argv, "panelMapeo"); //Le pasamos el nombre del nodo: panel
	PanelMapeo panel;

	while(ros::ok())
	{
		signal(SIGINT, manejadorSIGINT);
		signal(SIGSEGV, manejadorSIGSEGV);
		signal(SIGTERM, manejadorSIGTERM);
		signal(SIGHUP, manejadorSIGHUP);
		signal(SIGQUIT, manejadorSIGQUIT);
		signal(SIGKILL, manejadorSIGKILL);
		signal(SIGABRT, manejadorSIGABRT);
		ros::spinOnce();
	}
//	ros::spin();
	return 0;
}

} // end namespace rviz_plugin_tutorials

// Tell pluginlib about this class.  Every class which should be
// loadable by pluginlib::ClassLoader must have these two lines
// compiled in its .cpp file, outside of any namespace scope.
#include <pluginlib/class_list_macros.h>
PLUGINLIB_EXPORT_CLASS(rviz_plugin_tutorials::PanelMapeo, rviz::Panel)
// END_TUTORIAL
