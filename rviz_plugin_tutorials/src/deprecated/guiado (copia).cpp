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
#include <boost/algorithm/string.hpp>
#include <ctype.h>

//#include <iostream>
//#include <stdlib.h>
//#include <fstream>
//#include <string>
//#include <cstdlib>

#include "guiado.h"


namespace rviz_plugin_tutorials
{

using namespace std;

// We start with the constructor, doing the standard Qt thing of
// passing the optional *parent* argument on to the superclass
// constructor.
PanelGuiado::PanelGuiado(QWidget* parent) :
		rviz::Panel(parent), linear_velocity_(0), angular_velocity_(0)
{
	/*MOD*/

//	boton1 = new QPushButton("Arrancar Turtlebot", this);
//	boton1->setMaximumWidth(150);
//	boton1->setMaximumHeight(35);
	pushButton = new QPushButton("Inicio", this);
//	pushButton->setMaximumWidth(150);
//	pushButton->setMaximumHeight(35);
	pushButton->setToolTip(
			"Se cargan los programas encargados del guiado.");
//	pushButton->setCursor(QCursor(Qt::PointingHandCursor));

	pushButton_2 = new QPushButton("Enviar", this);
//	pushButton_2->setMaximumWidth(160);
//	pushButton_2->setMaximumHeight(35);
	pushButton_2->setToolTip(
			"Se procede a guardar la lista de la compra del cliente.");
//	pushButton_2->setCursor(QCursor(Qt::PointingHandCursor));

//	boton4 = new QPushButton("Teleoperar", this);
////	boton4->setMaximumWidth(100);
////	boton4->setMaximumHeight(35);
//	boton4->setToolTip(
//			"Se realiza la etapa de guiado del turtlebot por el mapa.");
//	boton4->setCursor(QCursor(Qt::PointingHandCursor));

	pushButton_3 = new QPushButton("Guiado", this);
//	pushButton_3->setMaximumWidth(100);
//	pushButton_3->setMaximumHeight(35);
	pushButton_3->setToolTip("Se realiza la etapa de guiado del turtlebot por el mapa.");
//	pushButton_3->setCursor(QCursor(Qt::PointingHandCursor));

//	boton5_1 = new QPushButton("Cancelar", this);
////	boton5_1->setMaximumWidth(100);
////	boton5_1->setMaximumHeight(35);
//	boton5_1->setToolTip("Cancela el control manual");
//	boton5_1->setCursor(QCursor(Qt::PointingHandCursor));

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
//	        //pushButton_3 = new QPushButton(gridLayoutWidget);
//	        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
//	        sizePolicy.setHorizontalStretch(0);
//	        sizePolicy.setVerticalStretch(0);
//	        sizePolicy.setHeightForWidth(pushButton_3->sizePolicy().hasHeightForWidth());
//	        pushButton_3->setSizePolicy(sizePolicy);
//
//	        gridLayout->addWidget(pushButton_3, 2, 1, 1, 1);
//
//	       // boton4 = new QPushButton(gridLayoutWidget);
//	        sizePolicy.setHeightForWidth(boton4->sizePolicy().hasHeightForWidth());
//	        boton4->setSizePolicy(sizePolicy);
//	        boton4->setLayoutDirection(Qt::LeftToRight);
//
//	        gridLayout->addWidget(boton4, 1, 3, 1, 1);
//
//	        //pushButton_2 = new QPushButton(gridLayoutWidget);
//	        sizePolicy.setHeightForWidth(pushButton_2->sizePolicy().hasHeightForWidth());
//	        pushButton_2->setSizePolicy(sizePolicy);
//
//	        gridLayout->addWidget(pushButton_2, 1, 1, 1, 1);
//
//	        //pushButton_3_1 = new QPushButton(gridLayoutWidget);
//	        sizePolicy.setHeightForWidth(pushButton_3_1->sizePolicy().hasHeightForWidth());
//	        pushButton_3_1->setSizePolicy(sizePolicy);
//
//	        gridLayout->addWidget(pushButton_3_1, 2, 3, 1, 1);
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
//	        //pushButton = new QPushButton(gridLayoutWidget);
//	        QSizePolicy sizePolicy1(QSizePolicy::Preferred, QSizePolicy::Preferred);
//	        sizePolicy1.setHorizontalStretch(0);
//	        sizePolicy1.setVerticalStretch(1);
//	        sizePolicy1.setHeightForWidth(pushButton->sizePolicy().hasHeightForWidth());
//	        pushButton->setSizePolicy(sizePolicy1);
//	        QPalette palette;
//	        QBrush brush(QColor(255, 0, 0, 255));
//	        brush.setStyle(Qt::SolidPattern);
//	        palette.setBrush(QPalette::Active, QPalette::Button, brush);
//	        palette.setBrush(QPalette::Inactive, QPalette::Button, brush);
//	        palette.setBrush(QPalette::Disabled, QPalette::Button, brush);
//	        pushButton->setPalette(palette);
//	        pushButton->setLayoutDirection(Qt::LeftToRight);
//
//	        gridLayout->addWidget(pushButton, 0, 1, 1, 1);
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
	        gridLayoutWidget->setGeometry(QRect(60, 10, 331, 451));
	        gridLayout = new QGridLayout(gridLayoutWidget);
	        gridLayout->setSpacing(6);
	        gridLayout->setContentsMargins(11, 11, 11, 11);
	        gridLayout->setContentsMargins(0, 0, 0, 0);
	        horizontalSpacer_5 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

	        gridLayout->addItem(horizontalSpacer_5, 0, 4, 7, 1);

	        groupBox = new QGroupBox(gridLayoutWidget);
	        QSizePolicy sizePolicy(QSizePolicy::MinimumExpanding, QSizePolicy::Preferred);
	        sizePolicy.setHorizontalStretch(0);
	        sizePolicy.setVerticalStretch(0);
	        sizePolicy.setHeightForWidth(groupBox->sizePolicy().hasHeightForWidth());
	        groupBox->setSizePolicy(sizePolicy);
	        groupBox->setMaximumSize(QSize(300, 80));
	        groupBox->setStyleSheet("			QGroupBox\n"
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
	"			}");
	        groupBox->setTitle(
	        			QApplication::translate("TurtlePanel", "Guiado", 0));
	        horizontalLayoutWidget = new QWidget(groupBox);
	        horizontalLayoutWidget->setGeometry(QRect(10, 20, 281, 51));
	        horizontalLayout = new QHBoxLayout(horizontalLayoutWidget);
	        horizontalLayout->setSpacing(6);
	        horizontalLayout->setContentsMargins(11, 11, 11, 11);
	        horizontalLayout->setContentsMargins(0, 0, 0, 0);

	        horizontalLayout->addWidget(pushButton);

	        horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

	        horizontalLayout->addItem(horizontalSpacer);

	        progressBar = new QProgressBar(horizontalLayoutWidget);
	        progressBar->setValue(0);

	        horizontalLayout->addWidget(progressBar);

	        horizontalLayout->setStretch(0, 5);
	        horizontalLayout->setStretch(1, 1);
	        horizontalLayout->setStretch(2, 10);

	        gridLayout->addWidget(groupBox, 1, 1, 1, 3);

	        horizontalSpacer_3 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

	        gridLayout->addItem(horizontalSpacer_3, 5, 1, 1, 1);

	        verticalSpacer_3 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

	        gridLayout->addItem(verticalSpacer_3, 4, 2, 1, 1);

	        verticalSpacer_2 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

	        gridLayout->addItem(verticalSpacer_2, 2, 2, 1, 1);

	        verticalSpacer_4 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

	        gridLayout->addItem(verticalSpacer_4, 6, 2, 1, 1);

	        horizontalSpacer_6 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

	        gridLayout->addItem(horizontalSpacer_6, 0, 0, 7, 1);

	        QSizePolicy sizePolicy1(QSizePolicy::Fixed, QSizePolicy::Fixed);
	        sizePolicy1.setHorizontalStretch(0);
	        sizePolicy1.setVerticalStretch(0);
	        sizePolicy1.setHeightForWidth(pushButton_3->sizePolicy().hasHeightForWidth());
	        pushButton_3->setSizePolicy(sizePolicy1);

	        gridLayout->addWidget(pushButton_3, 5, 2, 1, 1);

	        horizontalSpacer_4 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

	        gridLayout->addItem(horizontalSpacer_4, 5, 3, 1, 1);

	        groupBox_2 = new QGroupBox(gridLayoutWidget);
	        sizePolicy.setHeightForWidth(groupBox_2->sizePolicy().hasHeightForWidth());
	        groupBox_2->setSizePolicy(sizePolicy);
	        groupBox_2->setMaximumSize(QSize(300, 80));
	        groupBox_2->setStyleSheet("			QGroupBox\n"
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
	"			}");
	        groupBox_2->setTitle(QApplication::translate("TurtlePanel", "Lista de la compra", 0));
	        groupBox_2->setAlignment(Qt::AlignLeading|Qt::AlignLeft|Qt::AlignVCenter);
	        horizontalLayoutWidget_2 = new QWidget(groupBox_2);
	        horizontalLayoutWidget_2->setGeometry(QRect(10, 20, 281, 51));
	        horizontalLayout_2 = new QHBoxLayout(horizontalLayoutWidget_2);
	        horizontalLayout_2->setSpacing(6);
	        horizontalLayout_2->setContentsMargins(11, 11, 11, 11);
	        horizontalLayout_2->setContentsMargins(0, 0, 0, 0);
	        lineEdit = new QLineEdit(horizontalLayoutWidget_2);

	        horizontalLayout_2->addWidget(lineEdit);

	        horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

	        horizontalLayout_2->addItem(horizontalSpacer_2);

	        horizontalLayout_2->addWidget(pushButton_2);

	        horizontalLayout_2->setStretch(0, 15);
	        horizontalLayout_2->setStretch(1, 1);
	        horizontalLayout_2->setStretch(2, 5);

	        gridLayout->addWidget(groupBox_2, 3, 1, 1, 3);

	        verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);

