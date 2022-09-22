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

    parser.add_argument("-np", "--number-processors", action="store",
                        help="Specify the number of processors", dest="np", default=10)

    args=parser.parse_args()

    HOME = os.getcwd()+"/"
    testList = []

    # Find fsi_computation.py module
    foldersInPath = os.environ['PATH'].split(':')
    for folder in foldersInPath:
        if os.path.exists(os.path.join(folder, 'fsi_computation.py')):
            fileExec = os.path.join(folder, 'fsi_computation.py')
    if 'fileExec' not in locals():
        raise Exception("Module fsi_computation.py not found, please add to PATH")

    testList.append("dynamic_NACA0012")
    testList.append("forced_NACA0012")
    testList.append("static_NACA0012")
    testList.append("restart_NACA0012")
    testList.append("dynamic_BSCW")
    testList.append("forced_BSCW")
    testList.append("morphed_profile")
    testList.append("dryStructuralRun")

    os.system("cat BSCW_mesh_aa BSCW_mesh_ab BSCW_mesh_ac BSCW_mesh_ad BSCW_mesh_ae > BSCW.tar.gz")
    os.system("tar -xf BSCW.tar.gz")
    os.system("cp coarser.su2 forced_BSCW")
    os.system("mv coarser.su2 dynamic_BSCW")
    os.system("rm BSCW.tar.gz")

    for test in testList:
        print("Testing now: "+test)
        os.chdir(HOME+test)
        if args.clean:
            os.system("rm *vtu FSI* Struct* log* histo*")
        else:
            if args.serial:
                callSerialRegression()
                if test == "restart_NACA0012":
                    os.system("mv history* history.dat")
                compareResults("serial", test)
            else:
                callParallelRegression()
                if test == "restart_NACA0012":
                    os.system("mv history* history.dat")
                compareResults("parallel", test)

    print("DONE")

    return


def callSerialRegression():

    if os.path.isfile("fsi.cfg"):
        os.system("python3 {} -f fsi.cfg > log.txt".format(args.fileExec))
    elif os.path.isfile("fluid.cfg"):
        os.system("SU2_CFD fluid.cfg > log.txt")
    else:
        os.system("python3 runStruct.py > log.txt")

    return

def callParallelRegression():

    if os.path.isfile("fsi.cfg"):
        os.system("mpirun -np {} python3 {} --parallel -f fsi.cfg > log.txt".format(args.np, args.fileExec))
    elif os.path.isfile("fluid.cfg"):
        os.system("mpirun -np {} SU2_CFD fluid.cfg > log.txt".format(args.np))
    else:
        os.system("python3 runStruct.py > log.txt")

    return

def compareResults(mode,test):

    old_fluid = {}
    new_fluid = {}
    old_solid = {}
    new_solid = {}

    if test != "dryStructuralRun":
        new_fluid = readHistory('history.dat')
    new_solid = readHistory('StructHistoryModal.dat')

    if mode=="serial":

        if test != "dryStructuralRun":
            old_fluid = readHistory('ReferenceValues/history_serial.dat')
        old_solid = readHistory('ReferenceValues/StructHistoryModal_serial.dat')

    else:

        if test != "dryStructuralRun":
            old_fluid = readHistory('ReferenceValues/history_parallel.dat')
        old_solid = readHistory('ReferenceValues/StructHistoryModal_parallel.dat')

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


    if test != "dryStructuralRun":
        if passed_fluid and passed_solid:
            print("                         SUCCESS")
        else:
            print("                         FAILED")
    else:
        if passed_solid:
            print("                         SUCCESS")
        else:
            print("                         FAILED")

    return


def compareHistory(D,D2):

    tol = 1e-6

    passed = False
    for key in D.keys():
        if key in D2.keys():
            old = D[key]
            new = D2[key]
            if len(old)>0:
                if not (math.isnan(old[0]) or math.isnan(new[0])):
                    if len(old) == len(new):
                        if not (abs(old-new) <= tol).all():
                            if np.mean(old):
                              print("The maximum error in {} was {}%".format(key,max(abs(old-new))/np.mean(old)))
                            else:
                              print("The maximum error in {} was {}".format(key,max(abs(old-new))))
                            passed = False
                            return passed
                    else:
                        passed = False
                        print('Warning: not consistent number of iterations')
                        return passed
                elif (math.isnan(old[0]) and not math.isnan(new[0])):
                    pass
                elif (not math.isnan(old[0]) and math.isnan(new[0])):
                    passed = False
                    print('Warning: not consistent NAN data')
                    return passed
                elif (math.isnan(old[0]) and math.isnan(new[0])):
                    pass
                else:
                    passed = False
                    print('I should not be here')
                    return passed
            else:
                if len(new)>0:
                    passed = False
                    print("One file was empty")
                    return passed

    passed = True
    return passed

def readHistory(file):

    with open(file, 'r') as f:
        if file=="history.dat" or file == "ReferenceValues/history_serial.dat" or file == "ReferenceValues/history_parallel.dat":
            list = [[num for num in line.strip().split(',')] for line in f if line.strip() != "" ]
        else:
            list = [[num for num in line.strip().split('\t')] for line in f if line.strip() != "" ]

    index = 0
    if len(list[0]) == 1:
        index += 1
    else:
        pass
    keys = list[index]
    A = np.zeros((len(list)-1-index,len(list[index])))
    rowA = 0
    for row in range(index+1,len(list)):
        columnA = 0
        for column in range(len(list[index])):
            A[rowA][columnA] = float(list[row][column])
            columnA += 1
        rowA += 1
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
