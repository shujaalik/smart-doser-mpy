from stepper import Stepper
import constants
from machine import Timer

class Doser:
    def __init__(self):
        self.motor = Stepper(constants.IN1, constants.IN2, constants.IN3, constants.IN4, constants.STEPS, constants.SPEED)
        self.timer = Timer(0)
        self.timer_dose = 0
    
    def insert_dose(self, ml):
        self.motor.step(ml * constants.STEPS_EACH_ML)
        self.motor.release()
    
    def rotate(self, rotations):
        self.motor.step(rotations * constants.STEPS)
        self.motor.release()
    
    def schedule_action(self, arg):
        self.insert_dose(self.timer_dose)
    
    def run_schedule(self, dose, interval, intervalValue):
        self.timer_dose = dose
        self.timer.init(period=(60 if interval == "minute" else 3600) * 1000 * intervalValue, mode=Timer.PERIODIC, callback=self.schedule_action)
    
    def stop(self):
        self.timer_dose = 0
        self.timer.deinit()
        self.motor.release()
        