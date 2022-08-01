#define PI 3.141592
#define TARGET_HEIGHT 1.0
#define CAMERA_HEIGHT 0.4

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
#include <barcode_scan/GetBarcodesPTZ.h> // Service
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
  std::vector<int> x_coord;
  std::vector<int> y_coord;
  float distance, width, height, h1, h2, line_y;
  std::vector<float> obj_width, obj_height;
  geometry_msgs::Point p;
  PointCloud pc;
  tf::TransformListener tf_listener;
  visualization_msgs::Marker marker;
  ros::NodeHandle nh_;
  ros::Subscriber pc_sub, laser_sub; // Point cloud listener
  ros::Publisher marker_pub;
  ros::ServiceServer server;
  image_transport::ImageTransport it_;
  image_transport::Subscriber image_sub_;
  image_transport::Publisher image_pub_;
  Mat frame_gray, decolored, eq,grad_x, contrast, blurred, th, closed, out;
  Point2d start_line, end_line;

public:
  BarcodeScan() : it_(nh_)
  {
    // Subscrive to input video feed and publish output video feed
    image_sub_ = it_.subscribe("/camera/image_raw", 1, &BarcodeScan::imageCb, this);
    image_pub_ = it_.advertise("/image_converter/output_video", 1);
    laser_sub = nh_.subscribe("base_scan",1000,&BarcodeScan::laserCb,this);

	server = nh_.advertiseService("get_barcodes", &BarcodeScan::sendBarcodes, this);
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
	
	// Smooth the img
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
	x_coord.clear();
    y_coord.clear();
	// Draw rectangles and coordinates
	for(size_t i = 0; i<contours.size(); i++)
	{
		Point2f rect_points[4];
		minRect[i].points(rect_points);
		
		Point2d center = minRect[i].center; // Center of rectangle
		//putText(frame, format("(%.0f,%.0f)",center.x, center.y), minRect[i].center , FONT_HERSHEY_DUPLEX, 0.5, Scalar(0,255,0),1);
		
		// Translate from rgb image resolution to pcl resolution
		//int x = center.x*pc.width/width;
		//int y = center.y*pc.height/height;
		
		// Store the points to publish
		// Camera at home has a tilt angle of 30º and a vertical FOV of 40º
        h1 = CAMERA_HEIGHT + distance*tan(10*PI/180); //0.4 base height - 0.13 distance from lidar to robot center
        h2 = CAMERA_HEIGHT + distance*tan(50*PI/180);
        //h = h2 - ((float)focus_srv.request.y_coord)*(h2 - h1)/720;
        
        // Draw lines to represent target
        line_y = (h2-TARGET_HEIGHT)*720/(h2-h1);
        start_line.x = 0;
        start_line.y = line_y;
        end_line.x = 1280;
        end_line.y = line_y;
        line(frame, start_line, end_line, Scalar(0,0,255),2);
        start_line.y = line_y - 100;
        end_line.y = line_y - 100;
        line(frame, start_line, end_line, Scalar(0,0,200),1);
        start_line.y = line_y + 100;
        end_line.y = line_y + 100;
        line(frame, start_line, end_line, Scalar(0,0,200),1);
        
        if(center.y > ((int)line_y-100) && center.y < ((int)line_y+100))
        {
            for(int j = 0; j < 4; j++)
		    {
			    line(frame, rect_points[j], rect_points[(j+1)%4], Scalar(0,255,0), 1);
		    }
		    x_coord.push_back(center.x);
		    y_coord.push_back(center.y);
		    obj_width.push_back(minRect[i].size.width);
		    obj_height.push_back(minRect[i].size.height);
		}
	}	
	//imshow(OPENCV_WINDOW,frame);
	//marker.header.stamp = ros::Time::now();
	//marker_pub.publish(marker);
	return frame;
  }

  bool sendBarcodes(barcode_scan::GetBarcodesPTZ::Request &req, barcode_scan::GetBarcodesPTZ::Response &res)
  {
	res.count = x_coord.size();
	for(int i = 0; i<x_coord.size();i++)
	{
		res.x.push_back(x_coord[i]);
		res.y.push_back(y_coord[i]);
		//res.z.push_back(marker.points[i].z);
		res.width.push_back(obj_width[i]);
		res.height.push_back(obj_height[i]);
	}
	ROS_INFO("Sending back %d points",(int)res.count);
	return true;
  }

  void laserCb(const sensor_msgs::LaserScan& msg)
  {
    distance = msg.ranges[msg.ranges.size()/2];
  }


};



int main(int argc, char** argv)
{
  ros::init(argc, argv, "barcode_scan");
  BarcodeScan bs;
  ros::spin();
  return 0;
}
