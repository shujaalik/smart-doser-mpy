from stepper import Stepper
import constants

class Doser:
    def __init__(self):
        self.motor = Stepper(constants.IN1, constants.IN2, constants.IN3, constants.IN4, constants.STEPS, constants.SPEED)
    
    def insert_dose(self, ml):
        self.motor.step(ml * constants.STEPS_EACH_ML)
        self.motor.release()
    
    def rotate(self, rotations):
        self.motor.step(rotations * constants.STEPS)
        self.motor.release()
        