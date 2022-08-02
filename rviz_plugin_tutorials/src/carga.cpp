
#include "carga.h"

using namespace std;

namespace rviz_plugin_tutorials
{

PanelCarga::PanelCarga(QWidget* parent) : rviz::Panel(parent)
{
	botonCargar = new QPushButton("Cargar", this);
	botonCargar->setToolTip("Llevar el turtlebot a la base de carga.");
	botonCargar->setCursor(QCursor(Qt::PointingHandCursor));

	botonSalir = new QPushButton("Salir", this);
	botonSalir->setToolTip("Sacar al turtlebot de la base de carga.");
	botonSalir->setCursor(QCursor(Qt::PointingHandCursor));

	centralWidget = new QWidget();
	gridLayoutWidget = new QWidget(centralWidget);
	gridLayoutWidget->setGeometry(QRect(60, 0, 331, 451));
	gridLayout = new QGridLayout(gridLayoutWidget);
	gridLayout->setSpacing(6);
	gridLayout->setContentsMargins(11, 11, 11, 11);
	gridLayout->setContentsMargins(0, 0, 0, 0);

	verticalSpacer_5 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);
	gridLayout->addItem(verticalSpacer_5, 0, 2, 1, 1);

	userHome = getenv("HOME");
	char logo[256];
	strcpy(logo, userHome);
	strcat(logo, "/catkin_ws/src/interfaz/rviz_plugin_tutorials/icons/classes/comerzzia_aicia.png");

	label = new QLabel(gridLayoutWidget);
	label->setPixmap(QPixmap(QString::fromUtf8(logo)));
	label->setAlignment(Qt::AlignCenter);
	gridLayout->addWidget(label, 1, 1, 1, 3);

	horizontalSpacer_5 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	gridLayout->addItem(horizontalSpacer_5, 0, 4, 10, 1);

