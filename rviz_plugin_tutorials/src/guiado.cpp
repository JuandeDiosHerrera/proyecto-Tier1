
#include "guiado.h"

using namespace std;

namespace rviz_plugin_tutorials
{

//En el constructor hay que incluir algunos aspecto relacionados con Qt:
// Pasar el argumento opcional *parent* al constructor de la superclase rviz::Panel.
PanelGuiado::PanelGuiado(QWidget* parent) : rviz::Panel(parent)
{
	botonInicio = new QPushButton("Inicio", this);
	botonInicio->setToolTip("Se cargan los programas encargados del guiado.");
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

	botonEnviarObjetivos = new QPushButton("Enviar", this);
	botonEnviarObjetivos->setToolTip("Se procede a guardar la lista de la compra del cliente.");
	botonEnviarObjetivos->setCursor(QCursor(Qt::PointingHandCursor));

	botonGuiado = new QPushButton("Guiado", this);
	botonGuiado->setToolTip("Se realiza la etapa de guiado del turtlebot por el mapa.");
	botonGuiado->setCursor(QCursor(Qt::PointingHandCursor));

	centralWidget = new QWidget();
	gridLayoutWidget = new QWidget(centralWidget);
	gridLayoutWidget->setGeometry(QRect(60, 0, 331, 451));
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
	gridLayout->addWidget(label, 1, 1, 1, 3);

	horizontalSpacer_5 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	gridLayout->addItem(horizontalSpacer_5, 0, 4, 10, 1);

	groupBoxGuiado = new QGroupBox(gridLayoutWidget);
	QSizePolicy sizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);
	sizePolicy.setHorizontalStretch(0);
	sizePolicy.setVerticalStretch(0);
	sizePolicy.setHeightForWidth(groupBoxGuiado->sizePolicy().hasHeightForWidth());
	groupBoxGuiado->setSizePolicy(sizePolicy);
	groupBoxGuiado->setMaximumSize(QSize(300, 80));
	groupBoxGuiado->setStyleSheet(
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
	groupBoxGuiado->setTitle(QApplication::translate("Guide", "Guiado", 0));
	groupBoxGuiado->setAlignment(Qt::AlignHCenter);

	horizontalLayoutWidget = new QWidget(groupBoxGuiado);
	horizontalLayoutWidget->setGeometry(QRect(10, 20, 281, 51));

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

	gridLayout->addWidget(groupBoxGuiado, 3, 2, 1, 1);

	horizontalSpacer_3 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	gridLayout->addItem(horizontalSpacer_3, 5, 1, 1, 1);

	verticalSpacer_3 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);
	gridLayout->addItem(verticalSpacer_3, 6, 2, 1, 1);

