##############################################################################
# 
# Copyright (C) Zenoss, Inc. 2008, all rights reserved.
# 
# This content is made available according to terms specified in
# License.zenoss under the directory where your Zenoss product is installed.
# 
##############################################################################


__doc__="""
Structures for calling winreg RPC methods, and a class for decoding
the QueryValues result
"""
from datetime import datetime
import logging
import re
import struct
from collections import defaultdict

from winreg_constants import *

EXTRA_DEBUG = 9

logging.addLevelName(EXTRA_DEBUG, "ExtraDebug")
log = logging.getLogger("zen.winperf.winreg")

counterParser = re.compile(
        r'\\(?P<object>[^(\\]+)(\(((?P<parent>[^/]+)/)?(?P<instance>[^#\)]+)(#(?P<index>\d+))?\))?\\(?P<counter>[^\\]+)$'
    )
range = xrange

_path_cache = {}
def parseCounter(path, counterParser_match=counterParser.match):
    """
    Use the counterParser regular expression to break out
    (object, parent, instance, idx, counter) from a counter path string

    Information on potential counter formats can be found here:
    http://msdn.microsoft.com/en-us/library/windows/desktop/aa373193(v=vs.85).aspx
    """
    if path not in _path_cache:
        parts = counterParser_match(path).groupdict()
        parts = dict((k, v.lower() if v else None) for k,v in parts.iteritems())
        #if the counter doesn't specify an index, the first instance is used by default
        parts['index'] = int(parts['index'] or 0)
        _path_cache[path] = parts
    return _path_cache[path]

def extractUnicodeString(data, start, end, encoding):
    """
    Extracts a UTF-16 Unicode string from the data block in the specified
    range. If the string is NUL terminated then extacting the string will
    stop at the NUL position and the NUL will not be included in the
    resultant Python string.

    @param start: the starting position of the string in the data block
    @type start: int
    @param end: the ending position of the string in the data block
    @type end: int
    @return: a unicode string extracted from the raw data
    @rtype: string
    """
    # According to the documentation, length should NOT include any 
    # padding bytes added to the end of the name field, but it appears 
    # that some performance providers do this incorrectly and add the
    # padding data. Only extracting up to the NUL terminator allows us
    # to bypass this bug.
    for pos in range(start, end, 2):
        if data[pos:pos + 2] == '\x00\x00': break
    else:
        # fell through without finding a trailing NUL
        return unicode(data[start:end], encoding)

    # this is a NUL terminated unicode string, so skip that trailing NUL
    return unicode(data[start:pos], encoding)

def isNumerator(counterType, counterTypes=set((PERF_SAMPLE_FRACTION,
                           PERF_RAW_FRACTION,
                           PERF_LARGE_RAW_FRACTION,
                           PERF_PRECISION_SYSTEM_TIMER,
                           PERF_PRECISION_100NS_TIMER,
                           PERF_PRECISION_OBJECT_TIMER,
                           PERF_AVERAGE_TIMER,
                           PERF_AVERAGE_BULK))):
    return counterType in counterTypes