	groupBoxBaterias = new QGroupBox(gridLayoutWidget);
	QSizePolicy sizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);
	sizePolicy.setHorizontalStretch(0);
	sizePolicy.setVerticalStretch(0);
	sizePolicy.setHeightForWidth(groupBoxBaterias->sizePolicy().hasHeightForWidth());
	groupBoxBaterias->setSizePolicy(sizePolicy);
	groupBoxBaterias->setMaximumSize(QSize(375, 120));
	groupBoxBaterias->setStyleSheet(
			"QGroupBox\n"
			"{\n"
			"border: 0.5px solid gray;\n"
			"border-radius: 2px;\n"
			"margin-top: 0.5em;\n"
			"}\n"
			"QGroupBox::Title\n"
			"{\n"
			"subcontrol-origin: margin;\n"
			"left: 10px;\n"
			"padding: 0 3px 0 3px;\n"
			"}"
	);
	groupBoxBaterias->setTitle(QApplication::translate("Batteries status", "Estado baterias", 0));
	groupBoxBaterias->setAlignment(Qt::AlignHCenter);

	horizontalLayoutWidget_main = new QWidget(groupBoxBaterias);
	horizontalLayoutWidget_main->setGeometry(QRect(10, 20, 350, 90));

	horizontalLayout_main = new QHBoxLayout(horizontalLayoutWidget_main);
	horizontalLayout_main->setSpacing(6);
	horizontalLayout_main->setContentsMargins(11, 11, 11, 11);
	horizontalLayout_main->setContentsMargins(0, 0, 0, 0);

	groupBoxTurtlebot = new QGroupBox(horizontalLayoutWidget_main);
	groupBoxTurtlebot->setSizePolicy(sizePolicy);
	groupBoxTurtlebot->setMaximumSize(QSize(150, 80));
	groupBoxTurtlebot->setStyleSheet(
			"QGroupBox\n"
			"{\n"
			"border: 0.0px solid gray;\n"
			"border-radius: 2px;\n"
			"margin-top: 0.5em;\n"
			"}\n"
			"QGroupBox::Title\n"
			"{\n"
			"subcontrol-origin: margin;\n"
			"left: 10px;\n"
			"padding: 0 3px 0 3px;\n"
			"}"
	);
	groupBoxTurtlebot->setTitle(QApplication::translate("Turtlebot", "Turtlebot", 0));
	groupBoxTurtlebot->setAlignment(Qt::AlignHCenter);

	horizontalLayoutWidget = new QWidget(groupBoxTurtlebot);
	horizontalLayoutWidget->setGeometry(QRect(10, 20, 281, 51));
	horizontalLayout = new QHBoxLayout(horizontalLayoutWidget);
	horizontalLayout->setSpacing(6);
	horizontalLayout->setContentsMargins(11, 11, 11, 11);
	horizontalLayout->setContentsMargins(0, 0, 0, 0);

	bateriaTurtlebot = new QProgressBar(horizontalLayoutWidget);
	bateriaTurtlebot->setValue(0);
	bateriaTurtlebot->setMinimumWidth(125);
	bateriaTurtlebot->setStyleSheet("QProgressBar {border: 2px solid grey;border-radius: 5px;text-align: center;}"
							   	    "QProgressBar::chunk {background-color: #00FF00;width: 10px;margin:0.5px;}");

	horizontalLayout_main->addWidget(groupBoxTurtlebot);

	//CARGA PORTATIL

	groupBoxPortatil = new QGroupBox(horizontalLayoutWidget_main);
	QSizePolicy sizePolicy_1(QSizePolicy::Expanding, QSizePolicy::Fixed);
	sizePolicy_1.setHorizontalStretch(0);
	sizePolicy_1.setVerticalStretch(0);
	sizePolicy_1.setHeightForWidth(groupBoxPortatil->sizePolicy().hasHeightForWidth());
	groupBoxPortatil->setSizePolicy(sizePolicy_1);
	groupBoxPortatil->setMaximumSize(QSize(150, 80));
	groupBoxPortatil->setStyleSheet(
			"QGroupBox\n"
			"{\n"
			"border: 0.0px solid gray;\n"
			"border-radius: 2px;\n"
			"margin-top: 0.5em;\n"
			"}\n"
			"QGroupBox::Title\n"
			"{\n"
			"subcontrol-origin: margin;\n"
			"left: 10px;\n"
			"padding: 0 3px 0 3px;\n"
			"}"
	);
	groupBoxPortatil->setTitle(QApplication::translate("Laptop", "Portatil", 0));
	groupBoxPortatil->setAlignment(Qt::AlignHCenter);

	horizontalLayoutWidget_1 = new QWidget(groupBoxPortatil);
	horizontalLayoutWidget_1->setGeometry(QRect(10, 20, 281, 51));

	horizontalLayout_1 = new QHBoxLayout(horizontalLayoutWidget_1);
	horizontalLayout_1->setSpacing(6);
	horizontalLayout_1->setContentsMargins(11, 11, 11, 11);
	horizontalLayout_1->setContentsMargins(0, 0, 0, 0);

	bateriaPortatil = new QProgressBar(horizontalLayoutWidget_1);
	bateriaPortatil->setValue(0);
	bateriaPortatil->setMinimumWidth(125);
	bateriaPortatil->setObjectName("bateriaPortatil");
	bateriaPortatil->setAccessibleName("bateriaPortatil");
	bateriaPortatil->setStyleSheet("QProgressBar {border: 2px solid grey;border-radius: 5px;text-align: center;}"
								   "QProgressBar::chunk {background-color: #00FF00;width: 10px;margin: 0.5px;}");

	horizontalLayout_main->addWidget(groupBoxPortatil);

	horizontalLayout_main->setStretch(0, 10);
	horizontalLayout_main->setStretch(1, 10);

	gridLayout->addWidget(groupBoxBaterias, 3, 2, 1, 1);

	horizontalSpacer_3 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	gridLayout->addItem(horizontalSpacer_3, 5, 1, 1, 1);

	verticalSpacer_3 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);
	gridLayout->addItem(verticalSpacer_3, 6, 2, 1, 1);

	verticalSpacer_2 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);
	gridLayout->addItem(verticalSpacer_2, 4, 2, 1, 1);

	horizontalSpacer_6 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	gridLayout->addItem(horizontalSpacer_6, 0, 0, 7, 1);

	horizontalSpacer_4 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	gridLayout->addItem(horizontalSpacer_4, 5, 3, 1, 1);

	groupBoxOrdenes = new QGroupBox(gridLayoutWidget);
	sizePolicy.setHeightForWidth(groupBoxOrdenes->sizePolicy().hasHeightForWidth());
	groupBoxOrdenes->setSizePolicy(sizePolicy);
	groupBoxOrdenes->setMaximumSize(QSize(375, 80));
	groupBoxOrdenes->setStyleSheet(
			"QGroupBox\n"
			"{\n"
			"border: 0.5px solid gray;\n"
			"border-radius: 2px;\n"
			"margin-top: 0.5em;\n"
			"}\n"
			"QGroupBox::Title\n"
			"{\n"
			"subcontrol-origin: margin;\n"
			"left: 10px;\n"
			"padding: 0 3px 0 3px;\n"
			"}"
	);
	groupBoxOrdenes->setTitle(QApplication::translate("TurtlePanel", "Ordenes", 0));
	groupBoxOrdenes->setAlignment(Qt::AlignHCenter|Qt::AlignVCenter);

	horizontalLayoutWidget_2 = new QWidget(groupBoxOrdenes);
	horizontalLayoutWidget_2->setGeometry(QRect(10, 20, 281, 51));

	horizontalLayout_2 = new QHBoxLayout(horizontalLayoutWidget_2);
	horizontalLayout_2->setSpacing(6);
	horizontalLayout_2->setContentsMargins(11, 11, 11, 11);
	horizontalLayout_2->setContentsMargins(0, 0, 0, 0);

	horizontalSpacer_2_0 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	horizontalLayout_2->addItem(horizontalSpacer_2_0);

	horizontalLayout_2->addWidget(botonCargar);
	horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);

	horizontalLayout_2->addItem(horizontalSpacer_2);
	horizontalLayout_2->addWidget(botonSalir);

	horizontalLayout_2->setStretch(0, 3);
	horizontalLayout_2->setStretch(1, 10);
	horizontalLayout_2->setStretch(2, 1);
	horizontalLayout_2->setStretch(3, 10);

	gridLayout->addWidget(groupBoxOrdenes, 5, 2, 1, 1);

	verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);
	gridLayout->addItem(verticalSpacer, 2, 1, 1, 3);

	textBrowser = new QTextBrowser(gridLayoutWidget);
	//MOD 02/10/16 PARA CAMBIAR COLOR DE LETRA Y FONDO
	textBrowser->setObjectName("textBrowser");
	textBrowser->setAccessibleName("textBrowser");
	textBrowser->setAlignment(Qt::AlignJustify);
	textBrowser->setStyleSheet("#textBrowser {color: rgb(255,255,255); background-color: rgb(0,10,145);}");
	gridLayout->addWidget(textBrowser, 7, 1, 1, 3);

	gridLayout->setRowStretch(0, 1);
	gridLayout->setRowStretch(1, 20);
	gridLayout->setRowStretch(2, 1);
	gridLayout->setRowStretch(3, 28);
	gridLayout->setRowStretch(4, 2);
	gridLayout->setRowStretch(5, 28);
	gridLayout->setRowStretch(6, 1);
	gridLayout->setRowStretch(7, 73);
	gridLayout->setColumnStretch(0, 1);
	gridLayout->setColumnStretch(1, 1);
	gridLayout->setColumnStretch(2, 500);
	gridLayout->setColumnStretch(3, 1);
	gridLayout->setColumnStretch(4, 1);

	setLayout(gridLayout);

	clienteLista = nhLista.serviceClient<std_srvs::Trigger>("activa_dock");
	clienteProductos = nhProductos.serviceClient<std_srvs::Trigger>("salida_dock");

	batTurtlebot = cbTurtle.subscribe<diagnostic_msgs::DiagnosticArray>("/diagnostics", 1, &PanelCarga::obtenerBateriaTurtlebot,this);
	batPortatil = cbPortatil.subscribe<smart_battery_msgs::SmartBatteryStatus>("/laptop_charge", 1, &PanelCarga::obtenerBateriaPortatil,this);

	serverCarga = srvCarga.advertiseService("bloquea_botones_carga", &PanelCarga::recibeMensajesCarga, this);

	connect(botonCargar, SIGNAL(clicked()), this, SLOT(manejadorBotonCarga()));
	connect(botonSalir, SIGNAL(clicked()), this, SLOT(manejadorBotonSalir()));

	imprimeInstrucciones();

}

