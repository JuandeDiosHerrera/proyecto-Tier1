
#include "mapeo.h"

using namespace std;

namespace rviz_plugin_tutorials
{

PanelMapeo::PanelMapeo(QWidget* parent) : rviz::Panel(parent)
{
	botonInicio = new QPushButton("Inicio", this);
	botonInicio->setToolTip("Se cargan los programas de mapeo y se realiza el mapeado inicial.");
	botonInicio->setCursor(QCursor(Qt::PointingHandCursor));
	botonInicio->setStyleSheet(QLatin1String(
	      "QPushButton {"
	      "color: rgb(255,255,255);"
	      "background-color: rgb(0, 255, 0);"
	      "border-style: outset;"
	      "border-width: 2px;"
	      "border-radius: 10px;"
	      "border-color: rgb(127, 127, 127);"
	      "font: bold 14px;"
	      "min-width: 5em;"
	      "padding: 6px;"
	      "}"
	      "QPushButton:pressed {"
	      "background-color: rgb(0, 224, 0);"
	      "border-style: inset;"
	      "}"
	));

	botonExplorar = new QPushButton("Explorar", this);
	botonExplorar->setToolTip("Se escanea la zona y se guarda el mapa en este ordenador.");
	botonExplorar->setCursor(QCursor(Qt::PointingHandCursor));

	botonTeleop = new QPushButton("Teleoperar", this);
	botonTeleop->setToolTip("Control manual del robot.");
	botonTeleop->setCursor(QCursor(Qt::PointingHandCursor));

	botonCancelExp = new QPushButton("Cancelar", this);
	botonCancelExp->setToolTip("Cancela la exploracion");
	botonCancelExp->setCursor(QCursor(Qt::PointingHandCursor));

	botonCancelTeleop = new QPushButton("Cancelar", this);
	botonCancelTeleop->setToolTip("Cancela el control manual.");
	botonCancelTeleop->setCursor(QCursor(Qt::PointingHandCursor));

	centralWidget = new QWidget();
	gridLayoutWidget = new QWidget(centralWidget);
	gridLayoutWidget->setGeometry(QRect(40, 10, 351, 431));
	gridLayout = new QGridLayout(gridLayoutWidget);
	gridLayout->setSpacing(6);
	gridLayout->setContentsMargins(11, 11, 11, 11);
	gridLayout->setContentsMargins(0, 0, 0, 0);

	verticalSpacer_5 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);
	gridLayout->addItem(verticalSpacer_5, 0, 2, 1, 1);

	//DIRECCIÓN DEL LOGO DE COMERZZIA Y AICIA
	userHome = getenv("HOME");
	char logo[256];
	strcpy(logo, userHome);
	strcat(logo, "/catkin_ws/src/interfaz/rviz_plugin_tutorials/icons/classes/comerzzia_aicia.png");

	//LABEL PARA VISUALIZAR EL LOGO DE COMERZZIA Y EL DE AICIA
	label = new QLabel(gridLayoutWidget);
	label->setPixmap(QPixmap(QString::fromUtf8(logo)));
	label->setAlignment(Qt::AlignCenter);
	gridLayout->addWidget(label, 1, 0, 1, 4);

