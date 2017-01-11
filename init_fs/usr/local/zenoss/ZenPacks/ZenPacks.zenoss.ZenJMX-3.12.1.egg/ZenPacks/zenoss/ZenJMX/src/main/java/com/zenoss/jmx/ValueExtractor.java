/*****************************************************************************
 * 
 * Copyright (C) Zenoss, Inc. 2008, all rights reserved.
 * 
 * This content is made available according to terms specified in
 * License.zenoss under the directory where your Zenoss product is installed.
 * 
 ****************************************************************************/


package com.zenoss.jmx;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.Set;
import java.util.Map;
import java.util.regex.Pattern;

import javax.management.openmbean.CompositeData;
import javax.management.openmbean.TabularData;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

public class ValueExtractor {

    private static final Log _logger = LogFactory.getLog(ValueExtractor.class);

    /**
     * Traverses a TabularData or CompositeData structure to return nested data
     * 
     * e.g. To get the the used perm gen memory before last garbage collection
     * value from the result of the lastGcInfo attribute of the
     * java.lang:type=GarbageCollector,name=Copy mbean the path used would be
     * 
     * memoryUsageBeforeGc.[Perm Gen].used
     * 
     * In general the non bracketed values are keys into CompositeData and the
     * bracketed values are indexes into TabularData. For TabularData indexes
     * with more than one value a comma separated list without spaces should be
     * used, spaces are treated as part of the values in the index array.
     * 
     * e.g. [key1,key2]
     * 
     * The brackets aren't mandatory for indexes but are included for clarity.
     * 
     * Curly brackets can be used after a table index to specify a column name.
     * 
     * e.g memoryUsageBeforeGc.[Perm Gen].{value}.used
     * 
     * The column name is only necessary when the table has more than two
     * columns. If the table has two columns then the value is read from the
     * column not used for the index.
     * 
     * @param obj
     *            TabularData, CompositeData, or Map
     * @param path
     *            dot separated string that represents a path through the object
     * @return Object the value at the end of the path
     * @throws JmxException
     *             if a path element doesn't exist
     */
    public static Object getDataValue(final Object obj, String path)
            throws JmxException
        {
        if ( !(obj instanceof TabularData)
                && !(obj instanceof CompositeData)
                && !(obj instanceof Map) )
            {

            throw new IllegalArgumentException("Cannot process object of type "
                    + obj.getClass().getName());

            }

        _logger.debug("getDataValue: path is " + path);

        List<String> pathList = split(path);
        _logger.debug("getDataValue: pathList " + pathList);

        Object currentObj = obj;
        Iterator<String> pathElements = pathList.iterator();
        try
            {
            while (pathElements.hasNext())
                {
                _logger.debug("getDataValue: current object is " + obj);
                String currentKey = pathElements.next();
                pathElements.remove();

                _logger.debug("getDataValue: currentKey: " + currentKey);

                if ( currentObj instanceof TabularData )
                    {
                    _logger.debug("getDataValue: dealing with tabularData");
                    TabularData tData = (TabularData) currentObj;

                    String[] index = createTableIndex(currentKey);
                    currentObj = getDataByTableIndex(tData, index);
                    CompositeData cData = (CompositeData) currentObj;

                    int columnCount = cData.values().size();
                    String nextKey = null;

                    // look ahead and look for explicit column
                    if ( !pathList.isEmpty() )
                        {
                        nextKey = pathList.get(0);
                        }

                    if ( nextKey != null
                            && (isColumn(nextKey) || columnCount > 2) )
                        {

                        String columnKey = pathElements.next();
                        pathElements.remove();
                        if ( isColumn(columnKey) )
                            {
                            _logger.debug("using explicit column key "
                                    + columnKey + " for tabular data");
                            // remove first and last char - should be curly
                            // brackets
                            columnKey = columnKey.substring(1, columnKey
                                    .length() - 1);
                            }
                        else
                            {
                            _logger
                                    .debug("using column key "
                                            + columnKey
                                            + " for tabular data. No curly brackets found");
                            }
                        currentObj = getData(cData, columnKey);
                        }
                    else if ( cData.values().size() == 2 )
                        {
                        currentObj = getTableRowData(cData, index);
                        }
                    }
                else if ( currentObj instanceof CompositeData )
                    {
                    _logger.debug("getDataValue: dealing with CompositeData");
                    CompositeData cData = (CompositeData) currentObj;
                    currentObj = getData(cData, currentKey);
                    }
                else if ( currentObj instanceof Map )
                    {
                    _logger.debug("getDataValue: dealing with Map");
                    Map mData = (Map) currentObj;
                    currentObj = getData(mData, currentKey);
                    }
                else
                    {
                    // we still have a path but the object isn't composite or
                    // tabluar
                    String remainingPath = currentKey;
                    for (String val : pathList)
                        {
                        remainingPath += ".";
                        remainingPath += val;

                        }
                    _logger.warn("getDataValue: we still have a path but the "
                            + "object isn't composite or tabluar");
                    _logger.warn("getDataValue: remaining path is "
                            + remainingPath);
                    throw new JmxException("we still have a path but the "
                            + "object isn't composite or tabluar, remaining "
                            + "" + "path is " + remainingPath);

                    }

                }
            }
        catch (Exception e)
            {
            _logger.warn("could not get object for path " + path, e);
            throw new JmxException("could not get object for path " + path
                    + "; " + e.getMessage(), e);
            }
        return currentObj;
        }