void PanelCarga::manejadorBotonCarga()
{
	system("rosservice call /activa_dock &");
	botonCargar->setEnabled(false);
}

void PanelCarga::manejadorBotonSalir()
{
	system("rosservice call /salida_dock &");
	botonCargar->setEnabled(true);
}

void PanelCarga::save(rviz::Config config) const
{
	rviz::Panel::save(config);
}

void PanelCarga::load(const rviz::Config& config)
{
	rviz::Panel::load(config);
}

void PanelCarga::obtenerBateriaTurtlebot(const diagnostic_msgs::DiagnosticArray::ConstPtr& diagnostico)
{
	if(strcmp(diagnostico->status[0].hardware_id.c_str(),"Kobuki")==0)
		nivelTurtlebot = atof(diagnostico->status[0].values[1].value.c_str());

	// Comprobamos el nivel de carga
	if(nivelTurtlebot >= 50)
	{
		bateriaTurtlebot->setStyleSheet("QProgressBar {border: 2px solid grey;border-radius: 5px;text-align: center;}"
								   	   	"QProgressBar::chunk {background-color: #00FF00;width: 10px;margin: 0.5px;}");
	}
	else
	{
		if(nivelTurtlebot > 20)
		{
			//BATERÍA AMARILLA
			bateriaTurtlebot->setStyleSheet("QProgressBar {border: 2px solid grey;border-radius: 5px;text-align: center;}"
							     	   	   	"QProgressBar::chunk {background-color: #FFFF00;width: 10px;margin: 0.5px;}");
		}
		else
		{
			bateriaTurtlebot->setStyleSheet("QProgressBar {border: 2px solid grey;border-radius: 5px;text-align: center;}"
									   	   	"QProgressBar::chunk {background-color: #FF0000;width: 10px;margin: 0.5px;}");
		}
	}

	bateriaTurtlebot->setValue(nivelTurtlebot);
}

