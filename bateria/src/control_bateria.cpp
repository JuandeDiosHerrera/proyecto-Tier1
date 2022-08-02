#include <iostream>
#include <ros/ros.h>
#include <diagnostic_msgs/DiagnosticArray.h>
#include <vector>
#include <kobuki_msgs/AutoDockingAction.h>
#include <kobuki_msgs/PowerSystemEvent.h>
//#include <kobuki_msgs/Sound.h>
#include <geometry_msgs/Twist.h>
#include <actionlib/client/simple_action_client.h>
#include <sos/alerta.h>
//#include <move_base_msgs/MoveBaseAction.h>
#include <std_srvs/Trigger.h>

#include <etapa_guiado/Objetivo.h>

using namespace std;

#define DOCKING_ACTION "dock_drive_action"
#define BAT_MIN 20
#define TIMEOUT 60.0



typedef actionlib::SimpleActionClient<kobuki_msgs::AutoDockingAction> DockingClient;
//typedef actionlib::SimpleActionClient<move_base_msgs::MoveBaseAction> MoveClient;

DockingClient* gDockingClient;
//MoveClient* gMoveClient;

class Bateria
{
public:
	//Constructor
	Bateria();
	//Funciones
	void Run();
	bool AutoDock();
	bool SalirDock();
	bool PosIni();
	void CompruebaServicios();
	//Callbacks
	void controlBat(const diagnostic_msgs::DiagnosticArray::ConstPtr& diagnostico);
	void callBackKobukiPower(const kobuki_msgs::PowerSystemEventConstPtr &msg);
	//Servicio
	bool activarAutoDocking(std_srvs::Trigger::Request &req, std_srvs::Trigger::Response &res);
	bool salirZonaDock(std_srvs::Trigger::Request &req, std_srvs::Trigger::Response &res);

private:
	ros::NodeHandle cb,s1,cd,pe,ad,sd,so;

	float nivel;

	bool stopRobot;
	bool salirDock;

	ros::Subscriber nivelBat;
	ros::Subscriber powerEvent;
	ros::Publisher pub_vel;
	ros::Publisher sonido;
	ros::ServiceClient alarma;
	ros::ServiceServer activaDock;
	ros::ServiceServer salidaDock;
	ros::ServiceClient servicioObjetivos;


	geometry_msgs::Twist velDock;
	kobuki_msgs::AutoDockingGoal goal;
	kobuki_msgs::PowerSystemEvent event;
	//move_base_msgs::MoveBaseGoal posIni;
	//kobuki_msgs::Sound sound;
};

Bateria::Bateria():
	stopRobot(false),
	salirDock(false),
	nivel(100)
{
	//nivelBat = cb.subscribe<diagnostic_msgs::DiagnosticArray>("/diagnostics_agg", 1, &Bateria::controlBat,this);
	nivelBat = cb.subscribe<diagnostic_msgs::DiagnosticArray>("/diagnostics", 1, &Bateria::controlBat,this);
	pub_vel = cd.advertise<geometry_msgs::Twist>("cmd_vel_mux/input/autodock", 1000);
	servicioObjetivos = so.serviceClient<etapa_guiado::Objetivo>("consigue_objetivo"); //Servicio para que el robot llegue a los objetivos
	alarma = s1.serviceClient<sos::alerta>("alarma");
	activaDock = ad.advertiseService("activa_dock", &Bateria::activarAutoDocking, this);
	salidaDock = sd.advertiseService("salida_dock", &Bateria::salirZonaDock, this);
	//sonido = so.advertise<kobuki_msgs::Sound>("/mobile_base/commands/sound", 1, true); //Topic para enviar sonidos al robot

	Run();
}

void Bateria::controlBat(const diagnostic_msgs::DiagnosticArray::ConstPtr& diagnostico)
{


	if(strcmp(diagnostico->status[0].hardware_id.c_str(),"Kobuki")==0){

		nivel = atof(diagnostico->status[0].values[1].value.c_str());
		cout << diagnostico->status[0].name << ": "<< nivel << endl;

	}



	if(strcmp(diagnostico->status[0].values[4].value.c_str(),"Dock")==0){
		cout << " El robot se encuentra en la base de carga " << endl;
		stopRobot = true;

	}
	else{
		cout << " El robot esta fuera de la base de carga " << endl;
	}

}

bool Bateria::activarAutoDocking(std_srvs::Trigger::Request &req, std_srvs::Trigger::Response &res){

	cout << " Se ha recibido peticion para llevar al robot a la base de carga " << endl;

	res.success = PosIni();

	if(res.success == true){
		res.success = AutoDock();

		if(res.success == true)
			res.message = " Se ha llegado a la base de carga";
		else
			res.message = " Ha habido un problema al hacer AutoDocking. No se ha alcanzado el Dock";
	}
	else
		res.message = " Ha habido un problema al hacer AutoDocking. No se ha alcanzado la posicion inicial";



	return true;

}



