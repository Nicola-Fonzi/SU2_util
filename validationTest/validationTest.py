import os
import argparse

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-c","--clean", action="store_true",
                      help="Specify if we only want to clean the directories", dest="clean", default=False)

    parser.add_argument("-r", "--required",
                      dest="tests",
                      choices=["structure", "aeroOnly", "static", "forced", "dynamicRans", "dynamicEuler"],
                      default=["structure", "aeroOnly", "static", "forced", "dynamicRans", "dynamicEuler"],
                      nargs="+",
                      help='Regression tests required',)

    parser.add_argument("-np", "--number-processors", action="store",
                        help="Specify the number of processors", dest="np", default=10)

    args=parser.parse_args()

    HOME = os.getcwd()+"/2D-NACA0012"
    testList = []

    # Find fsi_computation.py module
    foldersInPath = os.environ['PATH'].split(':')
    for folder in foldersInPath:
        if os.path.exists(os.path.join(folder, 'fsi_computation.py')):
            execFile = os.path.join(folder, 'fsi_computation.py')
    if 'execFile' not in locals():
        raise Exception("Module fsi_computation.py not found, please add to PATH")

    if "structure" in args.tests:
        testList.append("/Structure_Only/dryRunStruct")
        testList.append("/Structure_Only/nonDiagDamp")
    if "aeroOnly" in args.tests:
        testList.append("/RANS/aeroOnly/pureSU2")
        testList.append("/RANS/aeroOnly/interface")
    if "static" in args.tests:
        testList.append("/RANS/static_aeroelasticity")
    if "forced" in args.tests:
        testList.append("/RANS/forced_sine")
    if "dynamicRans" in args.tests:
        testList.append("/RANS/dynamic_aeroelasticity/Ma01")
        testList.append("/RANS/dynamic_aeroelasticity/Ma02")
        testList.append("/RANS/dynamic_aeroelasticity/Ma03")
        testList.append("/RANS/dynamic_aeroelasticity/Ma0357")
        testList.append("/RANS/dynamic_aeroelasticity/Ma0364")
        testList.append("/RANS/dynamic_aeroelasticity/Ma02DiffRS")
    if "dynamicEuler" in args.tests:
        testList.append("/Euler/dynamic_aeroelasticity/Ma01")
        testList.append("/Euler/dynamic_aeroelasticity/Ma02")
        testList.append("/Euler/dynamic_aeroelasticity/Ma03")
        testList.append("/Euler/dynamic_aeroelasticity/Ma0357")
        testList.append("/Euler/dynamic_aeroelasticity/Ma0364")

    for test in testList:
        print("Testing now: "+test)
        os.chdir(HOME+test)
        if args.clean:
            os.system("rm *vtu FSI* Struct* log* histo*")
        else:
            if os.path.isfile("fsi.cfg"):
                os.system("mpirun -np {} python3 {} --parallel -f fsi.cfg > log.txt".format(args.np, execFile))
            elif os.path.isfile("fluid.cfg"):
                os.system("mpirun -np {} SU2_CFD fluid.cfg > log.txt".format(args.np))
            else:
                os.system("python3 runStruct.py > log.txt")
    return

if __name__ == '__main__':
    main()
