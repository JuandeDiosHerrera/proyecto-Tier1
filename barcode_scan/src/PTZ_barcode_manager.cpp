#define PI 3.141592

#include <ros/ros.h>
#include <barcode_scan/GetBarcodesPTZ.h>
#include <axis_camera/set_focus.h>
#include <std_srvs/Empty.h>
#include <zbar_ros/codes.h>
#include <axis_camera/ptz.h>
#include <math.h>
#include <std_msgs/String.h>
#include <sensor_msgs/LaserScan.h>
#include <robotnik_msgs/Axis.h>
#include <tf/transform_listener.h>
#include <position_detector/BuscaProductos.h> // BuscaProductos.srv
#include <geometry_msgs/PointStamped.h>
#include <stdio.h>
#include <iostream>
class BarcodeManager
{
	private:
		ros::NodeHandle nh;
		ros::ServiceClient client, command_client, home_client;
		ros::ServiceServer server;
		ros::Publisher pub;
		ros::Subscriber sub, laser_sub, params_sub;
		tf::TransformListener tf_listener;
		tf::StampedTransform s_transform;
		bool code_readed;
		std::string code_data, code_type;
		axis_camera::ptz command;
		barcode_scan::GetBarcodesPTZ srv;
        axis_camera::set_focus focus_srv;
        std_srvs::Empty home_srv;
		position_detector::BuscaProductos barcodes;
		geometry_msgs::PointStamped kinect_point, ptz_point, base_point, map_point;
		int productos, area_img, area_cod;
        float pan, tilt, distance, h, h1, h2, x;
	
