import os
import argparse

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("-c","--clean", action="store_true",
                      help="Specify if we only want to clean the directories", dest="clean", default=False)

    parser.add_argument("-s","--short", action="store_true",
                      help="Specify if we only want to perform few steps for verification", dest="short", default=False)

    parser.add_argument("-r", "--required",
                      dest="tests",
                      choices=["structure","aeroOnly", "static", "forced","dynamicRans","dynamicEuler"],
                      default=["structure","aeroOnly", "static", "forced","dynamicRans","dynamicEuler"],
                      nargs="+",
                      help='Regression tests required',)

    args=parser.parse_args()

    HOME = "/scratch/aero/nfonzi/SU2_util/regressionTest/2D-NACA0012"
    testList = []

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
        os.chdir(HOME+test)
        if args.clean:
            os.system("rm *vtu FSI* Struct* log* histo*")
        elif args.short:
            if os.path.isfile("fsi_short.cfg"):
                os.system("mpirun -np 38 python3 /scratch/aero/nfonzi/SU2/bin/fsi_computation.py --parallel -f fsi_short.cfg > log.txt")
            elif os.path.isfile("fluid_short.cfg"):
                os.system("mpirun -np 38 SU2_CFD fluid_short.cfg > log.txt")
            else:
                os.system("python3 runStruct.py")
        else:
            if os.path.isfile("fsi.cfg"):
                os.system("mpirun -np 38 python3 /scratch/aero/nfonzi/SU2/bin/fsi_computation.py --parallel -f fsi.cfg > log.txt")
            elif os.path.isfile("fluid.cfg"):
                os.system("mpirun -np 38 SU2_CFD fluid.cfg > log.txt")
            else:
                os.system("python3 runStruct.py")
    return

if __name__ == '__main__':
    main()
