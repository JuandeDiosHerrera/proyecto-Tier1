
#include "localizacion.h"

using namespace std;

namespace rviz_plugin_tutorials
{

//En el constructor hay que incluir algunos aspecto relacionados con Qt:
//Pasar el argumento opcional *parent* al constructor de la superclase rviz::Panel.
PanelLocalizacion::PanelLocalizacion(QWidget* parent) : rviz::Panel(parent)
{
	botonInicio = new QPushButton("Iniciar", this);
	botonInicio->setToolTip("Se cargan los programas encargados de localizar productos en el mapa.");
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

	botonLocProductos = new QPushButton("Enviar", this);
	botonLocProductos->setToolTip("Se realiza la localizacion de los productos en el mapa.");
	botonLocProductos->setCursor(QCursor(Qt::PointingHandCursor));

	botonTeleop = new QPushButton("Teleoperar", this);
	botonTeleop->setToolTip("Control manual del robot.");
	botonTeleop->setCursor(QCursor(Qt::PointingHandCursor));

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

	//LOCALIZACIÓN DE PRODUCTOS
	groupBoxLocProd = new QGroupBox(gridLayoutWidget);
	groupBoxLocProd->setMaximumSize(QSize(380, 85));
	groupBoxLocProd->setStyleSheet(QLatin1String(
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
	groupBoxLocProd->setTitle(QApplication::translate("Locating products", "Localizacion productos", 0));

	horizontalLayoutWidget = new QWidget(groupBoxLocProd);
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

	horizontalLayout->setStretch(0, 5);
	horizontalLayout->setStretch(1, 1);
	horizontalLayout->setStretch(2, 10);

	gridLayout->addWidget(groupBoxLocProd, 3, 1, 1, 2);

	groupBoxObjetivos = new QGroupBox(gridLayoutWidget);
	groupBoxObjetivos->setMaximumSize(QSize(200, 120));
	groupBoxObjetivos->setStyleSheet(QLatin1String(
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
	groupBoxObjetivos->setTitle(QApplication::translate("Getting goals", "Obtener objetivos", 0));

	gridLayoutWidget_3 = new QWidget(groupBoxObjetivos);
	gridLayoutWidget_3->setGeometry(QRect(10, 20, 131, 80));

	gridLayout_3 = new QGridLayout(gridLayoutWidget_3);
	gridLayout_3->setSpacing(6);
	gridLayout_3->setContentsMargins(11, 11, 11, 11);
	gridLayout_3->setContentsMargins(0, 0, 0, 0);

	horizontalSpacer_4 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	gridLayout_3->addItem(horizontalSpacer_4, 0, 0, 1, 1);

	gridLayout_3->addWidget(botonLocProductos, 0, 1, 1, 1);

	horizontalSpacer_5 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	gridLayout_3->addItem(horizontalSpacer_5, 0, 2, 1, 1);

	gridLayout->addWidget(groupBoxObjetivos, 5, 1, 1, 1);

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
	gridLayout->addItem(verticalSpacer, 2, 1, 1, 2);

	horizontalSpacer_6 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	gridLayout->addItem(horizontalSpacer_6, 0, 0, 6, 1);

	verticalSpacer_3 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);
	gridLayout->addItem(verticalSpacer_3, 4, 1, 1, 2);

	horizontalSpacer_7 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	gridLayout->addItem(horizontalSpacer_7, 0, 3, 6, 1);

	//Establecemos la proporción entre las 8 filas. A mayor número en el segundo parámetro, más abarcará la fila en
	//el panel.
    gridLayout->setRowStretch(0, 1);
	gridLayout->setRowStretch(1, 20);
	gridLayout->setRowStretch(2, 1);
	gridLayout->setRowStretch(3, 28);
	gridLayout->setRowStretch(4, 2);
	gridLayout->setRowStretch(5, 28);
	gridLayout->setRowStretch(6, 2);
	gridLayout->setRowStretch(7, 73);

	//Establecemos la proporción entre las 4 columnas. A mayor número en el segundo parámetro, más abarcará la
	//columna en el panel.
	gridLayout->setColumnStretch(0, 1);
	gridLayout->setColumnStretch(1, 10);
	gridLayout->setColumnStretch(2, 10);
	gridLayout->setColumnStretch(3, 1);

	//Establecemos como layout principal del panel el que contiene a todos los elementos: gridLayout.
	setLayout(gridLayout);

	//Metodología para enviar y recibir información desde programa_central mediante topics.
	topicProgreso = nhProgreso.subscribe("central_node_comm", 1000, &PanelLocalizacion::info_progreso, this);

	clientAutoLoc = nhAutoLoc.serviceClient<std_srvs::Trigger>("autolocalizacion_locProductos");
	clientLocProductos = nhLocProductos.serviceClient<std_srvs::Trigger>("recibir_objetivos");
	clientTeleop = nhTeleop.serviceClient<std_srvs::Trigger>("arranca_teleop");
	clientCancelTeleop = nhCancelTeleop.serviceClient<std_srvs::Trigger>("cancela_teleop");

	//Servicio para recibir mensajes de la etapa de localización de productos desde progama central y mostrarlos
	//al usuario a través del textBrowser.
	serverMsgLocProd = srvMsgLocProd.advertiseService("recibe_mensajes_locProductos", &PanelLocalizacion::recibeMensajesLocProd, this);

	//Declaramos las conexiones pertinentes.
	//Las señales que activarán las conexiones serán de pulsación de botones o SIGNAL(clicked).
	//Dependiendo de qué botón se pulse se ejecutará una función manejador indicada en SLOT().
	connect(botonInicio, SIGNAL(clicked()), this, SLOT(manejadorbotonInicio()));
	connect(botonLocProductos, SIGNAL(clicked()), this, SLOT(manejadorbotonLocProductos()));
	connect(botonTeleop, SIGNAL(clicked()), this, SLOT(manejadorbotonTeleop()));
	connect(botonCancelTeleop, SIGNAL(clicked()), this, SLOT(manejadorbotonCancelTeleop()));

}

void PanelLocalizacion::manejadorbotonInicio()
{
	clientAutoLoc.call(service);
}

void PanelLocalizacion::manejadorbotonLocProductos()
{
	textBrowser->clear();
//	system("rosrun localizacion_estanterias nav_est &");
	clientLocProductos.call(service);
}

void PanelLocalizacion::manejadorbotonTeleop()
{
	clientTeleop.call(service);
}

void PanelLocalizacion::manejadorbotonCancelTeleop()
{
	clientCancelTeleop.call(service);
}

void PanelLocalizacion::save(rviz::Config config) const
{
	rviz::Panel::save(config);
}

void PanelLocalizacion::load(const rviz::Config& config)
{
	rviz::Panel::load(config);
}

//MÉTODO QUE MODIFICA EL VALOR DE LA BARRA DE PROGRESO (POSIBLE MEJORA)
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

//Función que recibe los mensajes de la etapa de localización de productos desde progama central
//y los muestra al usuario a través del textBrowser.
/* Colores(en formato rgb):
 * Blanco(QColor(255,255,255,255)) => Mensaje normal
 * Verde(QColor(0,255,0,255)) => Mensaje de éxito
 * Rojo(QColor(255,0,0,255)) => Mensaje de fallo o error
 *
 * Nota: El cuarto campo de QColor representa la transparencia de las letras:
 * 255 => Totalmente opaco
 * 0 => Totalmente transparente
 */
bool PanelLocalizacion::recibeMensajesLocProd(programa_central::mensajes::Request &req, programa_central::mensajes::Response &res)
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
		//Exitos
		case 4:
			textBrowser->setTextColor(QColor(0,255,0,255));
			textBrowser->append(req.mensaje.c_str());
			textBrowser->setTextColor(QColor(255,255,255,255));
			break;
		//Bloquear todos los botones
		case 5:
			botonInicio->setEnabled(false);
			botonLocProductos->setEnabled(false);
			botonTeleop->setEnabled(false);
			botonCancelTeleop->setEnabled(false);
			break;
		//Liberar todos los botones
		case 6:
			botonInicio->setEnabled(true);
			botonLocProductos->setEnabled(true);
			botonTeleop->setEnabled(true);
			botonCancelTeleop->setEnabled(true);
			break;
		//Bloquear todos los botones, salvo los de teleoperación
		case 7:
			botonInicio->setEnabled(false);
			botonLocProductos->setEnabled(false);
			//botonTeleop->setEnabled(false);
			break;
	}
	return true;
}

void PanelLocalizacion::imprimeInstrucciones()
{
	textBrowser->append("INSTRUCCIONES");
	textBrowser->append("------------------------------------------------------------------");
	textBrowser->append("Ahora puede enviar objetivos al robot. Para realizar esta tarea puede usar cualquiera de las siguientes opciones:\n");
	textBrowser->append("\na) Mandar los objetivos de forma automatica. Para ello, solo debe pulsar el boton \"Enviar\" sin haber mandado ningun objetivo manualmente.\n");
	textBrowser->append("\nb) Mandar los objetivos de forma manual. Para ello, siga los siguientes pasos:\n");
	textBrowser->append("1. Pulse el boton \"2D Nav Goal\" de la parte superior de la interfaz cada vez que quiera mandarle un objetivo al turtlebot.\n");
	textBrowser->append("2. Marque en el mapa los objetivos que quiere pasarle al turtlebot.\n");
	textBrowser->append("3. Una vez haya marcado todos los objetivos pulse el boton \"Enviar\" de \"Obtener Objetivos\".");
	textBrowser->append("------------------------------------------------------------------\n");

	//AL IMPRIMIR INSTRUCCIONES, NO ANTES, LOS BOTONES DEBEN LIBERARSE
	botonInicio->setEnabled(true);
	botonLocProductos->setEnabled(true);
	botonTeleop->setEnabled(true);
	botonCancelTeleop->setEnabled(true);
}

} // fin namespace

//Hay que hacer que el pluginlib sepa que existe esta clase.
//Toda clase que deba cargarse con pluginlib::ClassLoader debe tener
//las siguientes líneas compiladas en su archivo .cpp, fuera del ámbito del namespace.
#include <pluginlib/class_list_macros.h>
PLUGINLIB_EXPORT_CLASS(rviz_plugin_tutorials::PanelLocalizacion, rviz::Panel)