	public:
	BarcodeManager():code_readed(false)
	{
		client = nh.serviceClient<barcode_scan::GetBarcodesPTZ>("get_barcodes");
        command_client = nh.serviceClient<axis_camera::set_focus>("focus_ptz");
        home_client = nh.serviceClient<std_srvs::Empty>("home_ptz");
		pub = nh.advertise<axis_camera::ptz>("commander",1000);
		sub = nh.subscribe("codes",1000,&BarcodeManager::codesCb,this);
        laser_sub = nh.subscribe("base_scan",1000,&BarcodeManager::laserCb,this);
        params_sub = nh.subscribe("camera_params",1000,&BarcodeManager::paramsCb,this);
		server = nh.advertiseService("barcode_manager",&BarcodeManager::zoomOnBarcodes,this);
		productos = 0;
		ROS_INFO("Requesting barcodes.");
		
	}
	bool zoomOnBarcodes(position_detector::BuscaProductos::Request &req, position_detector::BuscaProductos::Response &res)
	{
		// This service calls another service to get the position of the barcodes.
		// Then, it iterates through them to zoom in and read the information
		// Check if the service responds
        
        if(home_client.call(home_srv))
        {
		    ROS_INFO("Going back to initial position");      
        }else{
            ROS_INFO("Failed to reset camera");
        }
        
        ros::Duration(5.0).sleep();
        
		if(client.call(srv))
		{
			ROS_INFO("Received %d barcodes.", (int)srv.response.count);	
		}
		else
		{
			ROS_ERROR("The service call failed.");
			return false;
		}
		
		/*try
		{
			tf_listener.lookupTransform("/front_ptz_camera_base_link", "/camera_link",ros::Time(0),s_transform);
		}
		catch(tf::TransformException ex)
		{
			ROS_ERROR("%s",ex.what());
		}*/

		for(int i = 0; i<srv.response.count; i++)
		{
				
			
			// Apply the trasnformation of the points from kinect2 to PTZ
			/*double px = srv.response.x[i]+s_transform.getOrigin().x();
			double py = srv.response.y[i]+s_transform.getOrigin().y();
			double pz = srv.response.z[i]+s_transform.getOrigin().z();*/
			/*kinect_point.header.frame_id = "/camera_link";
			kinect_point.point.x = srv.response.x[i];
			kinect_point.point.y = srv.response.y[i];
			kinect_point.point.z = srv.response.z[i];*/
			/*tf_listener.transformPoint("/front_ptz_camera_base_link",ros::Time(0),kinect_point, "/camera_link",ptz_point);*/
			//tf_listener.transformPoint("map",ros::Time(0),srv.response)

			/*command.pan = atan2(py,px); 
			command.tilt = -atan2(pz,sqrt(px*px+py*py));
			command.relative = false*/

            // Prepara la petición para focus_ptz
		    focus_srv.request.imagewidth = 1280;
            focus_srv.request.imageheight = 720;
            focus_srv.request.imagerotation = 180;
            focus_srv.request.x_coord = srv.response.x[i];
            focus_srv.request.y_coord = srv.response.y[i];
            area_img = focus_srv.request.imagewidth*focus_srv.request.imageheight;
            area_cod = srv.response.width[i]*srv.response.height[i];
            focus_srv.request.zoom = (area_img*100)/area_cod;
            
            //h1 = 0.4 + distance*tan(0*PI/180);
            //h2 = 0.4 + distance*tan(40*PI/180);
            //h = h2 - ((float)focus_srv.request.y_coord)*(h2 - h1)/720;
            //ROS_INFO("Code height: %f",h);
            
            //ROS_INFO("Code in range.");
            if(focus_srv.request.zoom>500) focus_srv.request.zoom = 500;
			code_readed=false;
			ROS_INFO("Ready to read.");
			
			
			// Si la petición va bien, continúa
            if(command_client.call(focus_srv))
		    {
			    ROS_INFO("Aiming to target %d of %d", i+1,(int)srv.response.count);	
		    }
		    else
		    {
			    ROS_ERROR("The service call to aim failed.");
			    return false;
		    }

			ros::Duration(2.0).sleep(); 
            ros::spinOnce(); // It should spin to check the zbar msgs
            ros::Duration(2.0).sleep(); 
			if(!code_data.empty())
			    {	
				    res.data.push_back(code_data);
				    res.type.push_back(code_type);
				    ptz_point.point.x = distance+0.13; // Se le suma la distancia horizontal del lidar al centro de la base de la PTZ
			        ptz_point.point.y = -tan(pan)*ptz_point.point.x; //tan(pan) = -y/distance
			        ptz_point.point.z = tan(tilt)*ptz_point.point.x;
                    ptz_point.header.frame_id = "/front_ptz_camera_base_link";
                    ROS_INFO("El punto respecto a la camara:\n x: %f\ty: %f\tz:%f\npan:%f\ttilt:%f",ptz_point.point.x,ptz_point.point.y,ptz_point.point.z,pan,tilt);
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
				    ros::Duration(5.0).sleep();
			    }		
			code_data.clear();
                
		    res.header.stamp = ros::Time::now();
		    res.productos = productos;
		    // Goes back to initiail position
            if(home_client.call(home_srv))
            {
		        ROS_INFO("Going back to initial position");      
            }else{
                ROS_INFO("Failed to reset camera");
            }
			ros::Duration(5.0).sleep();
		}
		productos = 0;
	return true;
		
		
	}

	void codesCb(const zbar_ros::codes::ConstPtr& msg)
	{
		if(code_data!=msg->data[0].c_str() && code_readed == false)	
		{		
			code_readed=true;
			productos++;
			code_data=msg->data[0].c_str();
			code_type = msg->type[0].c_str();
			ROS_INFO("Code readed: [%s]",msg->data[0].c_str());
		}
	}

    void laserCb(const sensor_msgs::LaserScan& msg)
    {
        distance = msg.ranges[msg.ranges.size()/2];
        //ROS_INFO("%f",distance);
    }

    void paramsCb(const robotnik_msgs::Axis& msg)
    {
        pan = msg.pan;
        tilt = msg.tilt;
        //ROS_INFO("pan:%f\ttilt:%f\n",pan,tilt);
    }
};

int main(int argc, char **argv)
{
	ros::init(argc, argv, "barcode_manager");
	BarcodeManager bm;
	ros::spin();
	return 0;
}