//CUANDO PORTÁTIL TOSHIBA ESTÁ CONECTADO AL TURTLEBOT
void PanelCarga::obtenerBateriaPortatil(const smart_battery_msgs::SmartBatteryStatus::ConstPtr& diagnostico)
{
	nivelPortatil = diagnostico->percentage;

	// Comprobamos el nivel de carga
	if(nivelPortatil >= 50)
	{
		bateriaPortatil->setStyleSheet("QProgressBar {border: 2px solid grey;border-radius: 5px;text-align: center;}"
									   "QProgressBar::chunk {background-color: #00FF00;width: 10px;margin: 0.5px;}");
	}
	else
	{
		if(nivelPortatil > 20)
		{
			bateriaPortatil->setStyleSheet("QProgressBar {border: 2px solid grey;border-radius: 5px;text-align: center;}"
							     	 	   "QProgressBar::chunk {background-color: #FFFF00;width: 10px;margin: 0.5px;}");
		}
		else
		{
			bateriaPortatil->setStyleSheet("QProgressBar {border: 2px solid grey;border-radius: 5px;text-align: center;}"
										   "QProgressBar::chunk {background-color: #FF0000;width: 10px;margin: 0.5px;}");
		}
	}

	bateriaPortatil->setValue(nivelPortatil);
}

bool PanelCarga::recibeMensajesCarga(programa_central::mensajes::Request &req, programa_central::mensajes::Response &res)
{
	switch(req.cmd)
	{
		//Bloquear todos los botones
		case 5:
			botonCargar->setEnabled(false);
			botonSalir->setEnabled(false);
			break;
		//Liberar todos los botones
		case 6:
			botonCargar->setEnabled(true);
			botonSalir->setEnabled(true);
			break;
	}
	return true;
}

void PanelCarga::imprimeInstrucciones()
{
	textBrowser->append("INSTRUCCIONES");
	textBrowser->append("--------------------------------------------------------------------------------");
	textBrowser->append("En el panel de carga se puede realizar las siguientes acciones:\n");
	textBrowser->append("1. Pulse el boton \"Cargar\" para llevar al turtlebot a la zona de carga.\n");
	textBrowser->append("2. Pulse el boton \"Salir\" para sacar al turtlebot de la zona de carga.");
	textBrowser->append("--------------------------------------------------------------------------------\n");
}

} // fin namespace

// Tell pluginlib about this class.  Every class which should be
// loadable by pluginlib::ClassLoader must have these two lines
// compiled in its .cpp file, outside of any namespace scope.
#include <pluginlib/class_list_macros.h>
PLUGINLIB_EXPORT_CLASS(rviz_plugin_tutorials::PanelCarga, rviz::Panel)
