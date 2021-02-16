import os
import argparse
import subprocess

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-c","--clean", action="store_true",
                      help="Specify if we only want to clean the directories", dest="clean", default=False)

    parser.add_argument("-p","--parallel", action="store_true",
                      help="Specify if SU2 was built in parallel or not", dest="parallel", default=True)

    args=parser.parse_args()

    HOME = os.getcwd()+"/"
    testList = []

    testList.append("dynamic_NACA0012")
    testList.append("forced_NACA0012")
    testList.append("static_NACA0012")
    testList.append("restarted_NACA0012")
    testList.append("dynamic_BSCW")
    testList.append("forced_BSCW")
    testList.append("morphed_profile")
    testList.append("dryStructuralRun")

    for test in testList:
        print("Testing now: "+test)
        os.chdir(HOME+test)
        if args.clean:
            os.system("rm *vtu FSI* Struct* log* histo*")
        else:
            if not args.parallel:
                callSerialRegression(test)
                compareResults(test,"serial")
            else:
                callParallelRegression(test)
                compareResults(test,"parallel")
    return


def callSerialRegression(test):

    if os.path.isfile("fsi.cfg"):
        os.system("python3 /scratch/aero/nfonzi/SU2/bin/fsi_computation.py -f fsi.cfg > log.txt")
    elif os.path.isfile("fluid.cfg"):
        os.system("SU2_CFD fluid.cfg > log.txt")
    else:
        os.system("python3 runStruct.py > log.txt")

    return

def callParallelRegression(test):

    if os.path.isfile("fsi.cfg"):
        os.system("mpirun -np 38 python3 /scratch/aero/nfonzi/SU2/bin/fsi_computation.py --parallel -f fsi.cfg > log.txt")
    elif os.path.isfile("fluid.cfg"):
        os.system("mpirun -np 38 SU2_CFD fluid.cfg > log.txt")
    else:
        os.system("python3 runStruct.py > log.txt")

    return

def compareResults(test,mode):
    if mode=="serial"

if __name__ == '__main__':
    main()
