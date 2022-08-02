
#include "brazoDkSt.h"

using namespace std;

namespace rviz_plugin_tutorials
{

PanelBrazo::PanelBrazo(QWidget* parent) : rviz::Panel(parent)
{
	botonMov1 = new QPushButton("Movimiento 1", this);
	botonMov1->setToolTip("Movimiento del brazo, no. 1");
	botonMov1->setCursor(QCursor(Qt::PointingHandCursor));

	botonMov2 = new QPushButton("Movimiento 2", this);
	botonMov2->setToolTip("Movimiento del brazo, no. 2");
	botonMov2->setCursor(QCursor(Qt::PointingHandCursor));

	botonMov3 = new QPushButton("Movimiento 3", this);
	botonMov3->setToolTip("Movimiento del brazo, no. 3");
	botonMov3->setCursor(QCursor(Qt::PointingHandCursor));

	botonMov4 = new QPushButton("Movimiento 4", this);
	botonMov4->setToolTip("Movimiento del brazo, no. 4");
	botonMov4->setCursor(QCursor(Qt::PointingHandCursor));


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

	groupBoxMovs1 = new QGroupBox(gridLayoutWidget);
	QSizePolicy sizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);
	sizePolicy.setHorizontalStretch(0);
	sizePolicy.setVerticalStretch(0);
	sizePolicy.setHeightForWidth(groupBoxMovs1->sizePolicy().hasHeightForWidth());
	groupBoxMovs1->setSizePolicy(sizePolicy);
	groupBoxMovs1->setMaximumSize(QSize(375, 80));
	groupBoxMovs1->setStyleSheet(
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
	groupBoxMovs1->setTitle(QApplication::translate("Movements", "Movimientos", 0));
	groupBoxMovs1->setAlignment(Qt::AlignHCenter);

	horizontalLayoutWidget_1 = new QWidget(groupBoxMovs1);
	horizontalLayoutWidget_1->setGeometry(QRect(10, 20, 281, 51));

	horizontalLayout_1 = new QHBoxLayout(horizontalLayoutWidget_1);
	horizontalLayout_1->setSpacing(6);
	horizontalLayout_1->setContentsMargins(11, 11, 11, 11);
	horizontalLayout_1->setContentsMargins(0, 0, 0, 0);

	horizontalSpacer = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	horizontalLayout_1->addItem(horizontalSpacer);

	horizontalLayout_1->addWidget(botonMov1);

	horizontalSpacer_1 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	horizontalLayout_1->addItem(horizontalSpacer_1);

	horizontalLayout_1->addWidget(botonMov2);

	horizontalLayout_1->setStretch(0, 3);
	horizontalLayout_1->setStretch(1, 10);
	horizontalLayout_1->setStretch(2, 1);
	horizontalLayout_1->setStretch(3, 10);

	gridLayout->addWidget(groupBoxMovs1, 3, 2, 1, 1);

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

	groupBoxMovs2 = new QGroupBox(gridLayoutWidget);
	sizePolicy.setHeightForWidth(groupBoxMovs2->sizePolicy().hasHeightForWidth());
	groupBoxMovs2->setSizePolicy(sizePolicy);
	groupBoxMovs2->setMaximumSize(QSize(375, 80));
	groupBoxMovs2->setStyleSheet(
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
	groupBoxMovs2->setTitle(QApplication::translate("Movements", "Movimientos", 0));
	groupBoxMovs2->setAlignment(Qt::AlignHCenter|Qt::AlignVCenter);

	horizontalLayoutWidget_2 = new QWidget(groupBoxMovs2);
	horizontalLayoutWidget_2->setGeometry(QRect(10, 20, 281, 51));

	horizontalLayout_2 = new QHBoxLayout(horizontalLayoutWidget_2);
	horizontalLayout_2->setSpacing(6);
	horizontalLayout_2->setContentsMargins(11, 11, 11, 11);
	horizontalLayout_2->setContentsMargins(0, 0, 0, 0);

	horizontalSpacer_2_0 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	horizontalLayout_2->addItem(horizontalSpacer_2_0);

	horizontalLayout_2->addWidget(botonMov3);

	horizontalSpacer_2 = new QSpacerItem(40, 20, QSizePolicy::Expanding, QSizePolicy::Minimum);
	horizontalLayout_2->addItem(horizontalSpacer_2);

	horizontalLayout_2->addWidget(botonMov4);

	horizontalLayout_2->setStretch(0, 3);
	horizontalLayout_2->setStretch(1, 10);
	horizontalLayout_2->setStretch(2, 1);
	horizontalLayout_2->setStretch(3, 10);

	gridLayout->addWidget(groupBoxMovs2, 5, 2, 1, 1);

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

	serverBrazo = srvBrazo.advertiseService("bloquea_botones_brazo", &PanelBrazo::recibeMensajesBrazo, this);

	connect(botonMov1, SIGNAL(clicked()), this, SLOT(manejadorBotonMov1()));
	connect(botonMov2, SIGNAL(clicked()), this, SLOT(manejadorBotonMov2()));
	connect(botonMov3, SIGNAL(clicked()), this, SLOT(manejadorBotonMov3()));
	connect(botonMov4, SIGNAL(clicked()), this, SLOT(manejadorBotonMov4()));

	imprimeInstrucciones();

}

void PanelBrazo::manejadorBotonMov1()
{
	system("rosservice call /MueveElBrazo \"{Modo: 1, X: 0.0, Y: 0.0, Z: 0.0, Pitch: 0.0}\"");
}

void PanelBrazo::manejadorBotonMov2()
{
	system("rosservice call /MueveElBrazo \"{Modo: 2, X: 0.0, Y: 0.0, Z: 0.0, Pitch: 0.0}\"");
}

void PanelBrazo::manejadorBotonMov3()
{
	system("rosservice call /MueveElBrazo \"{Modo: 1, X: 0.0, Y: 0.0, Z: 0.0, Pitch: 0.0}\"");
}

void PanelBrazo::manejadorBotonMov4()
{
	system("rosservice call /MueveElBrazo \"{Modo: 2, X: 0.0, Y: 0.0, Z: 0.0, Pitch: 0.0}\"");
}

void PanelBrazo::save(rviz::Config config) const
{
	rviz::Panel::save(config);
}

void PanelBrazo::load(const rviz::Config& config)
{
	rviz::Panel::load(config);
}

bool PanelBrazo::recibeMensajesBrazo(programa_central::mensajes::Request &req, programa_central::mensajes::Response &res)
{
	switch(req.cmd)
	{
		//Bloquear todos los botones
		case 5:
			botonMov1->setEnabled(false);
			botonMov2->setEnabled(false);
			botonMov3->setEnabled(false);
			botonMov4->setEnabled(false);
			break;
		//Liberar todos los botones
		case 6:
			botonMov1->setEnabled(true);
			botonMov2->setEnabled(true);
			botonMov3->setEnabled(true);
			botonMov4->setEnabled(true);
			break;
	}
	return true;
}

void PanelBrazo::imprimeInstrucciones()
{
	textBrowser->append("--------------------------------------------------------------------------------");
	textBrowser->append("Pulse cualquier boton para hacer que el brazo se mueva.\n");
	textBrowser->append("Cada boton tiene un efecto distinto en el brazo.");
	textBrowser->append("--------------------------------------------------------------------------------\n");
}

} // fin namespace

#include <pluginlib/class_list_macros.h>
PLUGINLIB_EXPORT_CLASS(rviz_plugin_tutorials::PanelBrazo, rviz::Panel)