	groupBoxMapeo = new QGroupBox(gridLayoutWidget);
	groupBoxMapeo->setMaximumSize(QSize(380, 85));
	QSizePolicy sizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);
	sizePolicy.setHorizontalStretch(0);
	sizePolicy.setVerticalStretch(0);
	sizePolicy.setHeightForWidth(groupBoxMapeo->sizePolicy().hasHeightForWidth());
	groupBoxMapeo->setSizePolicy(sizePolicy);
	groupBoxMapeo->setStyleSheet(QLatin1String(
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
	));
	groupBoxMapeo->setTitle(QApplication::translate("Mapping", "Mapeado", 0));
	groupBoxMapeo->setAlignment(Qt::AlignHCenter);

	horizontalLayoutWidget = new QWidget(groupBoxMapeo);
	horizontalLayoutWidget->setGeometry(QRect(10, 20, 271, 51));

	horizontalLayout = new QHBoxLayout(horizontalLayoutWidget);
	horizontalLayout->setSpacing(6);
	horizontalLayout->setContentsMargins(11, 11, 11, 11);
	horizontalLayout->setContentsMargins(0, 0, 0, 0);

	horizontalLayout->addWidget(botonInicio);

	horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	horizontalLayout->addItem(horizontalSpacer);

	progressBar = new QProgressBar(horizontalLayoutWidget);
	progressBar->setValue(0);
	horizontalLayout->addWidget(progressBar);

	//PROPORCIÓN ENTRE COLUMNAS DEL LAYOUT HORIZONTAL
	horizontalLayout->setStretch(0, 5);
	horizontalLayout->setStretch(1, 1);
	horizontalLayout->setStretch(2, 10);

	gridLayout->addWidget(groupBoxMapeo, 3, 1, 1, 2);

	groupBoxExploracion = new QGroupBox(gridLayoutWidget);
	groupBoxExploracion->setMaximumSize(QSize(200, 120));
	groupBoxExploracion->setStyleSheet(QLatin1String(
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
	));
	groupBoxExploracion->setTitle(QApplication::translate("Exploration", "Exploracion", 0));

	gridLayoutWidget_3 = new QWidget(groupBoxExploracion);
	gridLayoutWidget_3->setGeometry(QRect(10, 20, 131, 80));

	gridLayout_3 = new QGridLayout(gridLayoutWidget_3);
	gridLayout_3->setSpacing(6);
	gridLayout_3->setContentsMargins(11, 11, 11, 11);
	gridLayout_3->setContentsMargins(0, 0, 0, 0);

	horizontalSpacer_4 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	gridLayout_3->addItem(horizontalSpacer_4, 0, 0, 2, 1);

	gridLayout_3->addWidget(botonCancelExp, 1, 1, 1, 1);
	gridLayout_3->addWidget(botonExplorar, 0, 1, 1, 1);

	horizontalSpacer_5 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	gridLayout_3->addItem(horizontalSpacer_5, 0, 2, 2, 1);

	gridLayout->addWidget(groupBoxExploracion, 5, 1, 1, 1);

	groupBoxTeleop = new QGroupBox(gridLayoutWidget);
	groupBoxTeleop->setMaximumSize(QSize(200, 120));
	groupBoxTeleop->setLayoutDirection(Qt::LeftToRight);
	groupBoxTeleop->setAutoFillBackground(false);
	groupBoxTeleop->setStyleSheet(QLatin1String(
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
	));
	groupBoxTeleop->setTitle(QApplication::translate("Teleoperation", "Teleoperacion", 0));
	groupBoxTeleop->setInputMethodHints(Qt::ImhNone);
	groupBoxTeleop->setAlignment(Qt::AlignCenter);

	gridLayoutWidget_2 = new QWidget(groupBoxTeleop);
	gridLayoutWidget_2->setGeometry(QRect(10, 20, 131, 80));

	gridLayout_2 = new QGridLayout(gridLayoutWidget_2);
	gridLayout_2->setSpacing(6);
	gridLayout_2->setContentsMargins(11, 11, 11, 11);
	gridLayout_2->setContentsMargins(0, 0, 0, 0);

	gridLayout_2->addWidget(botonCancelTeleop, 1, 1, 1, 1);

	horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	gridLayout_2->addItem(horizontalSpacer_2, 0, 0, 2, 1);

	gridLayout_2->addWidget(botonTeleop, 0, 1, 1, 1);

	horizontalSpacer_3 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	gridLayout_2->addItem(horizontalSpacer_3, 0, 2, 2, 1);

	gridLayout->addWidget(groupBoxTeleop, 5, 2, 1, 1);

	verticalSpacer_2 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);
	gridLayout->addItem(verticalSpacer_2, 6, 1, 1, 2);

	textBrowser = new QTextBrowser(gridLayoutWidget);
	textBrowser->setObjectName("textBrowser");
	textBrowser->setAccessibleName("textBrowser");
    textBrowser->setAlignment(Qt::AlignJustify);
    textBrowser->setStyleSheet("#textBrowser {color: rgb(255,255,255); background-color: rgb(0,10,145);}");
	gridLayout->addWidget(textBrowser, 7, 1, 1, 2);

	verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);
	gridLayout->addItem(verticalSpacer, 4, 1, 1, 2);

	horizontalSpacer_6 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	gridLayout->addItem(horizontalSpacer_6, 0, 0, 6, 1);

	verticalSpacer_3 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);
	gridLayout->addItem(verticalSpacer_3, 2, 1, 1, 2);

	horizontalSpacer_7 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	gridLayout->addItem(horizontalSpacer_7, 0, 3, 6, 1);

	//PROPORCIÓN ENTRE FILAS.
    gridLayout->setRowStretch(0, 1);
	gridLayout->setRowStretch(1, 20);
	gridLayout->setRowStretch(2, 1);
	gridLayout->setRowStretch(3, 28);
	gridLayout->setRowStretch(4, 2);
	gridLayout->setRowStretch(5, 28);
	gridLayout->setRowStretch(6, 2);
	gridLayout->setRowStretch(7, 73);

	//PROPORCIÓN ENTRE COLUMNAS.
	gridLayout->setColumnStretch(0, 1);
	gridLayout->setColumnStretch(1, 10);
	gridLayout->setColumnStretch(2, 10);
	gridLayout->setColumnStretch(3, 1);

	setLayout(gridLayout);

	//Metodología para enviar y recibir información desde programa_central mediante topics.
	topicProgreso = nhProgreso.subscribe("central_node_comm", 1000, &PanelMapeo::info_progreso, this);

	clientMapeo = nhMapeo.serviceClient<std_srvs::Trigger>("arranca_mapeo_ini");
	clientExploracion = nhExploracion.serviceClient<std_srvs::Trigger>("arranca_exploracion");
	clientTeleop = nhTeleop.serviceClient<std_srvs::Trigger>("arranca_teleop");
	clientCancelTeleop = nhCancelTeleop.serviceClient<std_srvs::Trigger>("cancela_teleop");
	clientCancelExplora = nh_CancelExplora.serviceClient<std_srvs::Trigger>("metodo_Cancela");

	serverMsgMapeo = srvMsgMapeo.advertiseService("recibe_mensajes_mapeo", &PanelMapeo::recibeMensajesMapeo, this);

	connect(botonInicio, SIGNAL(clicked()), this, SLOT(manejadorbotonInicio()));
	connect(botonExplorar, SIGNAL(clicked()), this, SLOT(manejadorbotonExplorar()));
	connect(botonTeleop, SIGNAL(clicked()), this, SLOT(manejadorbotonTeleop()));
	connect(botonCancelExp, SIGNAL(clicked()), this, SLOT(manejadorbotonCancelExp()));
	connect(botonCancelTeleop, SIGNAL(clicked()), this, SLOT(manejadorbotonCancelTeleop()));

}

