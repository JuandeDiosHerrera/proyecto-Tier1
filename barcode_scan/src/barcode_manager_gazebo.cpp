#include <ros/ros.h>
#include <barcode_scan/GetBarcodes.h>
#include <zbar_ros/codes.h>
#include <axis_camera/ptz.h>
#include <math.h>
#include <std_msgs/String.h>
#include <tf/transform_listener.h>
#include <position_detector/BuscaProductos.h> // BuscaProductos.srv
#include <geometry_msgs/PointStamped.h>
class BarcodeManager
{
	private:
		ros::NodeHandle nh;
		ros::ServiceClient client;
		ros::ServiceServer server;
		ros::Publisher pub;
		ros::Subscriber sub;
		tf::TransformListener tf_listener;
		tf::StampedTransform s_transform;
		bool code_readed;
		std::string code_data, code_type;
		axis_camera::ptz command;
		barcode_scan::GetBarcodes srv;
		position_detector::BuscaProductos barcodes;
		geometry_msgs::PointStamped kinect_point, ptz_point, base_point, map_point;
		int productos;
	
	public:
	BarcodeManager():code_readed(false)
	{
		client = nh.serviceClient<barcode_scan::GetBarcodes>("get_barcodes");
		pub = nh.advertise<axis_camera::ptz>("commander",1000);
		sub = nh.subscribe("codes",1000,&BarcodeManager::codesCb,this);
		server = nh.advertiseService("barcode_manager",&BarcodeManager::zoomOnBarcodes,this);
		productos = 0;
		ROS_INFO("Requesting barcodes.");
		
	}
	bool zoomOnBarcodes(position_detector::BuscaProductos::Request &req, position_detector::BuscaProductos::Response &res)
	{
		// This service calls another service to get the position of the barcodes.
		// Then, it iterates through them to zoom in and read the information
		// Check if the service responds
		if(client.call(srv))
		{
			ROS_INFO("Received %d barcodes.", (int)srv.response.count);	
		}
		else
		{
			ROS_ERROR("The service call failed.");
			return false;
		}
		
	/*	try
		{
			tf_listener.lookupTransform("/front_ptz_camera_base_link", "/camera_link",ros::Time(0),s_transform);
		}
		catch(tf::TransformException ex)
		{
			ROS_ERROR("%s",ex.what());
		}*/

		for(int i = 0; i<srv.response.count; i++)
		{
				
			ROS_INFO("Aiming to target %d of %d", i+1,(int)srv.response.count);
			// Apply the trasnformation of the points from kinect2 to PTZ
			/*double px = srv.response.x[i]+s_transform.getOrigin().x();
			double py = srv.response.y[i]+s_transform.getOrigin().y();
			double pz = srv.response.z[i]+s_transform.getOrigin().z();*/
			kinect_point.header.frame_id = "/camera_link";
			kinect_point.point.x = srv.response.x[i];
			kinect_point.point.y = srv.response.y[i];
			kinect_point.point.z = srv.response.z[i];
			tf_listener.transformPoint("/front_ptz_camera_base_link",ros::Time(0),kinect_point, "/camera_link",ptz_point);
			//tf_listener.transformPoint("map",ros::Time(0),srv.response)
			double px = ptz_point.point.x;
			double py = ptz_point.point.y+0.05;
			double pz = ptz_point.point.z;
			command.pan = atan2(py,px); 
			command.tilt = atan2(pz,sqrt(px*px+py*py));
			command.relative = false;
				
			code_readed=false;
			ROS_INFO("Ready to read.");
			
			while(!code_readed && command.zoom <2.0)
			{
				command.zoom += 0.001; // Increase zoom until any code is readable
				pub.publish(command);
				ros::spinOnce(); // It should spin to check the zbar msgs
				ros::Duration(0.01).sleep();
			}
			res.data.push_back(code_data);
			res.type.push_back(code_type);
			// Point from the base
			try{
			tf_listener.transformPoint("/base_link",ros::Time(0),ptz_point, "/front_ptz_camera_base_link",base_point);
			res.base_x.push_back(base_point.point.x);
			res.base_y.push_back(base_point.point.y);
			res.base_z.push_back(base_point.point.z);
			}
			catch(tf::TransformException& ex){
				ROS_ERROR("Received an exception trying to transform a point from \"/front_ptz_camera_base_link\" to \"base_link\": %s", ex.what());
				res.error=1;
			}
			// Point from the map
			try{
				tf_listener.transformPoint("/map",ros::Time(0),ptz_point, "/front_ptz_camera_base_link",map_point);
				res.map_x.push_back(map_point.point.x);
				res.map_y.push_back(map_point.point.y);
				res.map_z.push_back(map_point.point.z);
			}
			catch(tf::TransformException& ex){	
				ROS_ERROR("Received an exception trying to transform a point from \"/front_ptz_camera_base_link\" to \"map\": %s", ex.what());
				res.error = 1;
			}
			ROS_INFO("Zoom finished.");
			command.zoom = 0;
		}
		res.header.stamp = ros::Time::now();
		res.productos = productos;
		productos = 0;
		// Goes back to initiail position
		command.pan = 0.0;
		command.tilt = 0.0;
		command.zoom = 0.0;
		command.relative = false;
		pub.publish(command);
		ROS_INFO("Going back to initial position");

		
		
	}
	void codesCb(const zbar_ros::codes::ConstPtr& msg)
	{
		if(code_data!=msg->data[0].c_str())	
		{		
			code_readed=true;
			productos++;
			code_data=msg->data[0].c_str();
			code_type = msg->type[0].c_str();
			ROS_INFO("Code readed: [%s]",msg->data[0].c_str());
		}
	}
};

int main(int argc, char **argv)
{
	ros::init(argc, argv, "barcode_manager");
	BarcodeManager bm;
	ros::spin();
	return 0;
}
