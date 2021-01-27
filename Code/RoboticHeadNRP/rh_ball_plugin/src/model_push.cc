#include <functional>
#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>
#include <ignition/math/Vector3.hh>
#include <thread>
#include "ros/ros.h"
#include "ros/callback_queue.h"
#include "ros/subscribe_options.h"
#include "std_msgs/Float32.h"
#include <gazebo/transport/transport.hh>
#include <gazebo/msgs/msgs.hh>

namespace gazebo
{
  class ModelPush : public ModelPlugin
  {
    public: void Load(physics::ModelPtr _parent, sdf::ElementPtr /*_sdf*/)
    {
      // Store the pointer to the model
      this->model = _parent;

      // Listen to the update event. This event is broadcast every
      // simulation iteration.
      this->updateConnection = event::Events::ConnectWorldUpdateBegin(
          std::bind(&ModelPush::OnUpdate, this));

      // Create a topic name
      std::string x_speed_topicName = "/x_speed";
      std::string y_speed_topicName = "/y_speed";
      std::string z_speed_topicName = "/z_speed";


      // Initialize ros, if it has not already been initialized.
      if (!ros::isInitialized())
      {
        int argc = 0;
        char **argv = NULL;
        ros::init(argc, argv, "rh_ball_rosnode",
            ros::init_options::NoSigintHandler);
      }

      // Create our ROS node. This acts in a similar manner to
      // the Gazebo node
      this->rosNode.reset(new ros::NodeHandle("rh_ball_rosnode"));

      // x_speed
      ros::SubscribeOptions so =
        ros::SubscribeOptions::create<std_msgs::Float32>(
            x_speed_topicName,
            1,
            boost::bind(&ModelPush::OnRosMsg_x_speed, this, _1),
            ros::VoidPtr(), &this->rosQueue);
      this->rosSub = this->rosNode->subscribe(so);

      // Spin up the queue helper thread.
      this->rosQueueThread =
        std::thread(std::bind(&ModelPush::QueueThread, this));

      // y_speed
      ros::SubscribeOptions so2 =
        ros::SubscribeOptions::create<std_msgs::Float32>(
            y_speed_topicName,
            1,
            boost::bind(&ModelPush::OnRosMsg_y_speed, this, _1),
            ros::VoidPtr(), &this->rosQueue2);
      this->rosSub2 = this->rosNode->subscribe(so2);

      // Spin up the queue helper thread.
      this->rosQueueThread2 =
        std::thread(std::bind(&ModelPush::QueueThread2, this));

      // z_speed
      ros::SubscribeOptions so3 =
        ros::SubscribeOptions::create<std_msgs::Float32>(
            z_speed_topicName,
            1,
            boost::bind(&ModelPush::OnRosMsg_z_speed, this, _1),
            ros::VoidPtr(), &this->rosQueue3);
      this->rosSub3 = this->rosNode->subscribe(so3);

      // Spin up the queue helper thread.
      this->rosQueueThread3 =
        std::thread(std::bind(&ModelPush::QueueThread3, this));

      ROS_WARN("Loaded ModelPush Plugin with parent...%s", this->model->GetName().c_str());
    }

    // Called by the world update start event
    public: void OnUpdate()
    {
      // Apply a small linear velocity to the model.
      this->model->SetLinearVel(ignition::math::Vector3d(x_axis_speed, y_axis_speed, z_axis_speed));
    }

    public: void SetXSpeed(const double &_x_speed_msg)
    {
      this->x_axis_speed = _x_speed_msg;
      ROS_WARN("x_axis_speed >> %f", this->x_axis_speed);
    }

    public: void SetYSpeed(const double &_y_speed_msg)
    {
      this->y_axis_speed = _y_speed_msg;
      ROS_WARN("y_axis_speed >> %f", this->y_axis_speed);
    }

    public: void SetZSpeed(const double &_z_speed_msg)
    {
      this->z_axis_speed = _z_speed_msg;
      ROS_WARN("z_axis_speed >> %f", this->z_axis_speed);
    }

    public: void OnRosMsg_x_speed(const std_msgs::Float32ConstPtr &_msg)
    {
      this->SetXSpeed(_msg->data);
    }

    /// \brief ROS helper function that processes messages
    private: void QueueThread()
    {
      static const double timeout = 0.01;
      while (this->rosNode->ok())
      {
        this->rosQueue.callAvailable(ros::WallDuration(timeout));
      }
    }

    public: void OnRosMsg_y_speed(const std_msgs::Float32ConstPtr &_msg)
    {
      this->SetYSpeed(_msg->data);
    }

    /// \brief ROS helper function that processes messages
    private: void QueueThread2()
    {
      static const double timeout = 0.01;
      while (this->rosNode->ok())
      {
        this->rosQueue2.callAvailable(ros::WallDuration(timeout));
      }
    }

    public: void OnRosMsg_z_speed(const std_msgs::Float32ConstPtr &_msg)
    {
      this->SetZSpeed(_msg->data);
    }

    /// \brief ROS helper function that processes messages
    private: void QueueThread3()
    {
      static const double timeout = 0.01;
      while (this->rosNode->ok())
      {
        this->rosQueue3.callAvailable(ros::WallDuration(timeout));
      }
    }

    // Pointer to the model
    private: physics::ModelPtr model;

    // Pointer to the update event connection
    private: event::ConnectionPtr updateConnection;

    // initialization of the speed variables
    double x_axis_speed = 0.0;
    double y_axis_speed = 0.0;
    double z_axis_speed = 0.0;

    /// \brief A node use for ROS transport
    private: std::unique_ptr<ros::NodeHandle> rosNode;

    /// \brief A ROS subscriber
    private: ros::Subscriber rosSub;
    /// \brief A ROS callbackqueue that helps process messages
    private: ros::CallbackQueue rosQueue;
    /// \brief A thread the keeps running the rosQueue
    private: std::thread rosQueueThread;

    /// \brief A ROS subscriber
    private: ros::Subscriber rosSub2;
    /// \brief A ROS callbackqueue that helps process messages
    private: ros::CallbackQueue rosQueue2;
    /// \brief A thread the keeps running the rosQueue
    private: std::thread rosQueueThread2;

    /// \brief A ROS subscriber
    private: ros::Subscriber rosSub3;
    /// \brief A ROS callbackqueue that helps process messages
    private: ros::CallbackQueue rosQueue3;
    /// \brief A thread the keeps running the rosQueue
    private: std::thread rosQueueThread3;
  };

  // Register this plugin with the simulator
  GZ_REGISTER_MODEL_PLUGIN(ModelPush)
}