	        gridLayout->addItem(verticalSpacer, 0, 1, 1, 3);

	        textBrowser = new QTextBrowser(gridLayoutWidget);

	        //MOD 02/10/16 PARA CAMBIAR COLOR DE LETRA Y FONDO
			textBrowser->setObjectName("textBrowser");
			textBrowser->setAccessibleName("textBrowser");
	        textBrowser->setAlignment(Qt::AlignJustify);
//			textBrowser->setStyleSheet("#textBrowser {color: rgb(0,0,0); background-color: rgb(255,255,255);}");
		textBrowser->setStyleSheet("#textBrowser {color: rgb(255,255,255); background-color: rgb(0,10,145);}");


	        gridLayout->addWidget(textBrowser, 7, 1, 1, 3);

	        gridLayout->setRowStretch(0, 1);
	        gridLayout->setRowStretch(1, 15);
	        gridLayout->setRowStretch(2, 2);
	        gridLayout->setRowStretch(3, 15);
	        gridLayout->setRowStretch(4, 1);
	        gridLayout->setRowStretch(5, 10);
	        gridLayout->setRowStretch(6, 2);
	        gridLayout->setRowStretch(7, 20);
	        gridLayout->setColumnStretch(0, 1);
	        gridLayout->setColumnStretch(1, 15);
	        gridLayout->setColumnStretch(2, 10);
	        gridLayout->setColumnStretch(3, 15);
	        gridLayout->setColumnStretch(4, 1);