bool Bateria::salirZonaDock(std_srvs::Trigger::Request &req, std_srvs::Trigger::Response &res){

	cout << " Se ha recibido peticion para sacar al robot de la base de carga " << endl;

	if(stopRobot == true){

		stopRobot = false;

		salirDock = true;
		res.success = SalirDock();
		salirDock = false;

		if(res.success == true)
			res.message = " Se ha salido de la base de carga";
		else
			res.message = " No se ha posido salir de la base de carga correctamente";

	}
	else
		res.message = " El robot no se encuentra en la base de carga";

	return res.success;

}


void Bateria::Run()
{
	sos::alerta code;

	while(ros::ok())
	{
/*
		if (nivel < BAT_MIN)
		{
			cout << " La bateria esta por debajo del 94% " << endl;
			code.request.codigo = 1;
			alarma.call(code);

			PosIni();
			AutoDock(); //Llamamos a la funcion para que el robot vaya a la plataforma de carga

			break;
		}
		else
		{
			cout << " La bateria esta por encima del 94% " << endl;
		}
*/

		// Si se tiene orden de parar el robot, se para.
		if((stopRobot == true)&&(salirDock == false)){
			cout << " El robot esta inmovilizado en la base de carga" << endl;
			velDock.linear.x = 0;
			velDock.linear.y = 0;
			velDock.linear.z = 0;

			velDock.angular.x = 0;
			velDock.angular.y = 0;
			velDock.angular.z = 0;

			pub_vel.publish(velDock);
		}

		ros::Duration(0.5).sleep(); //Consultamos el nivel de bateria cada X segundos
		ros::spinOnce();
	}
}

bool Bateria::AutoDock()
{
	gDockingClient->sendGoal(goal);
	cout << " Enviando robot a la zona de carga..." << endl;

	gDockingClient->waitForResult(ros::Duration(TIMEOUT));

	if(gDockingClient->getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
	{
		//Se ha alcanzado la base
		cout << " Robot cargando" << endl;
		return true;
	}
	else
	{
		//Hemos tardado más de 60 segundos en alcanzar la base
		cout << " Error al alcanzar el dock" << endl;
		gDockingClient->cancelGoal();
		return false;
	}
}



bool Bateria::SalirDock()
{

	// Sale marca atras durante 1 segundo
	cout << " Saliendo hacia atras de la base de carga " << endl;


	double inicio = ros::Time::now().toSec();
	double total;

	while(total < 0.5){

		velDock.linear.x = -0.3; //Velocidad intermedia hacia atras en X
		velDock.linear.y = 0;
		velDock.linear.z = 0;

		velDock.angular.x = 0;
		velDock.angular.y = 0;
		velDock.angular.z = 0;

		pub_vel.publish(velDock);

		total = ros::Time::now().toSec() - inicio;
	}

	cout << " Done! " << endl;

	// Una vez alejado, se manda a la posicion inicial
	return PosIni();;
}

bool Bateria::PosIni()
{
	std::cout << " Moviendo a la posicion inicial ..." << std::endl;

	//Preparamos la peticion al servidor
	etapa_guiado::Objetivo msgobjetivo;

	msgobjetivo.request.objetivox = 0;
	msgobjetivo.request.objetivoy = 0;
	msgobjetivo.request.objetivoyaw = 0;

	cout << " Llamando al servidor de objetivos..." << endl;


	if(servicioObjetivos.call(msgobjetivo))
		return true;
	else
		return false;



	/*

	//Creamos el mensaje
	posIni.target_pose.header.stamp = ros::Time::now();
	posIni.target_pose.header.frame_id = "map";
	posIni.target_pose.pose.position.x = 0;
	posIni.target_pose.pose.position.y = 0;
	posIni.target_pose.pose.position.z = 0;
	//posIni.target_pose.pose.orientation = gquat;
	posIni.target_pose.pose.orientation.x = 0;
	posIni.target_pose.pose.orientation.y = 0;
	posIni.target_pose.pose.orientation.z = 0;
	posIni.target_pose.pose.orientation.w = 0;

	gMoveClient->sendGoal(posIni);

	gMoveClient->waitForResult(ros::Duration(TIMEOUT));

	if(gMoveClient->getState() == actionlib::SimpleClientGoalState::SUCCEEDED)
	{
		//Se ha alcanzado la base
		cout << " Se ha alcanzado la posicion inicial" << endl;
		return true;
	}
	else
	{
		//Hemos tardado más de 60 segundos en alcanzar la base
		cout << " Error al alcanzar la posicion inicial" << endl;
		gMoveClient->cancelGoal();
		return false;
	}


	*/

}


int main(int argc, char **argv)
{
	ros::init(argc, argv, "Control_Bateria_Y_Autodocking");

	ROS_INFO(" Esperando al servicio Docking ...");

	gDockingClient = new DockingClient(DOCKING_ACTION, true);
	gDockingClient->waitForServer();

	ROS_INFO(" Ready!");

	//ROS_INFO(" Esperando al servicio move_base_docking ...");

	//gMoveClient = new MoveDockClient("move_base", true);
	//gMoveClient->waitForServer();

	//ROS_INFO(" Ready!");

	Bateria bateria;

	return 0;
}
