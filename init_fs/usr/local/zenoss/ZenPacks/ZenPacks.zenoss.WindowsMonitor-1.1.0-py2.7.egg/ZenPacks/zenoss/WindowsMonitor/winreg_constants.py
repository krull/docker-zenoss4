##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__="A place to put all the ugly constants"

PERF_DETAIL_NOVICE        = 100 # The uninformed can understand it
PERF_DETAIL_ADVANCED      = 200 # For the advanced user
PERF_DETAIL_EXPERT        = 300 # For the expert user
PERF_DETAIL_WIZARD        = 400 # For the system designer

PERF_NO_INSTANCES = -1

PERF_SIZE_DWORD                 = 0
PERF_SIZE_LARGE                 = 0x100
PERF_SIZE_ZERO                  = 0x200
PERF_SIZE_VARIABLE_LEN          = 0x300
PERF_SIZE_MASK                  = 0x300

PERF_TYPE_NUMBER                = 0
PERF_TYPE_COUNTER               = 0x400
PERF_TYPE_TEXT                  = 0x800
PERF_TYPE_ZERO                  = 0xC00
PERF_TYPE_MASK                  = 0xC00

PERF_NUMBER_HEX                 = 0
PERF_NUMBER_DECIMAL             = 0x10000
PERF_NUMBER_DEC_1000            = 0x20000
PERF_COUNTER_VALUE              = 0
PERF_COUNTER_RATE               = 0x10000
PERF_COUNTER_FRACTION           = 0x20000
PERF_COUNTER_BASE               = 0x30000
PERF_COUNTER_ELAPSED            = 0x40000
PERF_COUNTER_QUEUELEN           = 0x50000
PERF_COUNTER_HISTOGRAM          = 0x60000
PERF_COUNTER_PRECISION          = 0x70000

PERF_TEXT_UNICODE               = 0
PERF_TEXT_ASCII                 = 0x10000
PERF_SUBTYPE_MASK               = 0x70000

PERF_TIMER_TICK                 = 0
PERF_TIMER_100NS                = 0x100000
PERF_OBJECT_TIMER               = 0x200000
PERF_TIMER_MASK                 = 0x300000

PERF_DELTA_COUNTER              = 0x400000
PERF_DELTA_BASE                 = 0x800000
PERF_INVERSE_COUNTER            = 0x1000000
PERF_MULTI_COUNTER              = 0x2000000
PERF_DISPLAY_NO_SUFFIX          = 0
PERF_DISPLAY_PER_SEC            = 0x10000000
PERF_DISPLAY_PERCENT            = 0x20000000
PERF_DISPLAY_SECONDS            = 0x30000000
PERF_DISPLAY_NOSHOW             = 0x40000000
PERF_DISPLAY_MASK               = 0x70000000
PERF_COUNTER_HISTOGRAM_TYPE     = 0x80000000

# 32-bit Counter.  Divide delta by delta time.  Display suffix: "/sec"
PERF_COUNTER_COUNTER = (PERF_SIZE_DWORD|PERF_TYPE_COUNTER|PERF_COUNTER_RATE|PERF_TIMER_TICK|PERF_DELTA_COUNTER|PERF_DISPLAY_PER_SEC)

# 64-bit Timer.  Divide delta by delta time.  Display suffix: "%"
PERF_COUNTER_TIMER = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_COUNTER_RATE|PERF_TIMER_TICK|PERF_DELTA_COUNTER|PERF_DISPLAY_PERCENT)

# Queue Length Space-Time Product. Divide delta by delta time. No Display 
# Suffix.
PERF_COUNTER_QUEUELEN_TYPE = (PERF_SIZE_DWORD|PERF_TYPE_COUNTER|PERF_COUNTER_QUEUELEN|PERF_TIMER_TICK|PERF_DELTA_COUNTER|PERF_DISPLAY_NO_SUFFIX)

# Queue Length Space-Time Product. Divide delta by delta time. No Display 
# Suffix.
PERF_COUNTER_LARGE_QUEUELEN_TYPE = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_COUNTER_QUEUELEN|PERF_TIMER_TICK|PERF_DELTA_COUNTER|PERF_DISPLAY_NO_SUFFIX)