#
# The PerformanceData class parses the provides access to the Windows 
# Performance Data Format as documented at the following web address:
#   http://msdn.microsoft.com/en-us/library/aa373105(VS.85).aspx
#
# This data structure is inherently variable and therefore requires
# a parsing approach to pull data off based upon previous data read.
# The data starts with a fixed-length structure known as a PERF_DATA_BLOCK
# and then followed by multiple PERF_COUNTER_DEFINITION structures, one
# for each performance counter retrieved. If the object queried supports
# multiple instances then these counter definitions are followed by a set
# of PERF_INSTANCE_DEFINITION structures, and within each instance a set 
# of PERF_COUNTER_BLOCK structures, otherwise just a set of 
# PERF_COUNTER_BLOCK structures will be found.
#
# +===========================+
# | PERF_DATA_BLOCK           |
# +---------------------------+
# | PERF_OBJECT_TYPE          |
# +---------------------------+
# |  PERF_COUNTER_DEFINITION  |
# +---------------------------+
# |  PERF_COUNTER_DEFINITION  |
# +---------------------------+
# |           ...             | } counter definitions for all counters
# +---------------------------+
# |  PERF_COUNTER_DEFINITION  |
# +---------------------------+
# |  PERF_INSTANCE_DEFINITION |
# +---------------------------+
# |   Name of instance        | } variable-length unicode string
# +---------------------------+
# |   PERF_COUNTER_BLOCK      |
# +---------------------------+
# |           ...             | } counter data for all counters of instance
# +---------------------------+
# |   PERF_COUNTER_BLOCK      |
# +---------------------------+
# |           ...             | } above block repeated for each instance
# +---------------------------+
# |  PERF_INSTANCE_DEFINITION |
# +---------------------------+
# |   Name of instance        | } variable-length unicode string
# +---------------------------+
# |   PERF_COUNTER_BLOCK      |
# +---------------------------+
# |           ...             | } counter data for all counters of instance
# +---------------------------+
# |   PERF_COUNTER_BLOCK      |
# +===========================+
#
# Alignment of the internal strutures of the performance data blocks is the
# responsibility of the data provider. The Windows OS will report an error
# if data is not properly aligned. As a client, we need to be aware of
# the alignment so we know what data to extract from where. By adhering to 
# strict offset and length values provided in each structure this happens
# automatically.
#
# See http://support.microsoft.com/kb/262335 for more details.
# 
class PerformanceData:
    class PerformanceObject:
        pass

    class PerfCounterDefinition:
        pass

    class PerfInstanceDefinition:
        pass
    
    class PerfCounterData:
        pass

    def __init__(self, data, dict):
        self.logLevel = log.getEffectiveLevel()
        self.data = data
        self.dict = dict

        cursor = self._parsePerfDataBlock()

        if cursor != len(data):
            log.debug("Parsed data length differs from data length (%d != %d)",
                cursor, len(data))

        del self.data
        del self.dict

    def _unpack(self, fmt, start, end, struct_unpack=struct.unpack):
        fmt = self._endianPrefix + fmt
        return struct_unpack(fmt, self.data[start:end])

    _fmt_cache={}
    def _calcsize(self, fmt, struct_calcsize=struct.calcsize):
        if fmt not in self._fmt_cache:
            self._fmt_cache[fmt] = struct_calcsize(self._endianPrefix + fmt)
        return self._fmt_cache[fmt]        

    def _parsePerfDataBlock(self, cursor = 0):
        #
        # Parses a PERF_DATA_BLOCK and the data that follows it. A 
        # PERF_DATA_BLOCK structure is defined at the following web address:
        #
        # http://msdn.microsoft.com/en-us/library/aa373157(VS.85).aspx
        #
        #  The C/C++ structure format is as follows:
        #  typedef struct _PERF_DATA_BLOCK {
        #      WCHAR Signature[4];
        #      DWORD LittleEndian;
        #      DWORD Version;
        #      DWORD Revision;
        #      DWORD TotalByteLength;
        #      DWORD HeaderLength;
        #      DWORD NumObjectTypes;
        #      DWORD DefaultObject;
        #      SYSTEMTIME SystemTime;
        #      LARGE_INTEGER PerfTime;
        #      LARGE_INTEGER PerfFreq;
        #      LARGE_INTEGER PerfTime100nSec;
        #      DWORD SystemNameLength;
        #      DWORD SystemNameOffset;
        #  } PERF_DATA_BLOCK;
        #
        # The SYSTEMTIME structure is defined at the following web address:
        #   http://msdn.microsoft.com/en-us/library/ms724950(VS.85).aspx
        #    
        #  The C/C++ structure format is as follows:
        #  typedef struct _SYSTEMTIME {
        #      WORD wYear;
        #      WORD wMonth;
        #      WORD wDayOfWeek;
        #      WORD wDay;
        #      WORD wHour;
        #      WORD wMinute;
        #      WORD wSecond;
        #      WORD wMilliseconds;
        #  } SYSTEMTIME;

        signature = self.data[cursor:cursor+8]
        if signature != "P\0E\0R\0F\0":
            raise RuntimeError, "Bad signature"

        self._endian, = struct.unpack("I", self.data[cursor+8:cursor+12])
        if not (self._endian in (0, 1)):
            raise RuntimeError("LittleEndian out of bound(%d)" % self._endian)
        self._endianPrefix = "><"[self._endian]
        self._encoding = { 0:"utf-16-be", 1:"utf-16-le" }[self._endian]

        #
        # there are 4 padding bytes that must be skipped after the SystemTime
        # member of the PERF_DATA_BLOCK structure
        #
        fmt = "6l8H4x3Q2l"
        size = self._calcsize(fmt)
        start = cursor + 12
        end = start + size
        (version, revision, totalByteLength, headerLength, numObjectTypes,
         self.defaultObject, stYear, stMonth, stDayOfWeek, stDay, stHour,
         stMin, stSec, stMs, self.perfTime, self.perfFreq, 
         self.perfTime100nSec, systemNameLength, systemNameOffset) = \
            self._unpack(fmt, start, end)

        self._systemTime = datetime(stYear,stMonth,stDay,stHour,stMin,
                                             stSec, stMs*1000)

        start = systemNameOffset
        end = systemNameOffset + systemNameLength
        self._systemName = extractUnicodeString(self.data, start, end, self._encoding)

        if self.logLevel <= EXTRA_DEBUG:
          log.log(EXTRA_DEBUG, "PERF_DATA_BLOCK:")
          log.log(EXTRA_DEBUG, "  Signature        = %s", signature)
          log.log(EXTRA_DEBUG, "  LittleEndian     = %d", self._endian)
          log.log(EXTRA_DEBUG, "  Version          = %d", version)
          log.log(EXTRA_DEBUG, "  Revision         = %d", revision)
          log.log(EXTRA_DEBUG, "  TotalByteLength  = %d", totalByteLength)
          log.log(EXTRA_DEBUG, "  HeaderLength     = %d", headerLength)
          log.log(EXTRA_DEBUG, "  NumObjectTypes   = %d", numObjectTypes)
          log.log(EXTRA_DEBUG, "  DefaultObject    = %d", self.defaultObject)
          log.log(EXTRA_DEBUG, "  SystemTime       = %r", self._systemTime)
          log.log(EXTRA_DEBUG, "  PerfTime         = %r", self.perfTime)
          log.log(EXTRA_DEBUG, "  PerfFreq         = %r", self.perfFreq)
          log.log(EXTRA_DEBUG, "  PerfTime100nSec  = %r", self.perfTime100nSec)
          log.log(EXTRA_DEBUG, "  SystemNameLength = %d", systemNameLength)
          log.log(EXTRA_DEBUG, "  SystemNameOffset = %d", systemNameOffset)
          log.log(EXTRA_DEBUG, "  SystemName       = %s", self._systemName)

        cursor = cursor + headerLength
        if self.logLevel <= EXTRA_DEBUG:
            log.log(EXTRA_DEBUG, "Cursor after PERF_DATA_BLOCK header = %d", cursor)

        self.objects = {}
        for i in range(numObjectTypes):
            self.curObject = self.PerformanceObject()
            cursor = self._parsePerfObjectType(cursor)
            if self.logLevel <= EXTRA_DEBUG:
                log.log(EXTRA_DEBUG, "Cursor after PERF_OBJECT_TYPE = %d", cursor)
            self.objects[self.curObject.name.lower()] = self.curObject
        if numObjectTypes > 0:
            del self.curObject

        return cursor

    def _parsePerfObjectType(self, cursor):
        #
        # Parses a PERF_OBJECT_TYPE data structure which is defined at the
        # following web address:
        #   http://msdn.microsoft.com/en-us/library/aa373160(VS.85).aspx
        #
        #  The C/C++ structure format is as follows:
        #  typedef struct _PERF_OBJECT_TYPE {
        #      DWORD TotalByteLength;
        #      DWORD DefinitionLength;
        #      DWORD HeaderLength;
        #      DWORD ObjectNameTitleIndex;
        #      LPWSTR ObjectNameTitle;
        #      DWORD ObjectHelpTitleIndex;
        #      LPWSTR ObjectHelpTitle;
        #      DWORD DetailLevel;
        #      DWORD NumCounters;
        #      DWORD DefaultCounter;
        #      DWORD NumInstances;
        #      DWORD CodePage;
        #      LARGE_INTEGER PerfTime;
        #      LARGE_INTEGER PerfFreq;
        #  } PERF_OBJECT_TYPE;
        #

        o = self.curObject
        fmt = "12l2Q"
        size = self._calcsize(fmt)
        (totalByteLength, definitionLength, headerLength, objectNameTitleIndex,
         objectNameTitle, objectHelpTitleIndex, objectHelpTitle, o.detailLevel,
         numCounters, o.defaultCounter, numInstances, o.codePage, o.perfTime,
         o.perfFreq) = self._unpack(fmt, cursor, cursor + size)

        o.name = self.dict[objectNameTitleIndex]

        if self.logLevel <= EXTRA_DEBUG:
            log.log(EXTRA_DEBUG, "PERF_OBJECT_TYPE:")
            log.log(EXTRA_DEBUG, "  TotalByteLength      = %d", totalByteLength)
            log.log(EXTRA_DEBUG, "  DefinitionLength     = %d", definitionLength)
            log.log(EXTRA_DEBUG, "  HeaderLength         = %d", headerLength)
            log.log(EXTRA_DEBUG, "  ObjectNameTitleIndex = %d", objectNameTitleIndex)
            log.log(EXTRA_DEBUG, "  ObjectNameTitle      = %d", objectNameTitle)
            log.log(EXTRA_DEBUG, "  ObjectHelpTitleIndex = %d", objectHelpTitleIndex)
            log.log(EXTRA_DEBUG, "  ObjectHelpTitle      = %d", objectHelpTitle)
            log.log(EXTRA_DEBUG, "  DetailLevel          = %d", o.detailLevel)
            log.log(EXTRA_DEBUG, "  NumCounters          = %d", numCounters)
            log.log(EXTRA_DEBUG, "  DefaultCounter       = %d", o.defaultCounter)
            log.log(EXTRA_DEBUG, "  NumInstances         = %d", numInstances)
            log.log(EXTRA_DEBUG, "  CodePage             = %d", o.codePage)
            log.log(EXTRA_DEBUG, "  PerfTime             = %d", o.perfTime)
            log.log(EXTRA_DEBUG, "  PerfFreq             = %d", o.perfFreq)
            log.log(EXTRA_DEBUG, "  Name                 = %s", o.name)

        c = cursor + headerLength
        if self.logLevel <= EXTRA_DEBUG:
            log.log(EXTRA_DEBUG, "Cursor after PERF_OBJECT_TYPE header = %d", c)

        #
        # pull the counter definitions out
        #
        o.counterDefinitions = {}
        for i in range(numCounters):
            counterDef, c = self._parsePerfCounterDefinition(c)
            if self.logLevel <= EXTRA_DEBUG:
                log.log(EXTRA_DEBUG, "Cursor after PERF_COUNTER_DEFINITION = %d", c)
            if counterDef:
                key = counterDef.name.lower()
                o.counterDefinitions[key] = counterDef

        #
        # pull all the counter blocks out, whether inside an instance or not
        #
        if numInstances == PERF_NO_INSTANCES:
            o.data = {}
            self.curData = o.data
            c = self._parsePerfCounterBlock(c)
            if self.logLevel <= EXTRA_DEBUG:
                log.log(EXTRA_DEBUG, "Cursor after PERF_COUNTER_BLOCK = %d", c)
        else:
            instances = defaultdict(list)
            for i in range(numInstances):
                self.curInstance = self.PerfInstanceDefinition()
                c = self._parsePerfInstanceDefinition(c)
                if self.logLevel <= EXTRA_DEBUG:
                    log.log(EXTRA_DEBUG, "Cursor after PERF_INSTANCE_DEFINITION = %d", c)
                instances[self.curInstance.name.lower()].append(self.curInstance)
            o.instances = dict(instances)

        # verify that our parsing resulted in the same cursor position as
        # the byte length, but this will be off if any padding bytes were
        # added by the provider
        if c != cursor + totalByteLength:
            if self.logLevel <= EXTRA_DEBUG:
                log.log(EXTRA_DEBUG, "Possible PERF_OBJECT_TYPE parse error (%d != %d)" %
                        (c, cursor + totalByteLength))

        return cursor + totalByteLength

    def _parsePerfCounterDefinition(self, cursor):
        #
        # Parses a PERF_COUNTER_DEFINITION structure which is defined at
        # the following web address:
        #  http://msdn.microsoft.com/en-us/library/aa373150(VS.85).aspx
        #
        #  The C/C++ structure format is as follows:
        #  typedef struct _PERF_COUNTER_DEFINITION {
        #      DWORD ByteLength;
        #      DWORD CounterNameTitleIndex;
        #      LPWSTR CounterNameTitle;
        #      DWORD CounterHelpTitleIndex;
        #      LPWSTR CounterHelpTitle;
        #      DWORD DefaultScale;
        #      DWORD DetailLevel;
        #      DWORD CounterType;
        #      DWORD CounterSize;
        #      DWORD CounterOffset;
        #  } PERF_COUNTER_DEFINITION;

        counterDef = self.PerfCounterDefinition()

        fmt = "10L"
        size = self._calcsize(fmt)
        (byteLength, counterNameTitleIndex, counterNameTitle, 
         counterHelpTitleIndex, counterHelpTitle, defaultScale, detailLevel,
         counterType, counterSize, counterOffset) = \
            self._unpack(fmt, cursor, cursor + size)

        counterDef.defaultScale = defaultScale
        counterDef.detailLevel = detailLevel
        counterDef.counterType = counterType
        counterDef.counterOffset = counterOffset
        counterDef.counterSize = counterSize

        if counterNameTitleIndex not in self.dict:
            counterDef = None
            counterName = None
            if self.logLevel <= logging.DEBUG:
                log.debug("Unable to find counter name for index %d",
                          counterNameTitleIndex)
        else:
            counterName = self.dict[counterNameTitleIndex]
            counterDef.name = counterName

            if isNumerator(counterType):
                baseCursor = cursor + byteLength

                fmt = "10L"
                size = self._calcsize(fmt)
                (basebyteLength, basecounterNameTitleIndex, 
                 basecounterNameTitle, basecounterHelpTitleIndex, 
                 basecounterHelpTitle, basedefaultScale, basedetailLevel, 
                 basecounterType, basecounterSize, basecounterOffset) = \
                    self._unpack(fmt, baseCursor, baseCursor + size)
    
                if (basecounterType & PERF_COUNTER_BASE) == PERF_COUNTER_BASE:
                    if self.logLevel <= logging.DEBUG:
                        log.log(EXTRA_DEBUG, 
                                "Found base counter definition for counter '%s'", 
                                counterName)
                    counterDef.baseOffset = basecounterOffset
                    counterDef.baseSize = basecounterSize

                else:
                    if self.logLevel <= logging.DEBUG:
                        log.log(EXTRA_DEBUG, 
                                "Did not find a base counter definition for counter '%s'", 
                                counterName)
                    counterDef = None

            elif (counterType & PERF_COUNTER_BASE) == PERF_COUNTER_BASE:
                # This is a real base counter, and we can just skip it...
                # NOTE: sometimes data comes across where the numerator has
                # PERF_COUNTER_BASE flag set, too, so we need to make sure
                # it is a numerator first, before we decide to skip it...
                counterDef = None

        if self.logLevel <= EXTRA_DEBUG:
            log.log(EXTRA_DEBUG, "PERF_COUNTER_DEFINITION:")
            log.log(EXTRA_DEBUG, "  ByteLength = %d", byteLength)
            log.log(EXTRA_DEBUG, "  CounterNameTitleIndex = %d", counterNameTitleIndex)
            log.log(EXTRA_DEBUG, "  CounterNameTitle      = %d", counterNameTitle)
            log.log(EXTRA_DEBUG, "  CounterHelpTitleIndex = %d", counterHelpTitleIndex)
            log.log(EXTRA_DEBUG, "  CounterHelpTitle      = %d", counterHelpTitle)
            log.log(EXTRA_DEBUG, "  DefaultScale          = %d", defaultScale)
            log.log(EXTRA_DEBUG, "  DetailLevel           = %d", detailLevel)
            log.log(EXTRA_DEBUG, "  CounterType           = 0x%08x", counterType)
            log.log(EXTRA_DEBUG, "  CounterSize           = %d", counterSize)
            log.log(EXTRA_DEBUG, "  CounterOffset         = %d", counterOffset)
            log.log(EXTRA_DEBUG, "  CounterName           = %s", counterName)

        return (counterDef, cursor + byteLength)

    def _parsePerfInstanceDefinition(self, cursor):
        #
        # Parses a PERF_INSTANCE_DEFINITION structure which is defined at the
        # follow web address:
        #     http://msdn.microsoft.com/en-us/library/aa373159(VS.85).aspx
        #
        # The C/C++ structure format is as follows:
        #     typedef struct _PERF_INSTANCE_DEFINITION {
        #         DWORD ByteLength;
        #         DWORD ParentObjectTitleIndex;
        #         DWORD ParentObjectInstance;
        #         DWORD UniqueID;
        #         DWORD NameOffset;
        #         DWORD NameLength;
        #     } PERF_INSTANCE_DEFINITION;
        #
        i = self.curInstance

        fmt = "6L"
        size = self._calcsize(fmt)
        start = cursor
        end = start + size

        (byteLength, parentObjectTitleIndex, parentObjectInstance,
         uniqueID, nameOffset, nameLength) = self._unpack(fmt, start, end)
         
        start = cursor + nameOffset
        end = start + nameLength
        i.name = extractUnicodeString(self.data, start, end, self._encoding)

        if self.logLevel <= EXTRA_DEBUG:
            log.log(EXTRA_DEBUG, "PERF_INSTANCE_DEFINITION:")
            log.log(EXTRA_DEBUG, "  ByteLength             = %d", byteLength)
            log.log(EXTRA_DEBUG, "  ParentObjectTitleIndex = %d", parentObjectTitleIndex)
            log.log(EXTRA_DEBUG, "  ParentObjectInstance   = %d", parentObjectInstance)
            log.log(EXTRA_DEBUG, "  UniqueID               = %d", uniqueID)
            log.log(EXTRA_DEBUG, "  NameOffset             = %d", nameOffset)
            log.log(EXTRA_DEBUG, "  NameLength             = %d", nameLength)
            log.log(EXTRA_DEBUG, "  Name                   = %s", i.name)

        i.data = {}
        self.curData = i.data
        return self._parsePerfCounterBlock(cursor + byteLength)

    def _parsePerfCounterBlock(self, cursor):
        #
        # Parses a list of PERF_COUNTER_BLOCK structures that are defined at 
        # the following web address:
        #     http://msdn.microsoft.com/en-us/library/aa373147(VS.85).aspx
        #
        #  The C/C++ structure format is as follows:
        #
        #     typedef struct _PERF_COUNTER_BLOCK {
        #         DWORD ByteLength;
        #     } PERF_COUNTER_BLOCK;
        #
        d = self.curData
        byteLength, = self._unpack("i", cursor, cursor + 4)

        #
        # go through all of this object's counter definitions and pick 
        # out the data from the counter block
        #
        for counterDef in self.curObject.counterDefinitions.itervalues():

            data = self.PerfCounterData()

            # Pull data will fill in data.data and data.baseData, if
            # a base counter is associated with this counter, and
            # automatically handle a long or quadword size difference
            self._pullData(data, counterDef, cursor)

            if counterDef.counterType in (PERF_COUNTER_COUNTER, 
                                          PERF_COUNTER_QUEUELEN_TYPE, 
                                          PERF_SAMPLE_COUNTER):
                data.time = self.perfTime
                if counterDef.counterType in (PERF_COUNTER_COUNTER, 
                                              PERF_SAMPLE_COUNTER):
                    data.frequency = self.perfFreq

            elif counterDef.counterType == PERF_OBJ_TIME_TIMER:
                data.time = self.curObject.perfTime

            elif counterDef.counterType == PERF_COUNTER_100NS_QUEUELEN_TYPE:
                data.time = self.perfTime100nSec

            elif counterDef.counterType == PERF_COUNTER_OBJ_TIME_QUEUELEN_TYPE:
                data.time = self.curObject.perfTime

            elif counterDef.counterType in (PERF_COUNTER_TIMER, 
                                            PERF_COUNTER_TIMER_INV, 
                                            PERF_COUNTER_BULK_COUNT, 
                                            PERF_COUNTER_LARGE_QUEUELEN_TYPE): 
                data.time = self.perfTime
                if counterDef.counterType == PERF_COUNTER_BULK_COUNT:
                    data.frequency = self.perfFreq

            elif counterDef.counterType in (PERF_COUNTER_MULTI_TIMER, 
                                            PERF_COUNTER_MULTI_TIMER_INV):
                data.frequency = self.perfFreq
                data.time = self.perfTime

                if (counterDef.counterType & PERF_MULTI_COUNTER) == PERF_MULTI_COUNTER:
                    # TODO: what about the MultiCounterData that comes from the next counter block? hmmm
                    pass

            #
            # These counters do not use any time reference
            #
            elif counterDef.counterType in (PERF_COUNTER_RAWCOUNT, 
                                            PERF_COUNTER_RAWCOUNT_HEX, 
                                            PERF_COUNTER_LARGE_RAWCOUNT, 
                                            PERF_COUNTER_LARGE_RAWCOUNT_HEX, 
                                            PERF_COUNTER_DELTA, 
                                            PERF_COUNTER_LARGE_DELTA):
                pass

            #
            # These counters use the 100ns time base in their calculation
            #
            elif counterDef.counterType in (PERF_100NSEC_TIMER, 
                                            PERF_100NSEC_TIMER_INV, 
                                            PERF_100NSEC_MULTI_TIMER, 
                                            PERF_100NSEC_MULTI_TIMER_INV):
                data.time = self.perfTime100nSec

                if (counterDef.counterType & PERF_MULTI_COUNTER) == PERF_MULTI_COUNTER:
                    # TODO: what about the MultiCounterData that comes from the next counter block? hmmm
                    pass

            #
            # These counters use two data points, this value and one from the
            # counter's base counter. The base counter should be the next
            # counter in the object's list of counters.
            #
            elif counterDef.counterType in (PERF_SAMPLE_FRACTION,
                                            PERF_RAW_FRACTION,
                                            PERF_LARGE_RAW_FRACTION):
                data.time = data.baseData

            elif counterDef.counterType in (PERF_PRECISION_SYSTEM_TIMER,
                                            PERF_PRECISION_100NS_TIMER,
                                            PERF_PRECISION_OBJECT_TIMER):
                data.time = data.baseData
            
            elif counterDef.counterType == PERF_AVERAGE_TIMER:
                data.time = data.baseData
                data.frequency = self.perfFreq

            elif counterDef.counterType == PERF_AVERAGE_BULK:
                data.time = data.baseData

            # These are base counters and are used in calculations for other counters.
            elif counterDef.counterType in (PERF_SAMPLE_BASE,
                                            PERF_AVERAGE_BASE,
                                            PERF_COUNTER_MULTI_BASE,
                                            PERF_RAW_BASE,
                                            PERF_LARGE_RAW_BASE):
                data.data = 0
                data.time = 0
                continue

            elif counterDef.counterType == PERF_ELAPSED_TIME:
                data.time = self.curObject.perfTime
                data.frequency = self.curObject.perfFreq

            # These counters are currently not supported.
            elif counterDef.counterType in (PERF_COUNTER_TEXT,
                                            PERF_COUNTER_NODATA,
                                            PERF_COUNTER_HISTOGRAM_TYPE):
                data.data = 0
                data.time = 0
                continue

            # Encountered an unidentified counter.
            else:
                data.data = 0
                data.time = 0
                continue

            d[counterDef.name.lower()] = data

        if self.logLevel <= EXTRA_DEBUG:
            log.log(EXTRA_DEBUG, "PERF_COUNTER_BLOCK:")
            log.log(EXTRA_DEBUG, "  ByteLength = %d", byteLength)

        return cursor + byteLength

    def _pullData(self, data, counterDef, cursor, fmtdict1={4:"L4xL", 8:"QL"}, fmtdict2={4:"L", 8:"Q"}):
        """
        Pull the performance counter raw data out of the data block based upon
        the provided counter definition. If the counter is a multi-counter, then
        the counter block will include 2 values in a row.
        """
        
        start = cursor + counterDef.counterOffset
        counterDef_counterSize = counterDef.counterSize

        if counterDef.counterType & PERF_MULTI_COUNTER == PERF_MULTI_COUNTER:
            fmt = fmtdict1[counterDef_counterSize]
            end = start + self._calcsize(fmt)
            (data.data, data.multiCounterData) = self._unpack(fmt, start, end)
                
            # TODO: do we need to handle a base value with a multi-counter?

        else:
            fmt = fmtdict2[counterDef_counterSize]
            end = start + counterDef_counterSize
            data.data, = self._unpack(fmt, start, end)

            #
            # If this counter definition has a base offset, then we need to 
            # pull the base data as well!
            #
            if hasattr(counterDef, 'baseOffset'):
                start = cursor + counterDef.baseOffset
                end = start + counterDef.baseSize
                fmt = fmtdict2[counterDef.baseSize]
                data.baseData, = self._unpack(fmt, start, end)

    def getCounter(self, counterParts):
        """
        Retrieves the PerfCounterDefinition and PerfCounterValue object for the
        specified counter.
        """
        counterObj = self.objects[counterParts['object']]
        counterDef = counterObj.counterDefinitions[counterParts['counter']]
        if counterParts['instance'] is None:
            dataObj = counterObj
        else:
            instanceData = counterObj.instances[counterParts['instance']]
            if 0 <= counterParts['index'] < len(instanceData):
                dataObj = instanceData[counterParts['index']]
            else:
                return counterDef, None

        counterValue = dataObj.data[counterParts['counter']]
        return counterDef, counterValue

