import matlab.engine

def runModel(bsa, numCycles, dosage):
    
    eng = matlab.engine.start_matlab()
    s = eng.genpath('Leukemia-Treatment-Project')
    eng.addpath(s, nargout=0)
    time, nominal_trajectory, linearized_trajectory, reactive_trajectory, anticipatory_trajectory, reactive_dosage, anticipatory_dosage = eng.runController(bsa, numCycles, dosage, nargout=7)
    eng.quit()

    return time, nominal_trajectory, linearized_trajectory, reactive_trajectory, anticipatory_trajectory, reactive_dosage, anticipatory_dosage

runModel(1.71, 2.0, [50.0, 70.0])