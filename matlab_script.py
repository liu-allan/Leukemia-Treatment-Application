import matlab.engine
eng = matlab.engine.start_matlab()
s = eng.genpath('Leukemia-Treatment-Project')
eng.addpath(s, nargout=0)
eng.main(nargout=0)
eng.quit()