
#ifndef PANELCARGA_H
#define PANELCARGA_H

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

#include <signal.h>

#include <iostream>
#include <stdlib.h>
#include <fstream>
#include <string>
#include <cstdlib>

#include "programa_central/mensajes.h"

#endif

class QLineEdit;

namespace rviz_plugin_tutorials
{

class DriveWidget;

// BEGIN_TUTORIAL
// Here we declare our new subclass of rviz::Panel.  Every panel which
// can be added via the Panels/Add_New_Panel menu is a subclass of
// rviz::Panel.
class PanelCarga: public rviz::Panel
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
	PanelCarga(QWidget* parent = 0);

	// Now we declare overrides of rviz::Panel functions for saving and
	// loading data from the config file.
	virtual void load(const rviz::Config& config);
	virtual void save(rviz::Config config) const;

	// Next come a couple of public Qt slots.
public Q_SLOTS:

	/*MOD*/
	void manejadorBoton();

protected Q_SLOTS:

	// Then we finish up with protected member variables.
protected:
	ros::NodeHandle nh;
	ros::ServiceClient cliente;
	std_srvs::Trigger baseCarga;

    QWidget *centralWidget;
    QWidget *gridLayoutWidget;
    QGridLayout *gridLayout;
    QSpacerItem *verticalSpacer;
    QLabel *label;
    QSpacerItem *verticalSpacer_2;
    QPushButton *pushButton;
    QSpacerItem *horizontalSpacer;
    QSpacerItem *horizontalSpacer_2;
    QMenuBar *menuBar;
    QToolBar *mainToolBar;
    QStatusBar *statusBar;

    QGroupBox *groupBox;
    QWidget *horizontalLayoutWidget;
    QHBoxLayout *horizontalLayout;
    QPushButton *pushButton_2;
    QSpacerItem *horizontalSpacer_3;
    QProgressBar *progressBar;
    QSpacerItem *verticalSpacer_3;
    QTextBrowser *textBrowser;

	// END_TUTORIAL
};

} // end namespace rviz_plugin_tutorials

#endif // PANELCARGA_H
