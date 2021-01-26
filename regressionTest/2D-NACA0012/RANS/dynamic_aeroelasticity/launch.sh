for i in Ma01 Ma02 Ma03 Ma0357 Ma0364 Ma02DIffRS
do
cd $i
mpirun -np 5 python3 /scratch/aero/nfonzi/SU2/bin/fsi_computation.py --parallel -f fsi.cfg > log.txt &
cd ..
done