def getCounterValue(path, pd, prev):
    """
    Calculates the current value for a specified performance collector with a
    current and optional previous PerformanceData objects.
    """
    #
    # The details on how to calculate counter values are provided at the 
    # following web address:
    #   http://msdn.microsoft.com/en-us/library/aa371891(VS.85).aspx
    #
    counterParts = parseCounter(path)
    currCounterDef, currCounterValue = pd.getCounter(counterParts)
    if prev:
        prevCounterDef, prevCounterValue = prev.getCounter(counterParts)

    if currCounterValue is None:
        return None

    if prev and prevCounterValue is None:
        prev = False

    try:
        #
        # ((N1 - N0) / (D1 - D0)) / F
        #
        if prev and currCounterDef.counterType in (PERF_COUNTER_COUNTER,
                                                   PERF_SAMPLE_COUNTER,
                                                   PERF_COUNTER_BULK_COUNT):
            numerator = currCounterValue.data - prevCounterValue.data
            denominator = currCounterValue.time - prevCounterValue.time
            value = float(numerator) / (float(denominator) / float(currCounterValue.frequency))

        #
        # (N1 - N0) / (D1 - D0)
        #
        elif prev and currCounterDef.counterType in (PERF_COUNTER_QUEUELEN_TYPE,
                                                     PERF_AVERAGE_BULK,
                                                     PERF_COUNTER_LARGE_QUEUELEN_TYPE,
                                                     PERF_COUNTER_100NS_QUEUELEN_TYPE,
                                                     PERF_COUNTER_OBJ_TIME_QUEUELEN_TYPE):
            numerator = currCounterValue.data - prevCounterValue.data
            denominator = currCounterValue.time - prevCounterValue.time
            value = float(numerator) / float(denominator)

        #
        # 100 * (N1 - N0) / (D1 - D0)
        #
        elif prev and currCounterDef.counterType in (PERF_COUNTER_TIMER,
                                                     PERF_100NSEC_TIMER,
                                                     PERF_OBJ_TIME_TIMER,
                                                     PERF_PRECISION_SYSTEM_TIMER,
                                                     PERF_PRECISION_100NS_TIMER,
                                                     PERF_PRECISION_OBJECT_TIMER):
            numerator = currCounterValue.data - prevCounterValue.data
            denominator = currCounterValue.time - prevCounterValue.time
            value = 100.0 * float(numerator) / float(denominator)
        
        #
        # 100 * (1 - ((N1 - N0)/(D1 - D0)))
        #
        elif prev and currCounterDef.counterType == PERF_COUNTER_TIMER_INV:
            numerator = currCounterValue.data - prevCounterValue.data
            denominator = currCounterValue.time - prevCounterValue.time
            value = 100.0 * (1.0 - (float(numerator) / float(denominator)))
        
        #
        # 100 * (1- (N1 - N0) / (D1 - D0))
        #
        elif prev and currCounterDef.counterType == PERF_100NSEC_TIMER_INV:
            numerator = currCounterValue.data - prevCounterValue.data
            denominator = currCounterValue.time - prevCounterValue.time
            value = 100.0 * (1.0 - (float(numerator) / float(denominator)))
        
        #
        # 100 * ((N1 - N0) / (D1 - D0) / TB)) / B1
        #
        elif prev and currCounterDef.counterType == PERF_COUNTER_MULTI_TIMER:
            numerator = currCounterValue.data - prevCounterValue.data
            denominator = currCounterValue.time - prevCounterValue.time
            denominator = float(denominator) / float(currCounterValue.frequency)
            value = 100.0 * (float(numerator) / denominator) / float(currCounterValue.multiCounterData)
            
        #
        # 100 * ((N1 - N0) / (D1 - D0)) / B1
        #
        elif prev and currCounterDef.counterType == PERF_100NSEC_MULTI_TIMER:
            numerator = currCounterValue.data - prevCounterValue.data
            denominator = currCounterValue.time - prevCounterValue.time
            value = 100.0 * (float(numerator) / float(denominator)) / float(currCounterValue.multiCounterData)
        
        #
        # 100 * (B1 - ((N1 - N0) / (D1 - D0)))
        #
        elif prev and currCounterDef.counterType in (PERF_COUNTER_MULTI_TIMER_INV,
                                                     PERF_100NSEC_MULTI_TIMER_INV):
            numerator = currCounterValue.data - prevCounterValue.data
            denominator = currCounterValue.time - prevCounterValue.time
            value = 100.0 * (float(currCounterValue.multiCounterData) - (float(numerator) / float(denominator)))
        
        #
        # raw counter
        #
        elif currCounterDef.counterType in (PERF_COUNTER_RAWCOUNT, 
                                            PERF_COUNTER_LARGE_RAWCOUNT, 
                                            PERF_COUNTER_RAWCOUNT_HEX, 
                                            PERF_COUNTER_LARGE_RAWCOUNT_HEX):
            value = currCounterValue.data

        #
        # N1 - N0
        #
        elif prev and currCounterDef.counterType in (PERF_COUNTER_DELTA, 
                                                     PERF_COUNTER_LARGE_DELTA):
            value = float(currCounterValue.data) - float(prevCounterValue.data)

        #
        # 100 * N/B
        #
        elif currCounterDef.counterType in (PERF_SAMPLE_FRACTION,
                                            PERF_RAW_FRACTION, 
                                            PERF_LARGE_RAW_FRACTION):
            value = 100.0 * float(currCounterValue.data) / float(currCounterValue.time)
        
        #
        # ((N1 - N0) / TB) / (B1 - B0)
        #
        elif prev and currCounterDef.counterType == PERF_AVERAGE_TIMER:
            numerator = currCounterValue.data - prevCounterValue.data
            denominator = currCounterValue.time - prevCounterValue.time
            value = float(numerator) / float(currCounterValue.frequency) / float(denominator)
        
        #
        # (D0 - N0) / F
        #
        elif currCounterDef.counterType == PERF_ELAPSED_TIME:
            value = (float(currCounterValue.time) - float(currCounterValue.data)) / float(currCounterValue.frequency)
            
        else:
            return None

        # System Up Time is being corrected here because it is returned
        # in seconds, but we expect it in centiseconds
        valueAsFloat = float(value)
        if counterParts == {'object': 'system',
                            'counter': 'system up time', 
                            'instance': None, 
                            'index': 0, 
                            'parent': None, 
                            }:
            log.debug('For \\System\\System Up Time counter, multiplying %f * 100', 
                 valueAsFloat )            
            valueAsFloat *= 100

        return valueAsFloat

    except ZeroDivisionError:
        return 0.0

