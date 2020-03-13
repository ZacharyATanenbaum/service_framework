#!/bin/bash

#SBATCH --job-name=SUB_PUB_INTERMEDIARY
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=64GB
#SBATCH --time=168:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=zat220@nyu.edu

module load python3/intel/3.6.3
source /home/zat220/Envs/zcorp/bin/activate

export PYTHONPATH="${PYTHONPATH}:../../libs"
export SUB_PORT=27000
export PUB_PORT=37000

/usr/bin/ssh -g -L $SUB_PORT:localhost:$SUB_PORT -f -N log-0
/usr/bin/ssh -g -L $SUB_PORT:localhost:$SUB_PORT -f -N log-1

/usr/bin/ssh -N -f -R $PUB_PORT:localhost:$PUB_PORT log-0
/usr/bin/ssh -N -f -R $PUB_PORT:localhost:$PUB_PORT log-1

unset XDG_RUNTIME_DIR
if [ "$SLURM_JOBTMP" != "" ]; then
    export XDG_RUNTIME_DIR=$SLURM_JOBTMP
fi


cd /home/zat220/Code/zcorp/buses/pub_sub_intermediary
python main.py -s $SUB_PORT -p $PUB_PORT
