#!/bin/sh
#set -x

# bmminer or cgminer check

is_bmminer=`ls /usr/bin/ | grep bmminer-api | wc -l`

if [ $is_bmminer -eq 1 ]
then
	echo "Found BMMiner"

	## check if bmminer is currently running
	bmminer=`bmminer-api -o`
	if [ "${bmminer}" == "Socket connect failed: Connection refused" ]; then
		echo "BMMiner is currently not running"

		## set static values so other scripts don't error out
		elapsed=0
		ghs5s=0
		ghsav=0
		foundblocks=0
		getworks=0
		accepted=0
		rejected=0
		hw=0
		utility=0
		discarded=0
		stale=0
		localwork=0
		wu=0
		diffa=0
		diffr=0
		bestshare=0
	else
		echo "BMMiner is up and running"
	fi
else
	echo "Found CGMiner"

	## check if cgminer is currently running
	cgminer=`cgminer-api -o`
	if [ "${cgminer}" == "Socket connect failed: Connection refused" ]; then
		echo "CGMiner is currently not running"

		## set static values so other scripts don't error out
		elapsed=0
		ghs5s=0
		ghsav=0
		foundblocks=0
		getworks=0
		accepted=0
		rejected=0
		hw=0
		utility=0
		discarded=0
		stale=0
		localwork=0
		wu=0
		diffa=0
		diffr=0
		bestshare=0
	else
		echo "CGMiner is up and running"

		## set values for output for other scripts
		elapsed=${cgminer#*Elapsed=}
		elapsed=${elapsed%%,GHS 5s=*}
	fi
fi


ant_stats_tmp=`bmminer-api -o stats`
ant_tmp=`bmminer-api -o`
if [ "${ant_tmp}" == "Socket connect failed: Connection refused" ]; then
	ant_elapsed=0
	ant_ghs5s=0
	ant_ghsav=0
	ant_foundblocks=0
	ant_getworks=0
	ant_accepted=0
	ant_rejected=0
	ant_hw=0
	ant_utility=0
	ant_discarded=0
	ant_stale=0
	ant_localwork=0
	ant_wu=0
	ant_diffa=0
	ant_diffr=0
	ant_bestshare=0
else
	ant_elapsed=${ant_tmp#*Elapsed=}
	ant_elapsed=${ant_elapsed%%,GHS 5s=*}
	
	ant_ghs5s=${ant_tmp#*GHS 5s=}
	ant_ghs5s=${ant_ghs5s%%,GHS av=*}
	
	ant_ghsav=${ant_tmp#*GHS av=}
	ant_ghsav=${ant_ghsav%%,Found Blocks=*}
	
	ant_foundblocks=${ant_tmp#*Found Blocks=}
	ant_foundblocks=${ant_foundblocks%%,Getworks=*}
	
	ant_getworks=${ant_tmp#*Getworks=}
	ant_getworks=${ant_getworks%%,Accepted=*}
	
	ant_accepted=${ant_tmp#*Accepted=}
	ant_accepted=${ant_accepted%%,Rejected=*}
	
	ant_rejected=${ant_tmp#*Rejected=}
	ant_rejected=${ant_rejected%%,Hardware Errors=*}
	
	ant_hw=${ant_tmp#*Hardware Errors=}
	ant_hw=${ant_hw%%,Utility=*}
	
	ant_utility=${ant_tmp#*Utility=}
	ant_utility=${ant_utility%%,Discarded=*}
	
	ant_discarded=${ant_tmp#*Discarded=}
	ant_discarded=${ant_discarded%%,Stale=*}
	
	ant_stale=${ant_tmp#*Stale=}
	ant_stale=${ant_stale%%,Get Failures=*}
	
	ant_localwork=${ant_tmp#*Local Work=}
	ant_localwork=${ant_localwork%%,Remote Failures=*}
	
	ant_wu=${ant_tmp#*Work Utility=}
	ant_wu=${ant_wu%%,Difficulty Accepted=*}
	
	ant_diffa=${ant_tmp#*Difficulty Accepted=}
	ant_diffa=${ant_diffa%%,Difficulty Rejected=*}
	ant_diffa=${ant_diffa%%.*}
	
	ant_diffr=${ant_tmp#*Difficulty Rejected=}
	ant_diffr=${ant_diffr%%,Difficulty Stale=*}
	ant_diffr=${ant_diffr%%.*}
	
	ant_diffs=${ant_tmp#*Difficulty Stale=}
	ant_diffs=${ant_diffs%%,Best Share=*}
	ant_diffs=${ant_diffs%%.*}
	
	ant_bestshare=${ant_tmp#*Best Share=}
	ant_bestshare=${ant_bestshare%%,Device Hardware*}

	ant_temp_1=${ant_stats_tmp#*temp6=}
	ant_temp_1=${ant_temp_1%%,temp7=*}

	ant_temp_2=${ant_stats_tmp#*temp7=}
	ant_temp_2=${ant_temp_2%%,temp8=*}

	ant_temp_3=${ant_stats_tmp#*temp8=}
	ant_temp_3=${ant_temp_3%%,temp9=*}

	
fi

if [ "${ant_elapsed}" = "" ]; then 
	ant_elapsed=0
fi

ant_days=$((${ant_elapsed}/86400))
ant_hours=$((${ant_elapsed}/3600-${ant_days}*24))
ant_minutes=$((${ant_elapsed}/60-${ant_days}*1440-${ant_hours}*60))
ant_seconds=$((${ant_elapsed}-${ant_days}*86400-${ant_hours}*3600-${ant_minutes}*60))

ant_localwork_split=$(echo $ant_localwork| sed -r ':1;s/(.*[0-9])([0-9]{3})/\1,\2/;t1')

ant_elapsed=
if [ ${ant_days} -gt 0 ]; then
ant_elapsed=${ant_elapsed}${ant_days}d
fi
if [ ${ant_hours} -gt 0 ]; then
ant_elapsed=${ant_elapsed}${ant_hours}h
fi
if [ ${ant_minutes} -gt 0 ]; then
ant_elapsed=${ant_elapsed}${ant_minutes}m
fi
if [ ${ant_seconds} -gt 0 ]; then
ant_elapsed=${ant_elapsed}${ant_seconds}s
fi

avg_pcb = (${ant_temp_1} + ${ant_temp_1} + ${ant_temp_1}) / 3;

echo '{';
echo '"'ant_elapsed'"': '"'${ant_elapsed}'",';
echo '"'ant_ghs5s'"': '"'${ant_ghs5s}'",';
echo '"'ant_ghsav'"': '"'${ant_ghsav}'",';
echo '"'ant_foundblocks'"': '"'${ant_foundblocks}'",';
echo '"'ant_getworks'"': '"'${ant_getworks}'",';
echo '"'ant_accepted'"': '"'${ant_accepted}'",';
echo '"'ant_rejected'"': '"'${ant_rejected}'",';
echo '"'ant_hw'"': '"'${ant_hw}'",';
echo '"'ant_utility'"': '"'${ant_utility}'",';
echo '"'ant_discarded'"': '"'${ant_discarded}'",';
echo '"'ant_stale'"': '"'${ant_stale}'",';
echo '"'ant_localwork'"': '"'${ant_localwork}'",';
echo '"'ant_localwork_split'"': '"'${ant_localwork_split}'",';
echo '"'ant_wu'"': '"'${ant_wu}'",';
echo '"'ant_diffa'"': '"'${ant_diffa}'",';
echo '"'ant_diffr'"': '"'${ant_diffr}'",';
echo '"'ant_diffs'"': '"'${ant_diffs}'",';
echo '"'ant_bestshare'"': '"'${ant_bestshare}'",';
echo '"'ant_temp_1'"': '"'${ant_temp_1}'",';
echo '"'ant_temp_2'"': '"'${ant_temp_2}'",';
echo '"'ant_temp_3'"': '"'${ant_temp_3}'"';
echo '"'avg_pcb'"': '"'${avg_pcb}'"';
echo '}';