# Queue Length Space-Time Product using 100 Ns timebase.
# Divide delta by delta time. No Display Suffix.
PERF_COUNTER_100NS_QUEUELEN_TYPE = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_COUNTER_QUEUELEN|PERF_TIMER_100NS|PERF_DELTA_COUNTER|PERF_DISPLAY_NO_SUFFIX)

# Queue Length Space-Time Product using Object specific timebase.
# Divide delta by delta time. No Display Suffix.
PERF_COUNTER_OBJ_TIME_QUEUELEN_TYPE = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_COUNTER_QUEUELEN|PERF_OBJECT_TIMER|PERF_DELTA_COUNTER|PERF_DISPLAY_NO_SUFFIX)

# 64-bit Counter.  Divide delta by delta time. Display Suffix: "/sec"
PERF_COUNTER_BULK_COUNT = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_COUNTER_RATE|PERF_TIMER_TICK|PERF_DELTA_COUNTER|PERF_DISPLAY_PER_SEC)

# Indicates the counter is not a  counter but rather Unicode text Display 
# as text.
PERF_COUNTER_TEXT = (PERF_SIZE_VARIABLE_LEN|PERF_TYPE_TEXT|PERF_TEXT_UNICODE|PERF_DISPLAY_NO_SUFFIX)

# Indicates the data is a counter  which should not be time averaged on 
# display (such as an error counter on a serial line). Display as is.  No 
# Display Suffix.
PERF_COUNTER_RAWCOUNT = (PERF_SIZE_DWORD|PERF_TYPE_NUMBER|PERF_NUMBER_DECIMAL|PERF_DISPLAY_NO_SUFFIX)

# Same as PERF_COUNTER_RAWCOUNT except its size is a large integer
PERF_COUNTER_LARGE_RAWCOUNT = (PERF_SIZE_LARGE|PERF_TYPE_NUMBER|PERF_NUMBER_DECIMAL|PERF_DISPLAY_NO_SUFFIX)

# Special case for RAWCOUNT that want to be displayed in hex. Indicates the
# data is a counter which should not be time averaged on display (such as 
# an error counter on a serial line). Display as is.  No Display Suffix.
PERF_COUNTER_RAWCOUNT_HEX = (PERF_SIZE_DWORD|PERF_TYPE_NUMBER|PERF_NUMBER_HEX|PERF_DISPLAY_NO_SUFFIX)
    
# Same as PERF_COUNTER_RAWCOUNT_HEX except its size is a large integer
PERF_COUNTER_LARGE_RAWCOUNT_HEX = (PERF_SIZE_LARGE|PERF_TYPE_NUMBER|PERF_NUMBER_HEX|PERF_DISPLAY_NO_SUFFIX)

# A count which is either 1 or 0 on each sampling interrupt (% busy) Divide
# delta by delta base. Display Suffix: "%"
PERF_SAMPLE_FRACTION = (PERF_SIZE_DWORD|PERF_TYPE_COUNTER|PERF_COUNTER_FRACTION|PERF_DELTA_COUNTER|PERF_DELTA_BASE|PERF_DISPLAY_PERCENT)

# A count which is sampled on each sampling interrupt (queue length) Divide
# delta by delta time. No Display Suffix.
PERF_SAMPLE_COUNTER = (PERF_SIZE_DWORD|PERF_TYPE_COUNTER|PERF_COUNTER_RATE|PERF_TIMER_TICK|PERF_DELTA_COUNTER|PERF_DISPLAY_NO_SUFFIX)

# A label: no data is associated with this counter (it has 0 length). Do 
# not display.
PERF_COUNTER_NODATA = (PERF_SIZE_ZERO|PERF_DISPLAY_NOSHOW)

# 64-bit Timer inverse (e.g., idle is measured, but display busy %) Display
# 100 - delta divided by delta time.  Display suffix: "%"
PERF_COUNTER_TIMER_INV = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_COUNTER_RATE|PERF_TIMER_TICK|PERF_DELTA_COUNTER|PERF_INVERSE_COUNTER|PERF_DISPLAY_PERCENT)
    
# The divisor for a sample, used with the previous counter to form a
# sampled %.  You must check for >0 before dividing by this!  This
# counter will directly follow the  numerator counter.  It should not
# be displayed to the user.
PERF_SAMPLE_BASE = (PERF_SIZE_DWORD|PERF_TYPE_COUNTER|PERF_COUNTER_BASE|PERF_DISPLAY_NOSHOW|1) 

