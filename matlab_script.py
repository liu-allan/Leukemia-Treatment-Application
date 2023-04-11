import matlab.engine

"""
bsa - Body Surface Area, float
numCycles - Number of cycles to run
dosage - mg
ANC_measurements - (Absolute Neutrophil Count / Litre) x 1e9

Sample Call: 

runModel(1.71, 3.0, [50.0, 70.0], [2.1, 2.0, 2.3])

Given 2 previous dosages and ANC measurements and one new measurement (2.3), find the anticipatory dosage.
runModel will automatically follow the reactive dosage strategy, therefore we do not need 3 dosages.

The outputs are all lists of length 21*numCycles*1000

"""
def runModel(bsa, numCycles, dosage, ANC_measurements):
    
    eng = matlab.engine.start_matlab()
    s = eng.genpath('Leukemia-Treatment-Project')
    eng.addpath(s, nargout=0)
    time, nominal_trajectory, linearized_trajectory, reactive_trajectory, anticipatory_trajectory, reactive_dosage, anticipatory_dosage = eng.runController(bsa, numCycles, dosage, ANC_measurements, nargout=7)
    eng.quit()

    indices = [i for i in range(0, len(time) - len(time) % 100, 100)]
    
    time = [time[i][0] for i in indices]
    reactive_trajectory = [reactive_trajectory[i][0] for i in indices]
    anticipatory_trajectory = [anticipatory_trajectory[i][0] for i in indices]
    reactive_dosage = [reactive_dosage[i][0] for i in indices]
    anticipatory_dosage = [anticipatory_dosage[i][0] for i in indices]

    return time, nominal_trajectory, linearized_trajectory, reactive_trajectory, anticipatory_trajectory, reactive_dosage, anticipatory_dosage