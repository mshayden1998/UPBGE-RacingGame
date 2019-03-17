import bge
from collections import OrderedDict

if not hasattr(bge, "__component__"):
    # Setting up objects
    objects = bge.logic.getCurrentScene().objects
    car = objects["Car"]
    w0 = objects["WFL"]
    w1 = objects["WFR"]
    w2 = objects["WBL"]
    w3 = objects["WBR"]

    # Add vehicle
    carId = car.getPhysicsId()
    susp = bge.constraints.createVehicle(carId)

    keyboard = bge.logic.keyboard
    key = bge.events
    joysticks = bge.logic.joysticks

class Component(bge.types.KX_PythonComponent):
    # Put your arguments here of the format ("key", default_value).
    # These values are exposed to the UI.
    args = OrderedDict([
        ("Name", ""),
        ("Brake", 0.0),
        ("TopSpeed", 0.0),
        ("Acceleration", 0.0),
        ("SuspRestLength", 0.0),
        ("WheelRadius", 0.0),
        ("SteerLimit", 0.0)
    ])

    def start(self, args):
        # Properties
        self.topSpeed = args["TopSpeed"]
        self.acceleration = args["Acceleration"]
        self.brake = args["Brake"]
        self.steerLimit = args["SteerLimit"]

        # Add wheels
        downDir = [0,0,-1]
        axleDir = [-1,0,0]
        suspRestLength = args["SuspRestLength"]
        wheelRadius = args["WheelRadius"]
        susp.addWheel(w0, [0.82,-0.98, 0], downDir, axleDir, suspRestLength, wheelRadius, True)
        susp.addWheel(w1, [-0.82,-0.98, 0], downDir, axleDir, suspRestLength, wheelRadius, True)
        susp.addWheel(w2, [0.82,0.9, 0], downDir, axleDir, suspRestLength, wheelRadius, False)
        susp.addWheel(w3, [-0.82,0.9, 0], downDir, axleDir, suspRestLength, wheelRadius, False)

        # Set suspension properties
        r_influence = 0.05
        susp.setRollInfluence(r_influence, 0)
        susp.setRollInfluence(r_influence, 1)
        susp.setRollInfluence(r_influence, 2)
        susp.setRollInfluence(r_influence, 3)

        compression = 3.0
        susp.setSuspensionCompression(compression, 0)
        susp.setSuspensionCompression(compression, 1)
        susp.setSuspensionCompression(compression, 2)
        susp.setSuspensionCompression(compression, 3)

        damping = 12.0
        susp.setSuspensionDamping(damping, 0)
        susp.setSuspensionDamping(damping, 1)
        susp.setSuspensionDamping(damping, 2)
        susp.setSuspensionDamping(damping, 3)

        stiffness = 25.0
        susp.setSuspensionStiffness(stiffness, 0)
        susp.setSuspensionStiffness(stiffness, 1)
        susp.setSuspensionStiffness(stiffness, 2)
        susp.setSuspensionStiffness(stiffness, 3)

        friction = 15.0
        susp.setTyreFriction(friction, 0)
        susp.setTyreFriction(friction, 1)
        susp.setTyreFriction(friction, 2)
        susp.setTyreFriction(friction, 3)

    def update(self):
        # Variables
        steerVelocity = 0.05
        # Apply force fowards and backwards
        if keyboard.inputs[key.WKEY].active:
            if car["Speed"] < self.topSpeed:
                car["Speed"] += self.acceleration
        elif keyboard.inputs[key.SKEY].active:
            if car["Speed"] > -self.topSpeed:
                car["Speed"] -= self.acceleration
        else:
            car["Speed"] = 0.0

        # Steer Left and Right
        if keyboard.inputs[key.AKEY].active:
            if car["Steer"] < self.steerLimit:
                car["Steer"] += steerVelocity
        elif keyboard.inputs[key.DKEY].active:
            if car["Steer"] > -self.steerLimit:
                car["Steer"] -= steerVelocity
        else:
            car["Steer"] = 0.0

        # Apply brake force
        if keyboard.inputs[key.LEFTCTRLKEY].active:
            susp.applyBraking(self.brake, 0)
            susp.applyBraking(self.brake, 1)
        else:
            susp.applyBraking(0, 0)
            susp.applyBraking(0, 1)

        # Setters
        susp.applyEngineForce(car["Speed"], 2)
        susp.applyEngineForce(car["Speed"], 3)
        susp.setSteeringValue(car["Steer"], 0)
        susp.setSteeringValue(car["Steer"], 1)