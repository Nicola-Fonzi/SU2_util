import os
from optparse import OptionParser

def main():

    parser=OptionParser()
    parser.add_option("--clean", action="store_true",
                      help="Specify if we only want to clean the directories", dest="clean", default=False)

    HOME = "/scratch/aero/nfonzi/SU2_util/regressionTest/2D-NACA0012/RANS"
    testList = []

    testList.append("/aeroOnly/pureSU2")
    testList.append("/aeroOnly/interface")
    testList.append("/static_aeroelasticity")
    testList.append("/forced_sine")
    testList.append("/dynamic_aeroelasticity/Ma01")
    testList.append("/dynamic_aeroelasticity/Ma02")
    testList.append("/dynamic_aeroelasticity/Ma03")
    testList.append("/dynamic_aeroelasticity/Ma0357")
    testList.append("/dynamic_aeroelasticity/Ma0364")
    testList.append("/dynamic_aeroelasticity/Ma02DiffRS")

    for test in testList:
        os.chdir(HOME+test)
        if clean:
            os.system("rm *vtu FSI* Struct* log* histo*")
        else:
            if os.path.isfile("fsi.cfg"):
                os.system("mpirun -np 38 python3 /scratch/aero/nfonzi/SU2/bin/fsi_computation.py --parallel -f fsi.cfg > log.txt")
            else:
                os.system("mpirun -np 38 SU2_CFD fluid.cfg > log.txt")
    return

if __name__ == '__main__':
    main()
