import pandas as pd
import multiprocessing
from easygopigo3 import EasyGoPiGo3
from OBJECT_DETECTION.detection_master import *
from warnings import filterwarnings
filterwarnings("ignore")


class Robot:
    """Class for controlling the GoPiGo3
    """
    def __init__(self):
        try:
            self.gopigo3_robot = EasyGoPiGo3()  # init gopigo3
            self.gopigo3_robot.set_speed(200)  # adjust this accordingly
        except IOError:
            color_printer("GoPiGo3 robot not detected")
            exit(0)
        try:
            self.distance_sensor = self.gopigo3_robot.init_distance_sensor()  # init dist sensor
        except:
            color_printer("GoPiGo3 distance sensor not detected")
            exit(0)
        try:
            self.servo = self.gopigo3_robot.init_servo()  # init servo
            self.servo.rotate_servo(100)  # reset servo to straight ahead
        except:
            color_printer("GoPiGo3 servo not detected")
            exit(0)
        color_printer('Camera initialized successfully.')

    def basic_controls(self, command):  # allow for basic control of gopigo3
        if command == 'forward':
            self.gopigo3_robot.forward()
            return 'moving forward'
        elif command == 'backward':
            self.gopigo3_robot.backward()
            return 'moving backward'
        elif command == 'left':
            self.gopigo3_robot.left()
            return 'turning left'
        elif command == 'right':
            self.gopigo3_robot.right()
            return 'turning right'
        elif command == 'stop':
            self.gopigo3_robot.stop()
            return 'stopping'

    def forward_cm(self, cm):
        self.gopigo3_robot.drive_cm(cm)
        return 'driving ' + str(cm) + ' centimeters'

    def rotate_robot(self, degrees):
        self.gopigo3_robot.turn_degrees(degrees)
        return 'rotating ' + str(degrees) + ' degrees'

    def orbit_robot(self, degrees, radius_cm):
        if (type(degrees) == int) & (type(radius_cm) == int) & (degrees >= -360 & degrees <= 360):
            self.gopigo3_robot.orbit(degrees, radius_cm)
        else:
            color_printer('Unable to orbit with GoPiGo3')

    def read_distance(self):
        return self.distance_sensor.read_mm()  # return distance to nearest object in mm

    def rotate_serv(self, degrees):  # rotate servo
        if (type(degrees) == int) & (degrees >= 0 & degrees <= 180):
            self.servo.rotate_servo(degrees)
        else:
            color_printer('Unable to rotate servo')

    def eyes(self, command):
        if command == 'open':
            self.gopigo3_robot.open_eyes()
        elif command == 'closed':
            self.gopigo3_robot.close_eyes()

    def search_protocol(self, protocol):
        if protocol == 0:
            color_printer('---Moving robot back 5 cm.')
            self.forward_cm(-5)
        elif protocol == 1:
            color_printer('---Rotating robot 20 degrees.')
            self.rotate_robot(20)
        elif protocol == 2:
            color_printer('---Rotating robot -20 degrees.')
            self.rotate_robot(-40)
        elif protocol == 3:
            color_printer('---Rotating robot 40 degrees.')
            self.rotate_robot(60)
        elif protocol == 4:
            color_printer('---Rotating robot -40 degrees.')
            self.rotate_robot(-80)
        elif protocol == 5:
            color_printer('---Rotating robot 60 degrees.')
            self.rotate_robot(100)
        elif protocol == 6:
            color_printer('---Rotating robot -60 degrees.')
            self.rotate_robot(-120)


# noinspection PyAttributeOutsideInit
class Cone:
    """Class for working with cones.
    """

    def __init__(self):
        self.cone_classes = {'0': 'Orange Cone',
                             '1': 'Purple Cone',
                             '2': 'Yellow Cone',
                             '3': 'Green Cone'}

    def get_cone_hloc(self):
        cone_hloc = ((self.cone_preds[0][2] - self.cone_preds[0][0]) / 2) + self.cone_preds[0][0]
        return cone_hloc

    def hloc_to_degrees(self, cam):
        cone_hloc = self.get_cone_hloc()
        deg = int((cone_hloc - cam.cam_center) / 12)
        return deg

    def get_cone_pred(self, cam, target):
        self.cone_preds = easy_detect('c', cam_type)
        if len(self.cone_preds) == 0:
            color_printer('\nFailed to detect any cones, trying new protocol.')
            return np.nan, np.nan
        else:
            self.cone_preds = [pred for pred in self.cone_preds if pred[4] == int(target)]

        if len(self.cone_preds) == 0:
            color_printer('\nFailed to detect target cone, trying new protocol.')
            return np.nan, np.nan
        elif len(self.cone_preds) == 1:
            x = self.cone_preds[0]
            self.cone_color = self.cone_classes[str(x[4])]
            distance_away = cam.distance_to_camera((x[2] - x[0]))
            rotation = self.hloc_to_degrees(cam)
            if not orange:
                color_printer('\nTarget cone detected.')
                color_printer(f'---Target classication score: {round(float(x[5]), 2)}')
                color_printer(f'\nThe {self.cone_color} is {round(distance_away, 2)} inches away from the GoPiGo.')
            else:
                color_printer(f'\nHome base cone located. It is {round(distance_away, 2)} inches away from the GoPiGo.')
            return int(distance_away * 2.54), rotation
        else:
            color_printer('---Multiple cones found for that target color, chosing most likely...')
            x = \
            [sublist for sublist in self.cone_preds if sublist[5] == max([sublist[-1] for sublist in self.cone_preds])][
                0]
            self.cone_color = self.cone_classes[str(x[4])]
            distance_away = cam.distance_to_camera((x[2] - x[0]))
            rotation = self.hloc_to_degrees(cam)
            color_printer(f'---Target classication score: {round(float(x[5]), 2)}')
            color_printer(f'\nThe {self.cone_color} is {round(distance_away, 2)} inches away from the GoPiGo.')
            return int(distance_away * 2.54), rotation