# A timer which, when divided by an average base, produces a time
# in seconds which is the average time of some operation.  This
# timer times total operations, and  the base is the number of opera-
# tions.  Display Suffix: "sec"
PERF_AVERAGE_TIMER = (PERF_SIZE_DWORD|PERF_TYPE_COUNTER|PERF_COUNTER_FRACTION|PERF_DISPLAY_SECONDS)

# Used as the denominator in the computation of time or count
# averages.  Must directly follow the numerator counter.  Not dis-
# played to the user.
PERF_AVERAGE_BASE = (PERF_SIZE_DWORD|PERF_TYPE_COUNTER|PERF_COUNTER_BASE|PERF_DISPLAY_NOSHOW|2) 

# A bulk count which, when divided (typically) by the number of
# operations, gives (typically) the number of bytes per operation.
# No Display Suffix.
PERF_AVERAGE_BULK = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_COUNTER_FRACTION|PERF_DISPLAY_NOSHOW)

# 64-bit Timer in object specific units. Display delta divided by
# delta time as returned in the object type header structure.  Display 
# suffix: "%"
PERF_OBJ_TIME_TIMER = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_COUNTER_RATE|PERF_OBJECT_TIMER|PERF_DELTA_COUNTER|PERF_DISPLAY_PERCENT)

# 64-bit Timer in 100 nsec units. Display delta divided by
# delta time.  Display suffix: "%"
PERF_100NSEC_TIMER = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_COUNTER_RATE|PERF_TIMER_100NS|PERF_DELTA_COUNTER|PERF_DISPLAY_PERCENT)

# 64-bit Timer inverse (e.g., idle is measured, but display busy %)
# Display 100 - delta divided by delta time.  Display suffix: "%"
PERF_100NSEC_TIMER_INV = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_COUNTER_RATE|PERF_TIMER_100NS|PERF_DELTA_COUNTER|PERF_INVERSE_COUNTER|PERF_DISPLAY_PERCENT)

# 64-bit Timer.  Divide delta by delta time.  Display suffix: "%"
# Timer for multiple instances, so result can exceed 100%.
PERF_COUNTER_MULTI_TIMER = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_COUNTER_RATE|PERF_DELTA_COUNTER|PERF_TIMER_TICK|PERF_MULTI_COUNTER|PERF_DISPLAY_PERCENT)

# 64-bit Timer inverse (e.g., idle is measured, but display busy %)
# Display 100 * _MULTI_BASE - delta divided by delta time.
# Display suffix: "%" Timer for multiple instances, so result
# can exceed 100%.  Followed by a counter of type _MULTI_BASE.
PERF_COUNTER_MULTI_TIMER_INV = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_COUNTER_RATE|PERF_DELTA_COUNTER|PERF_MULTI_COUNTER|PERF_TIMER_TICK|PERF_INVERSE_COUNTER|PERF_DISPLAY_PERCENT)

# Number of instances to which the preceding _MULTI_..._INV counter
# applies.  Used as a factor to get the percentage.
PERF_COUNTER_MULTI_BASE = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_COUNTER_BASE|PERF_MULTI_COUNTER|PERF_DISPLAY_NOSHOW)

# 64-bit Timer in 100 nsec units. Display delta divided by delta time.
# Display suffix: "%" Timer for multiple instances, so result can exceed 
# 100%.
PERF_100NSEC_MULTI_TIMER = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_DELTA_COUNTER|PERF_COUNTER_RATE|PERF_TIMER_100NS|PERF_MULTI_COUNTER|PERF_DISPLAY_PERCENT)

# 64-bit Timer inverse (e.g., idle is measured, but display busy %)
# Display 100 * _MULTI_BASE - delta divided by delta time.
# Display suffix: "%" Timer for multiple instances, so result
# can exceed 100%.  Followed by a counter of type _MULTI_BASE.
PERF_100NSEC_MULTI_TIMER_INV = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_DELTA_COUNTER|PERF_COUNTER_RATE|PERF_TIMER_100NS|PERF_MULTI_COUNTER|PERF_INVERSE_COUNTER|PERF_DISPLAY_PERCENT)