void PanelMapeo::manejadorbotonInicio()
{
	//USANDO SERVICIO arranca_mapeo_ini
	clientMapeo.call(service);
}

void PanelMapeo::manejadorbotonExplorar()
{
	//USANDO SERVICIO arranca_exploracion
	clientExploracion.call(service);
}

void PanelMapeo::manejadorbotonTeleop()
{
	//USANDO SERVICIO arranca_teleop
	clientTeleop.call(service);
}

void PanelMapeo::manejadorbotonCancelTeleop()
{
	//USANDO SERVICIO cancela_teleop
	clientCancelTeleop.call(service);
}

void PanelMapeo::manejadorbotonCancelExp()
{
  if(clientCancelExplora.call(service))
    {
      textBrowser->setTextColor(QColor(0,255,0,255));
      textBrowser->append("\nExploracion cancelada con exito.\n");
      textBrowser->setTextColor(QColor(255,255,255,255));
    }
  else
    {
      textBrowser->setTextColor(QColor(255,0,0,255));
      textBrowser->append("\nError al intentar cancelar la exploracion.\n");
      textBrowser->setTextColor(QColor(255,255,255,255));
    }

}

void PanelMapeo::save(rviz::Config config) const
{
	rviz::Panel::save(config);
}

void PanelMapeo::load(const rviz::Config& config)
{
	rviz::Panel::load(config);
}

//MÉTODO QUE MODIFICA EL VALOR DE LA BARRA DE PROGRESO (POSIBLE MEJORA)
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

bool PanelMapeo::recibeMensajesMapeo(programa_central::mensajes::Request &req, programa_central::mensajes::Response &res)
{
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
		//Éxitos
		case 4:
			textBrowser->setTextColor(QColor(0,255,0,255));
			textBrowser->append(req.mensaje.c_str());
			textBrowser->setTextColor(QColor(255,255,255,255));
			break;
		//Bloquear todos los botones
		case 5:
			botonInicio->setEnabled(false);
			botonExplorar->setEnabled(false);
			botonTeleop->setEnabled(false);
			botonCancelExp->setEnabled(false);
			botonCancelTeleop->setEnabled(false);
			break;
		//Liberar todos los botones
		case 6:
			botonInicio->setEnabled(true);
			botonExplorar->setEnabled(true);
			botonTeleop->setEnabled(true);
			botonCancelExp->setEnabled(true);
			botonCancelTeleop->setEnabled(true);
			break;
		//Bloquear todos los botones, salvo los de teleoperación
		case 7:
			botonInicio->setEnabled(false);
			botonExplorar->setEnabled(false);
			//botonTeleop->setEnabled(false);
			botonCancelExp->setEnabled(false);
			break;
		//Bloquear todos los botones, salvo el de cancelar exploración
		case 8:
			botonInicio->setEnabled(false);
			botonExplorar->setEnabled(false);
			botonTeleop->setEnabled(false);
			botonCancelTeleop->setEnabled(false);
			break;
	}
	return true;
}

void PanelMapeo::imprimeInstrucciones()
{
	textBrowser->append("INSTRUCCIONES");
	textBrowser->append("------------------------------------------------------------------");
	textBrowser->append("Elija si desea explorar automaticamente el mapa o dirigir al turtlebot de manera manual:\n");
	textBrowser->append("a) Pulse el boton \"Explorar\" de la seccion \"Exploracion\" para realizar la exploracion automatica. "
						"Pulse \"Cancelar\" para cancelar la exploracion.\n");
	textBrowser->append("b) Pulse el boton \"Teleoperar\" de la seccion \"Teleoperacion\" para realizar la exploracion manual. "
						"Pulse \"Cancelar\" para cancelar el control manual.\n");
	textBrowser->append("Si desea guardar el mapa, pase a la etapa de localizacion de productos.");
	textBrowser->append("------------------------------------------------------------------\n");
}

} // fin namespace

#include <pluginlib/class_list_macros.h>
PLUGINLIB_EXPORT_CLASS(rviz_plugin_tutorials::PanelMapeo, rviz::Panel)
