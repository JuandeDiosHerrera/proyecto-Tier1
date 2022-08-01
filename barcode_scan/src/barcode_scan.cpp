#include <ros/ros.h>
#include <math.h>
#include <image_transport/image_transport.h>
#include <sensor_msgs/LaserScan.h> // Message
#include <sensor_msgs/PointCloud2.h> // Message
#include <geometry_msgs/Transform.h> // Message
#include <pcl_ros/point_cloud.h>
#include <pcl_ros/transforms.h>
#include <pcl/point_types.h>
#include <tf/transform_listener.h> // Get tf
#include <visualization_msgs/Marker.h> // Message
#include <barcode_scan/GetBarcodes.h> // Service
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <string>

#define KINECT_FOV 1.4677
using namespace cv;

typedef pcl::PointCloud<pcl::PointXYZ> PointCloud;
static const std::string OPENCV_WINDOW = "Image window";

class BarcodeScan
{
  float distance, width, height;
  std::vector<float> obj_width, obj_height;
  geometry_msgs::Point p;
  PointCloud pc;
  tf::TransformListener tf_listener;
  visualization_msgs::Marker marker;
  ros::NodeHandle nh_;
  ros::Subscriber pc_sub; // Point cloud listener
  ros::Publisher marker_pub;
  ros::ServiceServer server;
  image_transport::ImageTransport it_;
  image_transport::Subscriber image_sub_;
  image_transport::Publisher image_pub_;
  Mat frame_gray, decolored, eq,grad_x, contrast, blurred, th, closed, out;

public:
  BarcodeScan() : it_(nh_)
  {
    // Subscrive to input video feed and publish output video feed
    image_sub_ = it_.subscribe("/camera/image_raw", 1, &BarcodeScan::imageCb, this);
    image_pub_ = it_.advertise("/image_converter/output_video", 1);

    pc_sub = nh_.subscribe("/camera/depth/points",1,&BarcodeScan::pclCb,this);
	marker_pub = nh_.advertise<visualization_msgs::Marker>("visualization_marker",10);
	//namedWindow(OPENCV_WINDOW,WINDOW_NORMAL);

	server = nh_.advertiseService("get_barcodes", &BarcodeScan::sendBarcodes, this);

	marker.header.frame_id = "/camera_link";
	marker.ns = "basic_shapes";
	marker.id = 0;
	marker.type = visualization_msgs::Marker::POINTS;
	marker.action = visualization_msgs::Marker::ADD;
	marker.pose.position.x = 0;
	marker.pose.position.y = 0;
	marker.pose.position.z = 0;
	marker.pose.orientation.x = 0.0;
	marker.pose.orientation.y = 0.0;
	marker.pose.orientation.z = 0.0;
	marker.pose.orientation.w = 1.0;
	marker.scale.x = 0.05;
	marker.scale.y = 0.05;
	marker.scale.z = 0.05;
	marker.color.r = 1.0f;
	marker.color.g = 0.0f;
	marker.color.b = 1.0f;
	marker.color.a = 1.0f;
	marker.frame_locked = true;	
	marker.lifetime = ros::Duration();	
  }

  ~BarcodeScan()
  {
    //destroyWindow(OPENCV_WINDOW);
  }

