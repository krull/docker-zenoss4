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

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;


/**
 * <p> Bean that carries results of a Call (along with some metadata)
 * between the Callables and the Processor.  </p>
 *
 * <p>$Author: chris $</p>
 *
 * @author Christopher Blunck
 * @version $Revision: 1.6 $
 */
public class Summary {

  // the id of the call that generated this summary
  private int _callId;

  // the device id that this summary corresponds to
  private String _deviceId;

  // the name of the data source this summar corresponds to
  private String _dataSourceId;

  // the results of the JMX call
  private Map<String, Object> _results;

  // maps datapoint names to the rrdtype they are stored in
  private Map<String, String> _typeMap;

  // the name of the object the request was issued against
  private String _objectName;

  // a textual description of the call that geerated this summary
  private String _callSummary;

  // the amount of time it took to execute the call
  private long _runtime;

  // flag indicating the call was cancelled
  private boolean _cancelled = false;

  // logger
  private static final Log _logger = LogFactory.getLog(Summary.class);


  /**
   * Vanilla constructor to follow bean pattern
   */
  public Summary() { }

  /**
   * Accessor method for _deviceId field
   */
  public String getDeviceId() { return _deviceId; }

  /**
   * Mutator method for _deviceId field
   */
  public void setDeviceId(String deviceId) { _deviceId = deviceId; }


  /**
   * Accessor method for _objectName field
   */
  public String getObjectName() { return _objectName; }

  /**
   * Mutator method for _objectName field
   */
  public void setObjectName(String objectName) { _objectName = objectName; }


  /**
   * Accessor method for _callSummary field
   */
  public String getCallSummary() { return _callSummary; }

  /**
   * Mutator method for _callSummary field
   */
  public void setCallSummary(String callSummary) { _callSummary = callSummary; }


  /**
   * Accessor method for _dataSource field
   */
  public String getDataSourceId() { return _dataSourceId; }

  /**
   * Mutator method for _dataSource field
   */
  public void setDataSourceId(String dataSourceId) { 
    _dataSourceId = dataSourceId; 
  }


  /**
   * Accessor method for _results field
   */
  public Map getResults() { return _results; }

  /**
   * Mutator method for _results field
   */
  public void setResults(Map<String, Object> results) { _results = results; }


  /**
   * Accessor method for _typeMap field
   */
  public Map<String, String> getTypeMap() { return _typeMap; }

  /**
   * Mutator method for _typeMap field
   */
  public void setTypeMap(Map<String, String> typeMap) { _typeMap = typeMap; }


  /**
   * Accessor method for _runtime field
   */
  public long getRuntime() { return _runtime; }

  /**
   * Mutator method for _runtime field
   */
  public void setRuntime(long runtime) { _runtime = runtime; }


  /**
   * Accessor method for _cancelled field
   */
  public boolean isCancelled() { return _cancelled; }


  /**
   * Mutator method for _cancelled field
   */
  public void setCancelled(boolean cancelled) { _cancelled = cancelled; }


  /**
   * Accessor method for _callId field
   */
  public Integer getCallId() { return _callId; }


  /**
   * Mutator method for _callId field
   */
  public void setCallId(Integer callId) { _callId = callId; }


  /**
   * @see Object#toString
   */
  public String toString() {
    return "Summary:\n" +
      "\tdeviceId: " + getDeviceId() + "\n" +
      "\tdatasourceId: " + getDataSourceId() + "\n" +
      "\tobjectName: " + getObjectName() + "\n" +
      "\tcallSummary: " + getCallSummary() + "\n" +
      "\truntime: " + getRuntime() + "\n" +
      "\tcallId: " + getCallId() + "\n" +
      "\tcancelled: " + isCancelled() + "\n" +
      "\tresults: " + getResults() + "\n";
  }


  /**
   * @see Object#equals
   */
  public boolean equals(Object other) {
    if (! (other instanceof Summary)) {
      return false;
    }

    boolean toReturn = true;

    Summary summary = (Summary) other;

    toReturn &= Utility.equals(summary.getCallId(), getCallId());
    toReturn &= Utility.equals(summary.getDeviceId(), getDeviceId());
    toReturn &= Utility.equals(summary.getDataSourceId(), getDataSourceId());
    toReturn &= Utility.equals(summary.getResults(), getResults());
    toReturn &= Utility.equals(summary.getTypeMap(), getTypeMap());
    toReturn &= Utility.equals(summary.getObjectName(), getObjectName());
    toReturn &= Utility.equals(summary.getCallSummary(), getCallSummary());
    toReturn &= summary.getRuntime() == getRuntime();
    toReturn &= summary.isCancelled() == isCancelled();
    
    return toReturn;
  }

}
