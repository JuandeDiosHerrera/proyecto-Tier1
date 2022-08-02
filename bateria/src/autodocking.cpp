#include <iostream>
#include <ros/ros.h>
#include <diagnostic_msgs/DiagnosticArray.h>
#include <vector>
#include <kobuki_msgs/AutoDockingAction.h>
#include <actionlib/client/simple_action_client.h>
#include <std_srvs/Trigger.h>


using namespace std;

#define DOCKING_ACTION "dock_drive_action"
#define BAT_MIN 20

typedef actionlib::SimpleActionClient<kobuki_msgs::AutoDockingAction> DockingClient;

DockingClient* gDockingClient;

class Autodock
{
public:
	//Constructor
	Autodock();
	//Funciones
	bool sautodock(std_srvs::Trigger::Request  &req, std_srvs::Trigger::Response  &res);
	bool szonadock(std_srvs::Trigger::Request  &req, std_srvs::Trigger::Response  &res);
	bool AutoDock();
	bool ZonaDock();

private:
	ros::NodeHandle s1,s2;

	ros::ServiceServer autodock, zonadock;
};

Autodock::Autodock()
{
	cout << "Ya esta listo el servicio de autodock" << endl;

	autodock = s1.advertiseService("autodock", &Autodock::sautodock, this);
	zonadock = s2.advertiseService("zonadock", &Autodock::szonadock, this);
}

bool Autodock::sautodock(std_srvs::Trigger::Request  &req, std_srvs::Trigger::Response  &res)
{
	bool estado = false;

	ZonaDock();
	estado = AutoDock();

	return estado;
}

bool Autodock::szonadock(std_srvs::Trigger::Request  &req, std_srvs::Trigger::Response  &res)
{
	ZonaDock();

	return true;
}

bool Autodock::AutoDock()
{
	kobuki_msgs::AutoDockingGoal goal;

	gDockingClient->sendGoal(goal);
	cout << "Enviando robot a la zona de carga..." << endl;

	gDockingClient->waitForResult(ros::Duration(160.0));

	if(gDockingClient->getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
	{
		//Se ha alcanzado la base
		cout << "Robot cargando" << endl;
		return true;
	}
	else
	{
		//Hemos tardado más de 60 segundos en alcanzar la base
		cout << "Error al alcanzar el dock" << endl;
		gDockingClient->cancelGoal();
		return false;
	}
}

bool Autodock::ZonaDock()
{
	//Funcion para llevar al robot a una zona cercana a la base de carga

	return true;
}


int main(int argc, char **argv)
{
	ros::init(argc, argv, "Nodo_Autodock");

	gDockingClient = new DockingClient(DOCKING_ACTION, true);
	gDockingClient->waitForServer();

	Autodock dock;

	ros::spin();

	return 0;
}