	setLayout(gridLayout);

	//MOD2
	pub_topic = nh_topic.advertise < std_msgs::String
			> ("interface_central_comm", 20, true);
	sub_topic = nh_sub.subscribe("central_node_comm", 1000,
			&PanelGuiado::info_progreso, this);

	client1 = nh1.serviceClient<std_srvs::Trigger>("arranca_etapa_1");
	client2 = nh2.serviceClient<std_srvs::Trigger>("arranca_guiado");
	client3 = nh3.serviceClient<std_srvs::Trigger>("arranca_etapa_3");
	client4 = nh4.serviceClient<std_srvs::Trigger>("arranca_etapa_4");
	client5 = nh5.serviceClient<std_srvs::Trigger>("arranca_etapa_5");
	client5_1 = nh5_1.serviceClient<std_srvs::Trigger>("cancela_etapa_5");
	client_salir = nh_salir.serviceClient<std_srvs::Trigger>("cierra_programa");

	serverMsgGuiado = srvMsgGuiado.advertiseService("recibe_mensajes_guiado", &PanelGuiado::recibeMensajesGuiado, this);

	clienteLista = nhLista.serviceClient<std_srvs::Trigger>("crea_lista");
	clienteProductos = nhProductos.serviceClient<etapa_guiado::Productos>("recibe_productos");