  void imageCb(const sensor_msgs::ImageConstPtr& msg)
  {
    cv_bridge::CvImagePtr cv_ptr;
    try
    {
      cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
    }
    catch (cv_bridge::Exception& e)
    {
      ROS_ERROR("cv_bridge exception: %s", e.what());
      return;
    }

    // Update GUI Window
	cv_ptr->image = BarcodeScan::detectAndDisplay(cv_ptr->image);
	//imshow(OPENCV_WINDOW,cv_ptr->image);
	waitKey(1);

    // Output modified video stream
    image_pub_.publish(cv_ptr->toImageMsg());
  }
  void pclCb(const PointCloud& msg)
  {
	tf::StampedTransform s_transform; // This is the tf taken from ros
	Eigen::Matrix4f tf; // This is the tf matrix for pcl

	try{
	// We try to get the tf from ros and send error if something fails
		tf_listener.lookupTransform("/camera_link","/camera2_depth_optical_frame", ros::Time(0),s_transform);
	}
	catch(tf::TransformException &ex){
		ROS_ERROR("%s",ex.what());
		ros::Duration(1.0).sleep();
	}
	
	// Convert stamped transform into basic transform
	tf::Transform transform(s_transform.getBasis(),s_transform.getOrigin());
	
	// Convert transform into pcl matrix
	pcl_ros::transformAsMatrix(transform,tf);
	
	// Transform pcl into new tf
	pcl::transformPointCloud(msg,pc,tf);
	if(!pc.isOrganized())
	{
		ROS_ERROR("The pointcloud is not organized\n");
	}
}
  Mat detectAndDisplay(Mat frame)
  {
	
	// Get the image dimensions from this camera
	width = frame.cols;
	height = frame.rows;

	// Change to gray
	cvtColor(frame, frame_gray, COLOR_BGR2GRAY);
	
	// Compute the Scharr gradiente representation
	// We only want the horizontal gradient
	Scharr(frame_gray,grad_x, CV_16S, 1,0);
	convertScaleAbs(grad_x, grad_x);
	
	// Smooth the img   erererre
	blur(grad_x, blurred, Size(21,3));
	
	// Threshold
	threshold(blurred, th,120,255, THRESH_BINARY);	
	
	// Close shapes 
	Mat kernel = getStructuringElement(MORPH_RECT, Size(9,9)); 
	morphologyEx(th, closed, MORPH_CLOSE, kernel);
	
	// Erode and dilate
	kernel = getStructuringElement(MORPH_RECT, Size(9,3));
	erode(closed, out, kernel, Point(-1,-1), 3);
	dilate(out,out, kernel, Point(-1,-1),3);	
	
	// Find contours
	vector<vector<Point> > contours;
	vector<Vec4i> hierarchy;
	findContours(out, contours,RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);
	
	vector<RotatedRect> minRect(contours.size());
	
	// Get rectangles
	for(size_t i = 0; i < contours.size(); i++)
	{
		minRect[i] = minAreaRect(contours[i]);
	}
	marker.points.clear();
	// Draw rectangles and coordinates
	for(size_t i = 0; i<contours.size(); i++)
	{
		Point2f rect_points[4];
		minRect[i].points(rect_points);
		for(int j = 0; j < 4; j++)
		{
			line(frame, rect_points[j], rect_points[(j+1)%4], Scalar(0,255,0), 1);
		}
		Point2d center = minRect[i].center; // Center of rectangle
		putText(frame, format("(%.0f,%.0f)",center.x, center.y), minRect[i].center , FONT_HERSHEY_DUPLEX, 0.5, Scalar(0,255,0),1);
		
		// Translate from rgb image resolution to pcl resolution
		int x = center.x*pc.width/width;
		int y = center.y*pc.height/height;
		
		// Store the points to publish
		if(pc.isOrganized() && !(isnan(pc.at(x,y).x)) )
		{
			p.x = pc.at(x,y).x;
			p.y = pc.at(x,y).y;
			p.z = pc.at(x,y).z;
			marker.points.push_back(p);
			obj_width.push_back(minRect[i].size.width);
			obj_height.push_back(minRect[i].size.height);
		}
	}	
	//imshow(OPENCV_WINDOW,frame);
	marker.header.stamp = ros::Time::now();
	marker_pub.publish(marker);
	return frame;
  }
  bool sendBarcodes(barcode_scan::GetBarcodes::Request &req, barcode_scan::GetBarcodes::Response &res)
  {
	res.count = marker.points.size();
	for(int i = 0; i<marker.points.size();i++)
	{
		res.x.push_back(marker.points[i].x);
		res.y.push_back(marker.points[i].y);
		res.z.push_back(marker.points[i].z);
		res.width.push_back(obj_width[i]);
		res.height.push_back(obj_height[i]);
	}
	ROS_INFO("Sending back %d points",(int)res.count);
	return true;
  }

};

int main(int argc, char** argv)
{
  ros::init(argc, argv, "barcode_scan");
  BarcodeScan bs;
  ros::spin();
  return 0;
}