	verticalSpacer_2 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);
	gridLayout->addItem(verticalSpacer_2, 4, 2, 1, 1);

	verticalSpacer_4 = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);
	gridLayout->addItem(verticalSpacer_4, 8, 2, 1, 1);

	horizontalSpacer_6 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	gridLayout->addItem(horizontalSpacer_6, 0, 0, 7, 1);

	QSizePolicy sizePolicy1(QSizePolicy::Fixed, QSizePolicy::Fixed);
	sizePolicy1.setHorizontalStretch(0);
	sizePolicy1.setVerticalStretch(0);
	sizePolicy1.setHeightForWidth(botonGuiado->sizePolicy().hasHeightForWidth());
	botonGuiado->setSizePolicy(sizePolicy1);

	gridLayout->addWidget(botonGuiado, 7, 2, 1, 1, Qt::AlignCenter);

	horizontalSpacer_4 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	gridLayout->addItem(horizontalSpacer_4, 5, 3, 1, 1);

	groupBoxLista = new QGroupBox(gridLayoutWidget);
	sizePolicy.setHeightForWidth(groupBoxLista->sizePolicy().hasHeightForWidth());
	groupBoxLista->setSizePolicy(sizePolicy);
	groupBoxLista->setMaximumSize(QSize(300, 80));
	groupBoxLista->setStyleSheet(
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
	groupBoxLista->setTitle(QApplication::translate("Shopping list", "Lista de la compra", 0));
	groupBoxLista->setAlignment(Qt::AlignHCenter|Qt::AlignVCenter);

	horizontalLayoutWidget_2 = new QWidget(groupBoxLista);
	horizontalLayoutWidget_2->setGeometry(QRect(10, 20, 281, 51));

	horizontalLayout_2 = new QHBoxLayout(horizontalLayoutWidget_2);
	horizontalLayout_2->setSpacing(6);
	horizontalLayout_2->setContentsMargins(11, 11, 11, 11);
	horizontalLayout_2->setContentsMargins(0, 0, 0, 0);

	lineEdit = new QLineEdit(horizontalLayoutWidget_2);
	horizontalLayout_2->addWidget(lineEdit);

	horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	horizontalLayout_2->addItem(horizontalSpacer_2);

	horizontalLayout_2->addWidget(botonEnviarObjetivos);

	horizontalLayout_2->setStretch(0, 15);
	horizontalLayout_2->setStretch(1, 1);
	horizontalLayout_2->setStretch(2, 5);

	gridLayout->addWidget(groupBoxLista, 5, 2, 1, 1);

	verticalSpacer = new QSpacerItem(20, 40, QSizePolicy::Minimum, QSizePolicy::Expanding);
	gridLayout->addItem(verticalSpacer, 2, 1, 1, 3);

	textBrowser = new QTextBrowser(gridLayoutWidget);
	//PARA CAMBIAR COLOR DE LETRA Y FONDO
	textBrowser->setObjectName("textBrowser");
	textBrowser->setAccessibleName("textBrowser");
	textBrowser->setAlignment(Qt::AlignJustify);
	textBrowser->setStyleSheet("#textBrowser {color: rgb(255,255,255); background-color: rgb(0,10,145);}");
	gridLayout->addWidget(textBrowser, 9, 1, 1, 3);

	//Establecemos la proporción entre las 8 filas. A mayor número en el segundo parámetro, más abarcará la fila en
	//el panel.
	gridLayout->setRowStretch(0, 1);
	gridLayout->setRowStretch(1, 20);
	gridLayout->setRowStretch(2, 1);
	gridLayout->setRowStretch(3, 28);
	gridLayout->setRowStretch(4, 2);
	gridLayout->setRowStretch(5, 28);
	gridLayout->setRowStretch(6, 1);
	gridLayout->setRowStretch(7, 13);
	gridLayout->setRowStretch(8, 1);
	gridLayout->setRowStretch(9, 73);

	//Establecemos la proporción entre las 4 columnas. A mayor número en el segundo parámetro, más abarcará la
	//columna en el panel.
	gridLayout->setColumnStretch(0, 1);
	gridLayout->setColumnStretch(1, 1);
	gridLayout->setColumnStretch(2, 500);
	gridLayout->setColumnStretch(3, 1);
	gridLayout->setColumnStretch(4, 1);

	//Establecemos como layout principal del panel el que contiene a todos los elementos: gridLayout.
	setLayout(gridLayout);

	topicProgreso = nhProgreso.subscribe("central_node_comm", 1000, &PanelGuiado::info_progreso, this);

	clientGuiado = nhGuiado.serviceClient<std_srvs::Trigger>("arranca_guiado");

	serverMsgGuiado = srvMsgGuiado.advertiseService("recibe_mensajes_guiado", &PanelGuiado::recibeMensajesGuiado, this);

	clienteLista = nhLista.serviceClient<std_srvs::Trigger>("crea_lista");
	clienteProductos = nhProductos.serviceClient<etapa_guiado::Productos>("recibe_productos");

	connect(botonInicio, SIGNAL(clicked()), this, SLOT(manejadorBotonInicio()));
	connect(botonEnviarObjetivos, SIGNAL(clicked()), this, SLOT(manejadorBotonObjetivos()));
	connect(botonGuiado, SIGNAL(clicked()), this, SLOT(manejadorBotonGuiado()));

}