# Indicates the data is a fraction of the following counter  which
# should not be time averaged on display (such as free space over
# total space.) Display as is.  Display the quotient as "%".
PERF_RAW_FRACTION = (PERF_SIZE_DWORD|PERF_TYPE_COUNTER|PERF_COUNTER_FRACTION|PERF_DISPLAY_PERCENT)

PERF_LARGE_RAW_FRACTION = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_COUNTER_FRACTION|PERF_DISPLAY_PERCENT)

# Indicates the data is a base for the preceding counter which should
# not be time averaged on display (such as free space over total space.)
PERF_RAW_BASE = (PERF_SIZE_DWORD|PERF_TYPE_COUNTER|PERF_COUNTER_BASE|PERF_DISPLAY_NOSHOW|3)

PERF_LARGE_RAW_BASE = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_COUNTER_BASE|PERF_DISPLAY_NOSHOW )

# The data collected in this counter is actually the start time of the
# item being measured. For display, this data is subtracted from the
# sample time to yield the elapsed time as the difference between the two.
# In the definition below, the PerfTime field of the Object contains
# the sample time as indicated by the PERF_OBJECT_TIMER bit and the
# difference is scaled by the PerfFreq of the Object to convert the time
# units into seconds.
PERF_ELAPSED_TIME = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_COUNTER_ELAPSED|PERF_OBJECT_TIMER|PERF_DISPLAY_SECONDS)

# This counter is used to display the difference from one sample
# to the next. The counter value is a constantly increasing number
# and the value displayed is the difference between the current
# value and the previous value. Negative numbers are not allowed
# which shouldn't be a problem as long as the counter value is
# increasing or unchanged.
PERF_COUNTER_DELTA = (PERF_SIZE_DWORD|PERF_TYPE_COUNTER|PERF_COUNTER_VALUE|PERF_DELTA_COUNTER|PERF_DISPLAY_NO_SUFFIX)

# Same as PERF_COUNTER_DELTA except its size is a large integer
PERF_COUNTER_LARGE_DELTA = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_COUNTER_VALUE|PERF_DELTA_COUNTER|PERF_DISPLAY_NO_SUFFIX)

# The precision counters are timers that consist of two counter values:
# 1) the count of elapsed time of the event being monitored
# 2) the "clock" time in the same units
# 
# the precition timers are used where the standard system timers are not
# precise enough for accurate readings. It's assumed that the service
# providing the data is also providing a timestamp at the same time which
# will eliminate any error that may occur since some small and variable
# time elapses between the time the system timestamp is captured and when
# the data is collected from the performance DLL. Only in extreme cases
# has this been observed to be problematic.
#
# when using this type of timer, the definition of the
# PERF_PRECISION_TIMESTAMP counter must immediately follow the
# definition of the PERF_PRECISION_*_TIMER in the Object header
#
# The timer used has the same frequency as the System Performance Timer
PERF_PRECISION_SYSTEM_TIMER = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_COUNTER_PRECISION|PERF_TIMER_TICK|PERF_DELTA_COUNTER|PERF_DISPLAY_PERCENT)

# The timer used has the same frequency as the 100 NanoSecond Timer
PERF_PRECISION_100NS_TIMER = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_COUNTER_PRECISION|PERF_TIMER_100NS|PERF_DELTA_COUNTER|PERF_DISPLAY_PERCENT)

# The timer used is of the frequency specified in the Object header's
# PerfFreq field (PerfTime is ignored)
PERF_PRECISION_OBJECT_TIMER = (PERF_SIZE_LARGE|PERF_TYPE_COUNTER|PERF_COUNTER_PRECISION|PERF_OBJECT_TIMER|PERF_DELTA_COUNTER|PERF_DISPLAY_PERCENT)

# This is the timestamp to use in the computation of the timer specified 
# in the previous description block
PERF_PRECISION_TIMESTAMP = (PERF_LARGE_RAW_BASE)

PDH_FMT_LONG        = 0x00000100
PDH_FMT_DOUBLE      = 0x00000200
PDH_FMT_LARGE       = 0x00000400
PDH_FMT_NOSCALE     = 0x00001000
PDH_FMT_1000        = 0x00002000
PDH_FMT_NOCAP100    = 0x00008000
