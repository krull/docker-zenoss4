/*****************************************************************************
 * 
 * Copyright (C) Zenoss, Inc. 2008, all rights reserved.
 * 
 * This content is made available according to terms specified in
 * License.zenoss under the directory where your Zenoss product is installed.
 * 
 ****************************************************************************/


package com.zenoss.zenpacks.zenjmx.call;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;

public class JMXTestData implements Serializable {

    /**
     * 
     */
    private static final long serialVersionUID = 4003588084046125117L;

    public int valueOne = 989;
    public String stringValue = "123";

    public int getValueOne()
        {
        return valueOne;
        }

    public String getStringValue()
        {
        return stringValue;
        }

    public NestedData getNested()
        {
        return new NestedData();
        }

    public static class NestedData {

        public String getNestedValue()
            {
            return nestedValue;
            }

        public Map<String, NestedDataRow> getRows()
        {
        Map<String, NestedDataRow> result = new HashMap<String, NestedDataRow>();
        
        result.put("rowOne", new NestedDataRow(654,384,938));
        result.put("rowTwo", new NestedDataRow(1,2,3));
        result.put("row.Three", new NestedDataRow(3,2,1));

        return result;
            
        }

        public String nestedValue = "321";
    }

    public static class NestedDataRow {

    
        public NestedDataRow(int anotherRowValue, int differntRowValue,
                int rowValue)
            {
            super();
            this.anotherRowValue = anotherRowValue;
            this.differntRowValue = differntRowValue;
            this.rowValue = rowValue;
            }

        private int rowValue = 654;
        private int anotherRowValue = 938;
        private int differntRowValue = 384;

        public int getRowValue()
            {
            return rowValue;
            }

        public int getAnotherRowValue()
            {
            return anotherRowValue;
            }

        public int getDifferentRowValue()
            {
            return differntRowValue;
            }
    }
}