    private static boolean isColumn(String key)
        {
        return key.startsWith("{") && key.endsWith("}");
        }

    private static Object getData(CompositeData cData, String key)
        {
        _logger.debug("composite data is: " + cData);
        _logger.debug("getting '" + key + "' from composite data");
        Object result = cData.get(key);
        _logger.debug("value from composite data is " + result);
        return result;
        }

    private static Object getData(Map mData, String key)
        {
        _logger.debug("map data is: " + mData);
        _logger.debug("getting '" + key + "' from map data");
        Object result = mData.get(key);
        _logger.debug("value from map data is " + result);
        return result;
        }

    private static String[] createTableIndex(String currentKey)
        {
        String index = null;
        if ( currentKey.startsWith("[") && currentKey.endsWith("]") )
            {
            _logger.debug("getDataValue: looks like an explicit index: "
                    + currentKey);
            // remove first and last char - should be brackets
            index = currentKey.substring(1, currentKey.length() - 1);
            }
        else
            {
            _logger.debug("getDataValue: no explicit index: " + currentKey);
            // no explicit table index,
            // assume index is the same as the name of the value
            index = currentKey;
            }

        _logger.debug("spliting " + index + " for index ");
        String[] indexValues = index.split(",");

        _logger.debug("index is " + Arrays.toString(indexValues));

        return indexValues;
        }

    private static Object getDataByTableIndex(TabularData tData,
            String[] tableIndex) throws JmxException
        {
        _logger.debug("TablularData is: " + tData);

        _logger.debug("extracting composite data from tabulardata with index "
                + Arrays.toString(tableIndex));
        CompositeData composite = (CompositeData) tData.get(tableIndex);
        if ( composite == null )
            {
            throw new JmxException(Arrays.toString(tableIndex)
                    + " is not an existing Index for this tabular data ");
            }
        _logger.debug("extracted composite data: " + composite);
        return composite;
        }

    private static Object getTableRowData(CompositeData cData, String[] index)
            throws JmxException
        {
        Object result = null;
        // This gets the data with a key not in index
        Set<String> keys = new HashSet<String>(Arrays.asList(index));

        for (String key : keys)
            {
            if ( !cData.values().contains(key) )
                {
                _logger.warn(key
                        + " not found in composite data row for tabular data");
                throw new JmxException(key
                        + " not found in composite data row for tabular data");

                }
            }

        // find the first value that isn't a part of the index
        for (Object value : cData.values())
            {
            if ( !keys.contains(value) )
                {
                result = value;
                }
            }
        return result;
        }

    /**
     * split a string on dots but leave values within brackets ([,}) that have dots intact
     * for example the string "test.{bracket.stuff}" should be split to an array 
     * [test, {bracket.stuff}]
     * 
     * @param path
     * @return
     */
    public static LinkedList<String> split(String path)
        {

        String[] splitPath = dotPattern.split(path);
        Iterator<String> pathElements = Arrays.asList(splitPath).iterator();
        LinkedList<String> resultPath = new LinkedList<String>();
        while (pathElements.hasNext())
            {
            String pathElement = pathElements.next();

            while (bracketStart.matcher(pathElement).matches()
                    && notBracketEnd.matcher(pathElement).matches()
                    && pathElements.hasNext())
                {
                pathElement = pathElement + "." + pathElements.next();

                }
            resultPath.add(pathElement);
            }
        return resultPath;
        }

    private static Pattern dotPattern = Pattern.compile("\\.");
    private static Pattern bracketStart = Pattern.compile("^[\\{\\[].*");
    private static Pattern notBracketEnd = Pattern.compile(".*[^\\}\\]]$");

}
