#!/bin/bash

#Author: Phichayut Siripis (phichayut.nine@gmail.com)
PARENTDIR=$(realpath ..)
BASEDIR=$(pwd)
BMARK=${1:-multiply}
CONFIG=${2:-DefaultConfig}
CORE="ROCKET Core"

# Check & Prepare Environment
lines=$(find ${PARENTDIR} -name "*${CONFIG}" | wc -l)
if [ $lines -eq 0 ]; then
    echo "Cannot find emulator with $CONFIG in the parrent directory"
    exit 1
fi

lines=$(find ${PARENTDIR}/generated-src -name "*${CONFIG}.json" | wc -l)
if [ $lines -eq 0 ]; then
    echo "Cannot find $CONFIG in the ${PARENTDIR}/generated-src directory"
    exit 1
fi

pip3 install PTable > /dev/null
rm -rf ${BASEDIR}/{output/$BMARK*,profiling,summary,variable.json} && mkdir -p ${BASEDIR}/{output,profiling,summary}

echo "
$(date +'%Y-%B-%d %T %Z')

-------------------------------------------------------------
------------ Rocket-Chip Emulator summary script ------------
--------------- Version: 0.1 (6 August 2018) ----------------
-------------------------------------------------------------

    Core: ${CORE}
    For program: ${BMARK}
    Using config: ${CONFIG}

"

#Hardlink program to output folder
ln -fs ${RISCV}/riscv64-unknown-elf/share/riscv-tests/benchmarks/${BMARK}.riscv ${BASEDIR}/output/${BMARK}.riscv

#Show Configuration

./script-src/show-emulator-info.py $(find ${PARENTDIR}/generated-src/*${CONFIG}.json)

#Start Emulating + Show total time to run the emulator

echo "
Total time to run emulator"
time { ${PARENTDIR}/emulator-freechips.rocketchip.system-${CONFIG} +max-cycles=100000000 +verbose ${BASEDIR}/output/${BMARK}.riscv 3>&1 1>&2 2>&3 | ${RISCV}/bin/spike-dasm > ${BASEDIR}/output/${BMARK}.riscv.out && [ $PIPESTATUS -eq 0 ] ; } 2> ${BASEDIR}/output/${BMARK}.out
echo ""

#Prepare Assembly Result
./script-src/prepare-asm.py ${BASEDIR}/output/${BMARK}.riscv.out

#Summarize
for file in $(find ${BASEDIR}/profiling/*); do
    ./script-src/summarize_asm.py $file &
done
#Wait and Show output

wait

for file in $(find ${BASEDIR}/summary/*); do
    cat $file
done

rm -rf variable.json