#ifndef PANEL_MAPEO_H
#define PANEL_MAPEO_H

#ifndef Q_MOC_RUN
# include <ros/ros.h>

# include <rviz/panel.h>

#include <QPushButton>

#include <std_srvs/Trigger.h>
#include "std_msgs/String.h"

//Añadidos por mí --> ui
#include <QGroupBox>
#include <QLocale>
#include <QVariant>
#include <QAction>
#include <QApplication>
#include <QButtonGroup>
#include <QFrame>

#include <QHeaderView>
#include <QWidget>

#include <QPainter>
#include <QLineEdit>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QTimer>

#include <QPushButton>
#include <QProgressBar>

#include <QSpacerItem>

/* 19/07/16 */
#include <QMainWindow>
#include <QMenuBar>
#include <QStatusBar>
#include <QTextBrowser>
#include <QToolBar>
//FIN Añadidos por mí --> ui

#include "programa_central/mensajes.h"
#include "etapa_guiado/Productos.h"

#endif

class QLineEdit;

namespace rviz_plugin_tutorials
{

class DriveWidget;

// BEGIN_TUTORIAL
// Here we declare our new subclass of rviz::Panel.  Every panel which
// can be added via the Panels/Add_New_Panel menu is a subclass of
// rviz::Panel.
class PanelGuiado: public rviz::Panel
{
// This class uses Qt slots and is a subclass of QObject, so it needs
// the Q_OBJECT macro.
	Q_OBJECT
public:
	// QWidget subclass constructors usually take a parent widget
	// parameter (which usually defaults to 0).  At the same time,
	// pluginlib::ClassLoader creates instances by calling the default
	// constructor (with no arguments).  Taking the parameter and giving
	// a default of 0 lets the default constructor work and also lets
	// someone using the class for something else to pass in a parent
	// widget as they normally would with Qt.
	PanelGuiado(QWidget* parent = 0);

	// Now we declare overrides of rviz::Panel functions for saving and
	// loading data from the config file.
	virtual void load(const rviz::Config& config);
	virtual void save(rviz::Config config) const;

	// Next come a couple of public Qt slots.
public Q_SLOTS:

	/*MOD*/
	void manejadorBoton1();
	void manejadorBoton2();
	void manejadorBoton3();
	void manejadorBoton4();
	void manejadorBoton5();
	void manejadorBoton5_1();

	bool recibeMensajesGuiado(programa_central::mensajes::Request &req, programa_central::mensajes::Response &res);
	void imprimeInstrucciones();

	std::string recibeProductosLista();
	std::vector<std::string> separaElementos(std::string listaProductos);
	std::vector<std::string> limpiaLista(std::vector<std::string> listaSeparada);

	//FUNCIÓN QUE CONTROLA LAS BARRAS DE PROGRESO.
	void info_progreso(const std_msgs::String::ConstPtr& str);

	//MOD BOTÓN DE SALIDA DE PROGRAMA
	//void manejadorBotonSalida();

	/*FIN MOD*/

	// Here we declare some internal slots.
protected Q_SLOTS:

	// Then we finish up with protected member variables.
protected:

	//Declaración de los NodeHandlers de ROS.
	ros::NodeHandle nh_topic, nh_sub;
	ros::NodeHandle nh1, nh2, nh3, nh4, nh5, nh5_1, nh_salir;
	ros::Publisher pub_topic;
	ros::Subscriber sub_topic;

	ros::ServiceClient client1, client2, client3, client4, client5, client5_1,
			client_salir;

	std_srvs::Trigger service;

	ros::ServiceServer serverMsgGuiado;
	ros::NodeHandle srvMsgGuiado;

	ros::NodeHandle nhLista, nhProductos;
	ros::ServiceClient clienteLista, clienteProductos;
	etapa_guiado::Productos servicioProductos;
	std_srvs::Trigger servicioLista;

	// The latest velocity values from the drive widget.
	float linear_velocity_;
	float angular_velocity_;

	 QWidget *centralWidget;
	    QWidget *gridLayoutWidget;
	    QGridLayout *gridLayout;
	    QSpacerItem *horizontalSpacer_5;
	    QGroupBox *groupBox;
	    QWidget *horizontalLayoutWidget;
	    QHBoxLayout *horizontalLayout;
	    QPushButton *pushButton;
	    QSpacerItem *horizontalSpacer;
	    QProgressBar *progressBar;
	    QSpacerItem *horizontalSpacer_3;
	    QSpacerItem *verticalSpacer_3;
	    QSpacerItem *verticalSpacer_2;
	    QSpacerItem *verticalSpacer_4;
	    QSpacerItem *horizontalSpacer_6;
	    QPushButton *pushButton_3;
	    QSpacerItem *horizontalSpacer_4;
	    QGroupBox *groupBox_2;
	    QWidget *horizontalLayoutWidget_2;
	    QHBoxLayout *horizontalLayout_2;
	    QLineEdit *lineEdit;
	    QSpacerItem *horizontalSpacer_2;
	    QPushButton *pushButton_2;
	    QSpacerItem *verticalSpacer;
	    QTextBrowser *textBrowser;
	    QMenuBar *menuBar;
	    QToolBar *mainToolBar;
	    QStatusBar *statusBar;
	// END_TUTORIAL
};

} // end namespace rviz_plugin_tutorials

#endif // PANEL_MAPEO_H