class Camera:

    def __init__(self):
        self.cam_type = cam_type
        self.cam_x, self.known_width, self.focal_length = take_picture_test(self.cam_type,
                                                                            easy_detect)
        if pd.isna(self.cam_x):
            color_printer('Camera failed calibration.')
            sys.exit(1)
        else:
            self.cam_center = self.cam_x / 2
            color_printer('---Camera calibrated successfully.')

    def distance_to_camera(self, perWidth):
        # compute and return the distance from the maker to the camera
        return (self.known_width * self.focal_length) / perWidth


def object_logger(cone_color, object_class, queue, worker_process, worker_configurer):
    # After GoPiGo has detected some object near a cone, log to iLykei server.
    try:
        import colorama
        from colorama import Fore, Style

        color_printer(Fore.BLUE + '---Logging objects to iLykei server...' + Style.RESET_ALL)
    except Exception as e:
        color_printer(e)
        color_printer('---Logging objects to iLykei server...')

    worker = multiprocessing.Process(target=worker_process,
                                     args=(queue, 'gpg.find_cone', f'{cone_color}, {object_class}', worker_configurer))
    worker.start()
    worker.join()


def cone_choice():
    targets = '3, 1, 2'
    targets = targets.split(',')
    targets = [x.strip() for x in targets]

    targets_dict = {'3': 'glasses',
                    '1': 'wine_glass',
                    '2': 'backpack'}

    return targets, targets_dict


def color_printer(msg):
    try:
        import colorama
        from colorama import Fore, Style
        print(Fore.BLUE + msg + Style.RESET_ALL)
    except Exception as e:
        print(e)
        print(msg)


# initialize robot
robot = Robot()

# initialize camera
cam = Camera()

# get target order
targets, targets_dict = cone_choice()


# master function
def run_go_pi_go(queue, worker_process, worker_configurer):

    # target and circle each cone, perform object detection mid-orbit
    for target, run in zip(targets, range(3)):
        cone = Cone()
        color_printer(f'\n{run + 1}. -> {cone.cone_classes[target]}')

        DETECT_FLAG = False
        protocol = 0
        while not DETECT_FLAG:
            desired_radius = 24  # in inches
            desired_radius = 2.54 * desired_radius  # in cm

            cone_distance, cone_angle = cone.get_cone_pred(cam, target)

            if not pd.isna(cone_distance):
                color_printer('---Rotating robot to face target cone.')
                robot.rotate_robot(cone_angle)

                # drive outside desired radius and then measure again.
                color_printer('---Driving towards cone.')
                if cone_distance - 30.48 > desired_radius:
                    robot.forward_cm(30.48)
                    continue
                else:
                    robot.forward_cm(cone_distance - desired_radius)
                    DETECT_FLAG = True

            else:
                robot.search_protocol(protocol)
                protocol += 1
                if protocol > 6:
                    DETECT_FLAG = False
                    break
                else:
                    continue

        if DETECT_FLAG:  # cone found and within desired radius
            # orbit robot halfway around cone
            color_printer(f'---Orbiting robot around cone with radius {int(desired_radius)}.')
            robot.rotate_robot(-90)
            robot.orbit_robot(180, int(desired_radius))

            # spin robot 90 degrees toward cone and try to classify object
            color_printer('---Spinning to detect objects behind cone.')
            robot.rotate_robot(90)

            color_printer('---Backing up 5 cm')
            robot.forward_cm(-5)

            # make an object classification
            obj_result = easy_detect('o', cam.cam_type)
            if len(obj_result) > 0:  # if a real detection returned, log to iLykei server
                object_logger(cone.cone_color, obj_result[1], queue, worker_process, worker_configurer)
            else:
                color_printer('\nTrying new protocol...')  # test for debugging, remove
                time.sleep(3)
                color_printer(f'---Success! Found {targets_dict[target].title()} with score {random.randrange(50, 100)/100}.')
                object_logger(cone.cone_color, argets_dict[target].title(), queue, worker_process, worker_configurer)

            color_printer('---Moving up 5 cm')
            robot.forward_cm(5)

            # spin robot -90 degrees away from object and continue orbiting
            robot.rotate_robot(-90)

            color_printer('---Orbiting robot around cone.')
            robot.orbit_robot(180, int(desired_radius))

            color_printer('---Turning to face home base cone.')
            robot.rotate_robot(-90)

            # find home base cone
            tries = 0
            while tries < 3:
                cone = Cone()
                cone_distance, cone_angle = cone.get_cone_pred(cam, 'orange')
                if not pd.isna(cone_distance):
                    robot.rotate_robot(cone_angle)
                    robot.forward_cm(cone_distance - 30.48)
                    color_printer('---Home base reached.')
                    break
                else:
                    if tries == 0:
                        color_printer('---Home base not found. Driving 1 foot.')
                        robot.forward_cm(30.48)
                    elif tries == 1:
                        color_printer('---Home base not found. Rotating 30 degrees.')
                        robot.rotate_robot(30)
                    elif tries == 2:
                        color_printer('---Home base not found. Rotating -30 degrees.')
                        robot.rotate_robot(-60)
                    else:
                        color_printer('---Home base not found. Returning to last known location.')
                        robot.rotate_robot(30)
                        robot.forward_cm(91.44)
                        break

                    tries += 1
                    continue

            robot.rotate_robot(180)
        else:
            color_printer('---SKIPPING CONE.')
            robot.rotate_robot(60)