from pysamba.library import *
from pysamba.rpc.dcerpc import policy_handle

class winreg_OpenHKPT_in(Structure):
    _fields_ = [
        ('system_name', POINTER(uint16_t)),
        ('access_mask', uint32_t),
        ]

class winreg_OpenHKPT_out(Structure):
    _fields_ = [
        ('handle', POINTER(policy_handle)),
        ('result', WERROR),
        ]
    
class winreg_OpenHKPT(Structure):
    _fields_ = [
        ('_in', winreg_OpenHKPT_in),
        ('out', winreg_OpenHKPT_out),
        ]

        
class winreg_String(Structure):
    _fields_ = [
        ('name_len', uint16_t),
        ('name_size', uint16_t),
        ('name', c_char_p),
        ]

class winreg_QueryValue_In(Structure):
    _fields_ = [
        ('handle', POINTER(policy_handle)),
        ('value_name', winreg_String),
        ('type', POINTER(enum)),
        ('data', POINTER(uint8_t)),
        ('size', POINTER(uint32_t)),
        ('length', POINTER(uint32_t)),
        ]

class winreg_QueryValue_Out(Structure):
    _fields_ = [
        ('type', POINTER(enum)),
        ('data', POINTER(uint8_t)),
        ('size', POINTER(uint32_t)),
        ('length', POINTER(uint32_t)),
        ('result', WERROR),
        ]

class winreg_QueryValue(Structure):
    _fields_ = [
        ('_in', winreg_QueryValue_In),
        ('out', winreg_QueryValue_Out),
        ]

class winreg_CloseKey_In(Structure):
    _fields_ = [
        ('handle', POINTER(policy_handle)),
        ]
    
class winreg_CloseKey_Out(Structure):
    _fields_ = [
        ('handle', POINTER(policy_handle)),
        ('result', WERROR),
        ]
    
class winreg_CloseKey(Structure):
    _fields_ = [
        ('_in', winreg_CloseKey_In),
        ('out', winreg_CloseKey_Out),
        ]

class winreg_OpenHKPD_in(Structure):
    _fields_ = [
        ('system_name', POINTER(uint16_t)),
        ('access_mask', uint32_t),
        ]
    
class winreg_OpenHKPD_out(Structure):
    _fields_ = [
        ('handle', POINTER(policy_handle)),
        ('result', WERROR),
        ]
    
class winreg_OpenHKPD(Structure):
    _fields_ = [
        ('_in', winreg_OpenHKPD_in),
        ('out', winreg_OpenHKPD_out),
        ]
