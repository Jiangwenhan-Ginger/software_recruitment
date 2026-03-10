import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
import datetime

class TemperatureLogger(Node):
    def __init__(self, filename='temperature_log.txt'):

        super().__init__('temperature_logger')
        self.filename = filename
        
        self.subscription = self.create_subscription(
            Float32,
            'temperature',
            self.callback,
            10  
        )
        self.subscription 

    def callback(self, msg: Float32):
        temperature = msg.data
        
        if temperature >= 50.0:
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message = f"[{current_time}] warning:{temperature:.2f}°C"
            
            self.get_logger().warn(log_message)
            
            try:
                with open(self.filename, 'a', encoding='utf-8') as file:
                    file.write(log_message + '\n')
            except IOError as e:
                self.get_logger().error(f"Error: {e}")

def main(args=None):
    rclpy.init(args=args)
    
    logger_node = TemperatureLogger('pla_deformation_log.txt')
    
    rclpy.spin(logger_node)
    
    logger_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
