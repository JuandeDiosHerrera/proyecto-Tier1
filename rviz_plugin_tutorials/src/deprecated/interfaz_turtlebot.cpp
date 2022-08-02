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

#include "interfaz_turtlebot.h"

namespace rviz_plugin_tutorials
{

// We start with the constructor, doing the standard Qt thing of
// passing the optional *parent* argument on to the superclass
// constructor.
InterfazTurtlebot::InterfazTurtlebot(QWidget* parent) :
		rviz::Panel(parent), linear_velocity_(0), angular_velocity_(0)
{
	/*MOD*/

//	boton1 = new QPushButton("Arrancar Turtlebot", this);
//	boton1->setMaximumWidth(150);
//	boton1->setMaximumHeight(35);

	boton2 = new QPushButton("Etapa de mapeo", this);
	boton2->setMaximumWidth(150);
	boton2->setMaximumHeight(35);
	boton2->setToolTip(
			"Se escanea la zona y se guarda el mapa en este ordenador.");
//	boton2->setCursor(QCursor(Qt::PointingHandCursor));

	boton3 = new QPushButton("Localizacion productos", this);
	boton3->setMaximumWidth(160);
	boton3->setMaximumHeight(35);
	boton3->setToolTip(
			"Se realiza la localizacion del robot y de los productos en el mapa.");
//	boton3->setCursor(QCursor(Qt::PointingHandCursor));

	boton4 = new QPushButton("Etapa de guiado", this);
	boton4->setMaximumWidth(150);
	boton4->setMaximumHeight(35);
	boton4->setToolTip(
			"Se realiza la etapa de guiado del turtlebot por el mapa.");
//	boton4->setCursor(QCursor(Qt::PointingHandCursor));

	boton5 = new QPushButton("Teleoperar", this);
	boton5->setMaximumWidth(100);
	boton5->setMaximumHeight(35);
	boton5->setToolTip("Control manual del robot");
//	boton5->setCursor(QCursor(Qt::PointingHandCursor));

	boton5_1 = new QPushButton("Cancelar", this);
	boton5_1->setMaximumWidth(100);
	boton5_1->setMaximumHeight(35);
	boton5_1->setToolTip("Cancela el control manual");
//	boton5_1->setCursor(QCursor(Qt::PointingHandCursor));

//MOD BOTÓN DE SALIDA DE PROGRAMA
	boton_salida = new QPushButton("Salir", this);
	boton_salida->setMaximumWidth(150);
	boton_salida->setMaximumHeight(35);
	boton_salida->setToolTip("Salir del programa");
//	boton_salida->setCursor(QCursor(Qt::PointingHandCursor));

	textBrowser = new QTextBrowser();

//	bar1 = new QProgressBar;
	bar2 = new QProgressBar;
	bar2->setValue(0);
	bar3 = new QProgressBar;
	bar3->setValue(0);
	bar4 = new QProgressBar;
	bar4->setValue(0);

//	QHBoxLayout* layout1 = new QHBoxLayout;
	QHBoxLayout* layout2 = new QHBoxLayout;
	layout2->setSpacing(40);
	QHBoxLayout* layout3 = new QHBoxLayout;
	QHBoxLayout* layout4 = new QHBoxLayout;
	layout4->setSpacing(40);
	QHBoxLayout* layout5 = new QHBoxLayout;

	//QHBoxLayout* layout5_1 = new QHBoxLayout;

//	layout1->setSpacing(5);
	layout5->setSpacing(2);

//	layout1->addWidget(
//			new QLabel(
//					"Arrancar los drivers del Turtlebot y de la Kinect para operar con ellos.")); //Los \n generan violación de segmento en RVIZ
	//output_topic_editor_ = new QLineEdit;
	//layout1->addWidget( output_topic_editor_ );
	//boton1->setIcon(QIcon::fromTheme("/home/adri/catkin_ws/src/prototipo/logo/turtlebot_2_lg.png"));
//	boton1->setToolTip("Inicia el Turtlebot y la Kinect");
//	layout1->addWidget(boton1);
//	layout1->addWidget(bar1);

//	layout2->addWidget(
//			new QLabel(
//					"El Turtlebot escanea la zona y guarda el mapa en el ordenador central."));
	//boton2->setToolTip("Realiza el mapeado inicial");
	layout2->addWidget(boton2);
	layout2->addWidget(bar2);

//	layout3->addWidget(
//			new QLabel(
//					"En esta etapa se realiza la localización del robot en el mapa y se procede a buscar los productos del supermercado."));
	layout3->addWidget(boton3);
	layout3->addWidget(bar3);

//	layout4->addWidget(
//			new QLabel(
//					"En esta etapa el Turtlebot le indica al usuario adónde debe ir para encontrar los productos que quiere."));
	layout4->addWidget(boton4);
	layout4->addWidget(bar4);

//	layout5->addWidget(
//			new QLabel(
//					"Habilita la teleoperacion para controlar el Turtlebot de forma manual."));
	layout5->addWidget(boton5);
	layout5->addWidget(boton5_1);
	/*FIN MOD*/

	//MOD2
	pub_topic = nh_topic.advertise<std_msgs::String>("interface_central_comm",
			20, true);
	sub_topic = nh_sub.subscribe("central_node_comm", 1000,
			&InterfazTurtlebot::info_progreso, this);

	client1 = nh1.serviceClient<std_srvs::Trigger>("arranca_etapa_1");
	client2 = nh2.serviceClient<std_srvs::Trigger>("arranca_etapa_2");
	client3 = nh3.serviceClient<std_srvs::Trigger>("arranca_etapa_3");
	client4 = nh4.serviceClient<std_srvs::Trigger>("arranca_etapa_4");
	client5 = nh5.serviceClient<std_srvs::Trigger>("arranca_etapa_5");
	client5_1 = nh5_1.serviceClient<std_srvs::Trigger>("cancela_etapa_5");
	client_salir = nh_salir.serviceClient<std_srvs::Trigger>("cierra_programa");

	// Lay out the topic field above the control widget.
	QVBoxLayout* main_layout = new QVBoxLayout;

	//main_layout->setSpacing(0);

//	groupBox = new QGroupBox;
//	groupBox->setEnabled(true);
//	groupBox->setMinimumSize(QSize(350, 90));
//	groupBox->setMaximumSize(QSize(350, 90));
//	groupBox->setCursor(QCursor(Qt::ArrowCursor));
//	groupBox->setAutoFillBackground(false);
//	groupBox->setStyleSheet(QLatin1String("QGroupBox\n"
//			" {\n"
//			"	border: 0.5px solid gray;\n"
//			"	border-radius: 2px;\n"
//			"	margin-top: 0.5em;\n"
//			"}\n"
//			"\n"
//			"QGroupBox::Title\n"
//			"{\n"
//			"	subcontrol-origin: margin;\n"
//			"	left: 10px;\n"
//			"	padding: 0 3px 0 3px;\n"
//			"}"));
//	groupBox->setInputMethodHints(Qt::ImhNone);
//	groupBox->setFlat(false);
//	groupBox->setCheckable(false);
//	groupBox->setChecked(false);
//	groupBox->setTitle(
//			QApplication::translate("TurtlePanel", "Inicializacion Turtlebot",
//					0));

	groupBox2 = new QGroupBox;
	groupBox2->setEnabled(true);
	groupBox2->setMinimumSize(QSize(350, 90));
	groupBox2->setMaximumSize(QSize(350, 90));
	groupBox2->setCursor(QCursor(Qt::ArrowCursor));
	groupBox2->setAutoFillBackground(false);
	groupBox2->setStyleSheet(QLatin1String("QGroupBox\n"
			" {\n"
			"	border: 0.5px solid gray;\n"
			"	border-radius: 2px;\n"
			"	margin-top: 0.5em;\n"
			"}\n"
			"\n"
			"QGroupBox::Title\n"
			"{\n"
			"	subcontrol-origin: margin;\n"
			"	left: 10px;\n"
			"	padding: 0 3px 0 3px;\n"
			"}"));
	groupBox2->setInputMethodHints(Qt::ImhNone);
	groupBox2->setFlat(false);
	groupBox2->setCheckable(false);
	groupBox2->setChecked(false);
	groupBox2->setTitle(
			QApplication::translate("TurtlePanel", "Etapa de mapeo", 0));

	groupBox3 = new QGroupBox;
	groupBox3->setEnabled(true);
	groupBox3->setMinimumSize(QSize(350, 90));
	groupBox3->setMaximumSize(QSize(350, 90));
	groupBox3->setCursor(QCursor(Qt::ArrowCursor));
	groupBox3->setAutoFillBackground(false);
	groupBox3->setStyleSheet(QLatin1String("QGroupBox\n"
			" {\n"
			"	border: 0.5px solid gray;\n"
			"	border-radius: 2px;\n"
			"	margin-top: 0.5em;\n"
			"}\n"
			"\n"
			"QGroupBox::Title\n"
			"{\n"
			"	subcontrol-origin: margin;\n"
			"	left: 10px;\n"
			"	padding: 0 3px 0 3px;\n"
			"}"));
	groupBox3->setInputMethodHints(Qt::ImhNone);
	groupBox3->setFlat(false);
	groupBox3->setCheckable(false);
	groupBox3->setChecked(false);
	groupBox3->setTitle(
			QApplication::translate("TurtlePanel", "Etapa de localizacion", 0));

	groupBox4 = new QGroupBox;
	groupBox4->setEnabled(true);
	groupBox4->setMinimumSize(QSize(350, 90));
	groupBox4->setMaximumSize(QSize(350, 90));
	groupBox4->setCursor(QCursor(Qt::ArrowCursor));
	groupBox4->setAutoFillBackground(false);
	groupBox4->setStyleSheet(QLatin1String("QGroupBox\n"
			" {\n"
			"	border: 0.5px solid gray;\n"
			"	border-radius: 2px;\n"
			"	margin-top: 0.5em;\n"
			"}\n"
			"\n"
			"QGroupBox::Title\n"
			"{\n"
			"	subcontrol-origin: margin;\n"
			"	left: 10px;\n"
			"	padding: 0 3px 0 3px;\n"
			"}"));
	groupBox4->setInputMethodHints(Qt::ImhNone);
	groupBox4->setFlat(false);
	groupBox4->setCheckable(false);
	groupBox4->setChecked(false);
	groupBox4->setTitle(
			QApplication::translate("TurtlePanel", "Etapa de guiado", 0));

	groupBox5 = new QGroupBox;
	groupBox5->setEnabled(true);
	groupBox5->setMinimumSize(QSize(350, 90));
	groupBox5->setMaximumSize(QSize(350, 90));
	groupBox5->setCursor(QCursor(Qt::ArrowCursor));
	groupBox5->setAutoFillBackground(false);
	groupBox5->setStyleSheet(QLatin1String("QGroupBox\n"
			" {\n"
			"	border: 0.5px solid gray;\n"
			"	border-radius: 2px;\n"
			"	margin-top: 0.5em;\n"
			"}\n"
			"\n"
			"QGroupBox::Title\n"
			"{\n"
			"	subcontrol-origin: margin;\n"
			"	left: 10px;\n"
			"	padding: 0 3px 0 3px;\n"
			"}"));
	groupBox5->setInputMethodHints(Qt::ImhNone);
	groupBox5->setFlat(false);
	groupBox5->setCheckable(false);
	groupBox5->setChecked(false);
	groupBox5->setTitle(
			QApplication::translate("TurtlePanel", "Teleoperacion", 0));

	/*MOD*/
//	main_layout->addWidget(
//			new QLabel(
//					"---Inicializacion Turtlebot------------------------------------"));
//	groupBox->setLayout(layout1);
//	main_layout->addWidget(groupBox);
//	main_layout->addWidget(
//			new QLabel(
//					"---Etapa de mapeo----------------------------------------------"));

	groupBox2->setLayout(layout2);
	main_layout->addWidget(groupBox2);
//	main_layout->addWidget(
//			new QLabel(
//					"---Etapa de localizacion---------------------------------------"));

	groupBox3->setLayout(layout3);
	main_layout->addWidget(groupBox3);
//	main_layout->addWidget(
//			new QLabel(
//					"---Etapa de guiado---------------------------------------------"));

	groupBox4->setLayout(layout4);
	main_layout->addWidget(groupBox4);
//	main_layout->addWidget(
//			new QLabel(
//					"---Teleoperacion-----------------------------------------------"));

	groupBox5->setLayout(layout5);
	main_layout->addWidget(groupBox5);
	/*FIN MOD*/

	//MOD BOTÓN DE SALIDA DE PROGRAMA
	QHBoxLayout* layoutSalida = new QHBoxLayout;
	layoutSalida->setAlignment(Qt::AlignHCenter);
	layoutSalida->addWidget(boton_salida);
	main_layout->addLayout(layoutSalida);
	textBrowser->setGeometry(QRect(15, 40, 300, 100));
	main_layout->addWidget(textBrowser);
	textBrowser->append("Hola");
	textBrowser->append("Que tal");

	setLayout(main_layout);

	// Create a timer for sending the output.  Motor controllers want to
	// be reassured frequently that they are doing the right thing, so
	// we keep re-sending velocities even when they aren't changing.
	//
	// Here we take advantage of QObject's memory management behavior:
	// since "this" is passed to the new QTimer as its parent, the
	// QTimer is deleted by the QObject destructor when this InterfazTurtlebot
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
	connect(boton_salida, SIGNAL(clicked()), this,
			SLOT(manejadorBotonSalida()));

	// Start the timer.
	output_timer->start(100);

	// Make the control widget start disabled, since we don't start with an output topic.
//	drive_widget_->setEnabled(false);
}

//MOD BOTÓN DE SALIDA DE PROGRAMA
void InterfazTurtlebot::manejadorBotonSalida()
{
	//USANDO SERVICIOS
//	if (client_salir.call(service))
//		ROS_INFO("Llamada a salir realizada con exito.");
//	else
//		ROS_ERROR("Fallo al llamar al servicio cierra_programa.");

	//EL PROPIO BOTÓN SE ENCARGA DE CERRAR EL PROGRAMA
	ROS_INFO("Cerrando RVIZ y la red de ROS...");
	system("rosnode kill /cierre_xterm");
	system("rosnode kill /RVIZ");
	system("rosnode kill /nodo_central");

	//USANDO TOPICS
//	std_msgs::String mensaje;
//	ROS_INFO("Mandando mensaje de salida al nodo central");
//	mensaje.data = "salir";
//	pub_topic.publish(mensaje);
}

void InterfazTurtlebot::manejadorBoton1()
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

void InterfazTurtlebot::manejadorBoton2()
{
	//USANDO SERVICIOS
	if (client2.call(service))
		ROS_INFO("Llamada 2 realizada con exito.");
	else
		ROS_ERROR("Fallo al llamar al servicio arranca_etapa_2.");

	//USANDO TOPICS
//	std_msgs::String mensaje;
//	ROS_INFO("Mandando mensaje 2 al nodo central");
//	mensaje.data = "mensaje2";
//	pub_topic.publish(mensaje);
}

void InterfazTurtlebot::manejadorBoton3()
{
	//USANDO SERVICIOS
	if (client3.call(service))
		ROS_INFO("Llamada 3 realizada con exito.");
	else
		ROS_ERROR("Fallo al llamar al servicio arranca_etapa_3.");

	//USANDO TOPICS
//	std_msgs::String mensaje;
//	ROS_INFO("Mandando mensaje 3 al nodo central");
//	mensaje.data = "mensaje3";
//	pub_topic.publish(mensaje);
}

void InterfazTurtlebot::manejadorBoton4()
{
	//USANDO SERVICIOS
	if (client4.call(service))
		ROS_INFO("Llamada 4 realizada con exito.");
	else
		ROS_ERROR("Fallo al llamar al servicio arranca_etapa_4.");

	//USANDO TOPICS
//	std_msgs::String mensaje;
//	ROS_INFO("Mandando mensaje 4 al nodo central");
//	mensaje.data = "mensaje4";
//	pub_topic.publish(mensaje);
}

void InterfazTurtlebot::manejadorBoton5()
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

void InterfazTurtlebot::manejadorBoton5_1()
{
	//USANDO SERVICIOS
	if (client5_1.call(service))
		ROS_INFO("Llamada 6 realizada con exito.");
	else
		ROS_ERROR("Fallo al llamar al servicio cancela_etapa_5.");

	//USANDO TOPICS
//	std_msgs::String mensaje;
//	ROS_INFO("Mandando mensaje 6 al nodo central");
//	mensaje.data = "mensaje6";
//	pub_topic.publish(mensaje);
}

// Save all configuration data from this panel to the given
// Config object.  It is important here that you call save()
// on the parent class so the class id and panel name get saved.
void InterfazTurtlebot::save(rviz::Config config) const
{
	rviz::Panel::save(config);
}

// Load all configuration data for this panel from the given Config object.
void InterfazTurtlebot::load(const rviz::Config& config)
{
	rviz::Panel::load(config);
}

//MÉTODO QUE MODIFICA EL VALOR DE LAS DIFERENTES BARRAS DE PROGRESO
void InterfazTurtlebot::info_progreso(const std_msgs::String::ConstPtr& str)
{
	if (strcmp(str->data.c_str(), "Progreso mapeo: Fase 0") == 0)
	{
		bar2->setValue(21);
	}
	if (strcmp(str->data.c_str(), "Progreso mapeo: Fase 1") == 0)
	{
		bar2->setValue(27);
	}
	if (strcmp(str->data.c_str(), "Progreso mapeo: Fase 1.1") == 0)
	{
		bar2->setValue(34);
	}
	if (strcmp(str->data.c_str(), "Progreso mapeo: Fase 2") == 0)
	{
		bar2->setValue(59);
	}
	if (strcmp(str->data.c_str(), "Progreso mapeo: Fase 2.1") == 0)
	{
		bar2->setValue(63);
	}
	if (strcmp(str->data.c_str(), "Progreso mapeo: Fase 3") == 0)
	{
		bar2->setValue(69);
	}
	if (strcmp(str->data.c_str(), "Progreso mapeo: Fase 3.1") == 0)
	{
		bar2->setValue(73);
	}
	if (strcmp(str->data.c_str(), "Progreso mapeo: Fase 4") == 0)
	{
		bar2->setValue(88);
	}
	if (strcmp(str->data.c_str(), "Progreso mapeo: Fase 5") == 0)
	{
		bar2->setValue(100);
	}

	if (strcmp(str->data.c_str(), "Progreso localizacion: Fase 0") == 0)
	{
		bar3->setValue(22);
	}
	if (strcmp(str->data.c_str(), "Progreso localizacion: Fase 1") == 0)
	{
		bar3->setValue(35);
	}
	if (strcmp(str->data.c_str(), "Progreso localizacion: Fase 2") == 0)
	{
		bar3->setValue(87);
	}
	if (strcmp(str->data.c_str(), "Progreso localizacion: Fase 3") == 0)
	{
		bar3->setValue(100);
	}

	if (strcmp(str->data.c_str(), "Progreso guiado: Fase 0") == 0)
	{
		bar4->setValue(22);
	}
	if (strcmp(str->data.c_str(), "Progreso guiado: Fase 1") == 0)
	{
		bar4->setValue(57);
	}
	if (strcmp(str->data.c_str(), "Progreso guiado: Fase 2") == 0)
	{
		bar4->setValue(100);
	}
}

int main(int argc, char *argv[])
{
	ROS_INFO("Iniciando panel");
	ros::init(argc, argv, "panel"); //Le pasamos el nombre del nodo: panel
	InterfazTurtlebot panel;
	ros::spin();
	return 0;
}

} // end namespace rviz_plugin_tutorials

// Tell pluginlib about this class.  Every class which should be
// loadable by pluginlib::ClassLoader must have these two lines
// compiled in its .cpp file, outside of any namespace scope.
#include <pluginlib/class_list_macros.h>
PLUGINLIB_EXPORT_CLASS(rviz_plugin_tutorials::InterfazTurtlebot, rviz::Panel)
// END_TUTORIAL
