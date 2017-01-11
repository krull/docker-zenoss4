/*****************************************************************************
 * 
 * Copyright (C) Zenoss, Inc. 2008, all rights reserved.
 * 
 * This content is made available according to terms specified in
 * License.zenoss under the directory where your Zenoss product is installed.
 * 
 ****************************************************************************/


package com.zenoss.zenpacks.zenjmx.call;

import java.util.Map;

import com.zenoss.zenpacks.zenjmx.call.JMXTestData.NestedDataRow;

public interface ZenJMXTestMXBean {

    public JMXTestData getCompositeTestData();
    public Map<String, NestedDataRow> getTabularTestData();
    public Map<String, Integer> getSimpleTabularTestData();
    public Map<Integer, Integer> getIndexedTabularTestData();


}
