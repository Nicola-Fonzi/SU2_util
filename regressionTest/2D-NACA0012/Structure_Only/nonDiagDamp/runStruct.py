import math

CSD_ConFile = '/mnt/d/Desktop/test_NonDiagonalDamping/solid.cfg'




import pysu2_nastran
imposed_motion = 0
SolidSolver = pysu2_nastran.Solver(CSD_ConFile,imposed_motion)

deltaT = 0.001
totTime = 30.

NbTimeIter = int((totTime/deltaT)-1)
time = 0.0
TimeIter = 0


SolidSolver.setInitialDisplacements()


while TimeIter <= NbTimeIter:
	
	SolidSolver.run(time)
	SolidSolver.writeSolution(time, TimeIter, NbTimeIter)
	SolidSolver.updateSolution()
	
	TimeIter += 1
	time += deltaT