	// Create a timer for sending the output.  Motor controllers want to
	// be reassured frequently that they are doing the right thing, so
	// we keep re-sending velocities even when they aren't changing.
	//
	// Here we take advantage of QObject's memory management behavior:
	// since "this" is passed to the new QTimer as its parent, the
	// QTimer is deleted by the QObject destructor when this PanelGuiado
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
	connect(pushButton, SIGNAL(clicked()), this, SLOT(manejadorBoton2()));
	connect(pushButton_2, SIGNAL(clicked()), this, SLOT(manejadorBoton3()));
//	connect(boton4, SIGNAL(clicked()), this, SLOT(manejadorBoton4()));
	connect(pushButton_3, SIGNAL(clicked()), this, SLOT(manejadorBoton5()));
//	connect(boton5_1, SIGNAL(clicked()), this, SLOT(manejadorBoton5_1()));
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
//void PanelGuiado::manejadorBotonSalida()
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

void PanelGuiado::manejadorBoton1()
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

void PanelGuiado::manejadorBoton2()
{
	//USANDO SERVICIOS
	if (client2.call(service))
		ROS_INFO("Llamada 2 realizada con exito.");
	else
		ROS_ERROR("Fallo al llamar al servicio arranca_guiado.");

	//USANDO TOPICS
//	std_msgs::String mensaje;
//	ROS_INFO("Mandando mensaje 2 al nodo central");
//	mensaje.data = "mensaje2";
//	pub_topic.publish(mensaje);
}

void PanelGuiado::manejadorBoton3()
{
//	//USANDO SERVICIOS
//	if (client3.call(service))
//		ROS_INFO("Llamada 3 realizada con exito.");
//	else
//		ROS_ERROR("Fallo al llamar al servicio arranca_etapa_3.");


	std::string listaProductos = recibeProductosLista();
	std::vector<std::string> productosSeparados;
	cout << "Productos recibidos: " << listaProductos << endl;
	if(listaProductos != "")
	{
		productosSeparados = separaElementos(listaProductos);
		//cout << endl;
		//cout << "Probando si funciona clear..." << endl;
		lineEdit->clear();
		//cout << "clear funciona." << endl;
	}
	else
	{
		ROS_ERROR("No se puede pasar 0 elementos");
		textBrowser->setTextColor(QColor(255,0,0,255));
		textBrowser->append("\nNo ha enviado ningun producto.\n");
		textBrowser->setTextColor(QColor(255,255,255,255));
	}

	servicioProductos.request.productos.assign(productosSeparados.begin(),productosSeparados.end());
	if(clienteProductos.call(servicioProductos))
	{
		switch(servicioProductos.response.cmd)
		{
		case 0:
			textBrowser->clear();
			break;
		case 1:
			textBrowser->append(servicioProductos.response.mensaje.c_str());
			break;
		case 2:
			imprimeInstrucciones();
			break;
		}
	}

	//USANDO TOPICS
//	std_msgs::String mensaje;
//	ROS_INFO("Mandando mensaje 3 al nodo central");
//	mensaje.data = "mensaje3";
//	pub_topic.publish(mensaje);
}

std::string PanelGuiado::recibeProductosLista()
{
	return lineEdit->text().toUtf8().constData();
}

std::vector<std::string> PanelGuiado::separaElementos(std::string listaProductos)
{
	std::vector<std::string> listaSeparada;
	std::vector<std::string> listaResultado;
	boost::split(listaSeparada, listaProductos, boost::is_any_of(","));
	listaResultado = limpiaLista(listaSeparada);
	cout << "Dimension del vector: " << listaResultado.size() << endl;
	cout << "Productos recibidos y separados: " << endl;
	for (std::vector<std::string>::const_iterator i = listaResultado.begin(); i != listaResultado.end(); ++i)
		cout << *i << endl;
	//cout << endl;
	return listaResultado;
}

std::vector<std::string> PanelGuiado::limpiaLista(std::vector<std::string> listaSeparada)
{
	std::vector<std::string> listaResultado;
//	if(!listaSeparada.empty())
//	{
		//cout << "El vector no esta vacio" << endl;
		cout << listaSeparada.size() << endl;
		for (int i = 0; i < listaSeparada.size(); ++i)
		{
			//cout << "Recorriendo el vector..." << endl;
			std::string producto = listaSeparada.at(i);
			if(producto != "")
			{
				std::string productoResultado = "";
				std::string productoResultado2 = "";

				productoResultado = producto;
				for(int j = 0; j < producto.length(); ++j)
				{
					if(isalnum(producto.at(j)))	//isalpha
						break;
					else
					{
						//productoResultado = producto;
						productoResultado = producto.substr(j+1);
						//cout << "Borrado limite inferior: " << productoResultado << endl;
					}
				}

				productoResultado2 = productoResultado;
				for(int k = productoResultado.length()-1; 0 <= k; --k)
				{
					if(isalnum(productoResultado.at(k)))	//isalpha
						break;
					else
					{
						//productoResultado2 = productoResultado;
						productoResultado2 = productoResultado.substr(0,k);
						//cout << "Borrado limite inferior: " << productoResultado << endl;
					}
				}
//				if(isalpha(producto.at(0)))
//				{
//					productoResultado = producto.substr(0);
//					//cout << "Borrado limite inferior: " << productoResultado << endl;
//				}
//				if(!isalpha(producto.at(producto.length()-1)))
//				{
//					productoResultado = productoResultado.substr(0,productoResultado.length()-1);
//					//cout << "Borrado limite superior: " << productoResultado << endl;
//				}
//				listaResultado.push_back(productoResultado);
				if(productoResultado2 != "")
					listaResultado.push_back(productoResultado2);
				else
					ROS_ERROR("Formato de producto no valido");
			}
			else
				ROS_ERROR("No se puede introducir un producto vacio");
		}
//	}
	//else
		//cout << "El vector estaba vacio" << endl;
	return listaResultado;
}

void PanelGuiado::manejadorBoton4()
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

void PanelGuiado::manejadorBoton5()
{
	//USANDO SERVICIOS
//	if (client5.call(service))
//		ROS_INFO("Llamada 5 realizada con exito.");
//	else
//		ROS_ERROR("Fallo al llamar al servicio arranca_etapa_5.");

	textBrowser->clear();

	clienteLista.call(servicioLista);


	//USANDO TOPICS
//	std_msgs::String mensaje;
//	ROS_INFO("Mandando mensaje 5 al nodo central");
//	mensaje.data = "mensaje5";
//	pub_topic.publish(mensaje);
}

void PanelGuiado::manejadorBoton5_1()
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
void PanelGuiado::save(rviz::Config config) const
{
	rviz::Panel::save(config);
}

// Load all configuration data for this panel from the given Config object.
void PanelGuiado::load(const rviz::Config& config)
{
	rviz::Panel::load(config);
}

//MÉTODO QUE MODIFICA EL VALOR DE LAS DIFERENTES BARRAS DE PROGRESO
void PanelGuiado::info_progreso(const std_msgs::String::ConstPtr& str)
{
	if (strcmp(str->data.c_str(), "Progreso guiado: Fase 0") == 0)
	{
		progressBar->setValue(22);
	}
	if (strcmp(str->data.c_str(), "Progreso guiado: Fase 1") == 0)
	{
		progressBar->setValue(57);
	}
	if (strcmp(str->data.c_str(), "Progreso guiado: Fase 2") == 0)
	{
		progressBar->setValue(100);
	}
}


bool PanelGuiado::recibeMensajesGuiado(programa_central::mensajes::Request &req, programa_central::mensajes::Response &res)
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


void PanelGuiado::imprimeInstrucciones()
{
	textBrowser->append("INSTRUCCIONES");
	textBrowser->append("---------------------------------------------------------------------");
	textBrowser->append("Ahora puede realizar la compra. Para ello, siga los siguientes pasos:\n");
	textBrowser->append("1. Escriba los productos que desea separados por comas y pulse el boton \"Enviar\" de \"Lista de la compra\".\n");
	textBrowser->append("2. Cuando haya completado su lista de la compra, pulse el boton \"Guiado\".");
	textBrowser->append("---------------------------------------------------------------------\n");
}

//int main(int argc, char *argv[])
//{
//	ROS_INFO("Iniciando panel");
//	ros::init(argc, argv, "PanelGuiado"); //Le pasamos el nombre del nodo: panel
//	PanelGuiado panel;
//	ros::spin();
//	return 0;
//}

} // end namespace rviz_plugin_tutorials

// Tell pluginlib about this class.  Every class which should be
// loadable by pluginlib::ClassLoader must have these two lines
// compiled in its .cpp file, outside of any namespace scope.
#include <pluginlib/class_list_macros.h>
PLUGINLIB_EXPORT_CLASS(rviz_plugin_tutorials::PanelGuiado, rviz::Panel)
// END_TUTORIAL
