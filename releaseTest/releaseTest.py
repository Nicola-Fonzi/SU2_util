import os
import argparse
import numpy as np
import math

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-c","--clean", action="store_true",
                      help="Specify if we only want to clean the directories", dest="clean", default=False)

    parser.add_argument("-s","--serial", action="store_true",
                      help="Specify if SU2 was built in serial or not", dest="serial", default=False)

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
            if args.serial:
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

    old_fluid = []
    new_fluid = []
    old_solid = []
    new_solid = []

    new_fluid = readHistory(test+'/history.dat')
    new_fluid = readHistory(test+'/StructHistoryModal.dat')

    if mode=="serial":

        old_fluid = readHistory(test+'/ReferenceValues/history_serial.dat')
        old_solid = readHistory(test+'/ReferenceValues/StructHistoryModal_serial.dat')

    else:

        old_fluid = readHistory(test+'/ReferenceValues/history_parallel.dat')
        old_solid = readHistory(test+'/ReferenceValues/StructHistoryModal_parallel.dat')

    if len(new_fluid)>0:
        if len(old_fluid)>0:
            passed_fluid = compareHistory(old_fluid,new_fluid)
        else:
            print("Old fluid solution could not be found")
    else:
        if len(old_fluid)>0:
            print("New fluid solution could not be found")

    if len(new_solid)>0:
        if len(old_solid)>0:
            passed_solid = compareHistory(old_solid,new_solid)
        else:
            print("Old solid solution could not be found")
    else:
        if len(old_solid)>0:
            print("New solid solution could not be found")


    if passed_fluid and passed_solid:
        print("                         SUCCESS")
    else:
        print("                         FAILED")

    return


def compareHistory(D,D2):

    tol = 1e-6

    passed = True
    for key in D.keys():
        if key in D2.keys():
            old = D[key]
            new = D2[key]
    if not (math.isnan(old[0]) or math.isnan(new[0])):
        if len(old) == len(new):
            if not (abs(old-new) <= tol).all():
                passed = False
                break
        else:
            passed = False
            print('Warning: not consistent number of iterations')
            break
    elif ( (math.isnan(old[0]) and not math.isnan(new[0])) or (not math.isnan(old[0]) and math.isnan(new[0])) ):
        passed = False
        print('Warning: not consistent NAN data')
        break

    return passed

def readHistory(file):

    with open(file, 'r') as f:
        list = [[num for num in line.split(',')] for line in f if line.strip() != "" ]

    keys = list[0]
    A = np.asarray(list[1:],dtype=float)
    D = {}
    i = 0
    for key in keys:
        key = key.strip().replace('"','')
        D[key] = A[:,i]
        i += 1
    hist = D

    return hist


if __name__ == '__main__':
    main()