void PanelGuiado::manejadorBotonInicio()
{
	clientGuiado.call(service);
}

void PanelGuiado::manejadorBotonObjetivos()
{
	std::string listaProductos = recibeProductosLista();
	std::vector<std::string> productosSeparados;

	if(listaProductos != "")
	{
		productosSeparados = separaElementos(listaProductos);
		lineEdit->clear();
	}
	else
	{
		//No se puede pasar 0 elementos
		textBrowser->setTextColor(QColor(255,0,0,255));
		textBrowser->append("\nNo ha enviado ningun producto.\n");
		textBrowser->setTextColor(QColor(255,255,255,255));
	}

	servicioProductos.request.productos.assign(productosSeparados.begin(),productosSeparados.end());

	if(clienteProductos.call(servicioProductos))
	{
		switch(servicioProductos.response.cmd)
		{
			//Limpieza de pantalla
			case 0:
				textBrowser->clear();
				break;
			//Mensajes normales
			case 1:
				textBrowser->setTextColor(QColor(255,255,255,255));
				textBrowser->append(servicioProductos.response.mensaje.c_str());
				break;
			//Instrucciones
			case 2:
				textBrowser->setTextColor(QColor(255,255,255,255));
				imprimeInstrucciones();
				break;
			//Errores
			case 3:
				textBrowser->setTextColor(QColor(255,0,0,255));
				textBrowser->append(servicioProductos.response.mensaje.c_str());
				textBrowser->setTextColor(QColor(255,255,255,255));
				break;
			//Exitos
			case 4:
				textBrowser->setTextColor(QColor(0,255,0,255));
				textBrowser->append(servicioProductos.response.mensaje.c_str());
				textBrowser->setTextColor(QColor(255,255,255,255));
				break;
			//Limpia y mensajes normales
			case 5:
				textBrowser->clear();
				textBrowser->setTextColor(QColor(255,255,255,255));
				textBrowser->append(servicioProductos.response.mensaje.c_str());
				break;
		}
	}
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

	for (std::vector<std::string>::const_iterator i = listaResultado.begin(); i != listaResultado.end(); ++i)
		cout << *i << endl;

	return listaResultado;
}

std::vector<std::string> PanelGuiado::limpiaLista(std::vector<std::string> listaSeparada)
{
	std::vector<std::string> listaResultado;

	for (int i = 0; i < listaSeparada.size(); ++i)
	{
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
					productoResultado = producto.substr(j+1);
			}

			productoResultado2 = productoResultado;

			for(int k = productoResultado.length()-1; 0 <= k; --k)
			{
				if(isalnum(productoResultado.at(k)))	//isalpha sólo para caracteres alfabéticos
					break;
				else
					productoResultado2 = productoResultado.substr(0,k);
			}

			if(productoResultado2 != "")
				listaResultado.push_back(productoResultado2);
		}
	}
	return listaResultado;
}

void PanelGuiado::manejadorBotonGuiado()
{
	textBrowser->clear();
	clienteLista.call(servicioLista);
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

//MÉTODO QUE MODIFICA EL VALOR DE LA BARRA DE PROGRESO
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
			botonEnviarObjetivos->setEnabled(false);
			botonGuiado->setEnabled(false);
			break;
		//Liberar todos los botones
		case 6:
			botonInicio->setEnabled(true);
			botonEnviarObjetivos->setEnabled(true);
			botonGuiado->setEnabled(true);
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

	//AL IMPRIMIR INSTRUCCIONES, NO ANTES, LOS BOTONES DEBEN LIBERARSE
	botonInicio->setEnabled(true);
	botonEnviarObjetivos->setEnabled(true);
	botonGuiado->setEnabled(true);
}

} // fin namespace

// Tell pluginlib about this class.  Every class which should be
// loadable by pluginlib::ClassLoader must have these two lines
// compiled in its .cpp file, outside of any namespace scope.
#include <pluginlib/class_list_macros.h>
PLUGINLIB_EXPORT_CLASS(rviz_plugin_tutorials::PanelGuiado, rviz::Panel)
