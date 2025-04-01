class checkAngleVariation(): 
    def __init__(self, angles:list, holdAngles:list, time):
        self.angles = angles
        self.holdangles = holdAngles
        self.speedLimits = [6.4, 2.4, 6.5,10.15,6.15,10.15] # rad/s this parameter could be lowered --> spped limit 1.15°/s
        self.deltaT = time # seconds 
    
    def _angleVariation(self):
        variation = {}

        for i in range(len(self.angles)):
            if abs(self.angles[i] - self.holdangles[i])/self.deltaT > self.speedLimits[i]:
                variation[i+1] = False
            else:
                variation[i+1] = True
        return variation
    
    def checkVariation(self):
        variation = self._angleVariation()
        highVariations = []
        for key, value in variation.items():
            if value == False:
                highVariations.append(key)
        return highVariations, self.holdangles




