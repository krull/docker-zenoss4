/*****************************************************************************
 * 
 * Copyright (C) Zenoss, Inc. 2008, all rights reserved.
 * 
 * This content is made available according to terms specified in
 * License.zenoss under the directory where your Zenoss product is installed.
 * 
 ****************************************************************************/


package com.zenoss.zenpacks.zenjmx.call;

import java.util.List;
import java.util.Map;
import java.util.concurrent.Callable;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import com.zenoss.jmx.JmxClient;
import com.zenoss.jmx.JmxException;
import com.zenoss.zenpacks.zenjmx.ConfigAdapter;


/**
 * <p>
 * Call for a multi-value attribute
 * </p>
 *
 * <p>$Author: chris $</p>
 *
 * @author Christopher Blunck
 * @version $Revision: 1.6 $
 */
public class AttributeCall
  extends JmxCall {

  // configuration parameters
  public static final String ATTRIBUTE_KEY = "attributeKey";


  // the name of the attribute to query
  private String _attrName;

  // the keys of the attributes we should query
  private List<String> _keys;

  //the path to the data
  private String _attributePath;
  // logger
  private static final Log _logger = 
    LogFactory.getLog(AttributeCall.class);


  /**
   * Creates a MultiValueAttributeCall
   */
  public AttributeCall(String objectName, String attrName, List<String> keys,
            String attributePath)
        {
        super(objectName);

        _attrName = attrName;
        _keys = keys;
        _attributePath = attributePath;
        _summary.setCallSummary("attribute: " + attrName + "; attribute path "
                + _attributePath + "; (" + keys + ")");
        }


  /**
   * Returns the name of the attribute being queried
   */
  public String getAttributeName() { return _attrName; }


  /**
   * Returns the sub-attribute names that are being queried.  These
   * are the fields of the multi-value attribute we are interested in.
   */
  public List<String> getKeys() { return _keys; }


  /**
   * @throws JmxException 
 * @see Callable#call
   */
  public Summary call(JmxClient client) throws JmxException {
      // record when we started
      _startTime = System.currentTimeMillis();
      // issue the query
      Map<String, Object> values = client.query(_objectName, _attrName, _keys, _attributePath);
      
      _summary.setResults(values);
      
      // record the runtime of the call
      _summary.setRuntime(System.currentTimeMillis() - _startTime);
      
      // set our id so the processor can remove it from the reactor
      _summary.setCallId(hashCode());
    
      // return result
      return _summary;
    
  }


  /**
   * Creates a MultiValueAttributeCall from the configuration provided
   */
  public static AttributeCall fromValue(ConfigAdapter  config) 
    throws ConfigurationException {

    // ugly form of downcasting...  but XML-RPC doesn't give us a List<String>
    List<String> keys = config.getDataPoints();

    
    AttributeCall call = 
      new AttributeCall(config.getOjectName(),
                                  config.getAttributeName(),
                                  keys, config.getAttributePath());
    
    call.setDeviceId(config.getDevice());
    call.setDataSourceId(config.getDatasourceId());

    return call;
  }


  /**
   * @see Object#equals
   */
  public boolean equals(Object other) {
    if (! (other instanceof AttributeCall)) {
      return false;
    }

    boolean toReturn = super.equals(other);

    AttributeCall call = (AttributeCall) other;

    toReturn &= Utility.equals(call.getAttributeName(), getAttributeName());
    toReturn &= Utility.equals(call.getKeys(), getKeys());
    
    return toReturn;
  }
  

  /**
   * @see JmxCall#hashCode
   */
  public int hashCode() {
    int hc = 0;

    hc += super.hashCode();
    hc += hashCode(_attrName);
    hc += hashCode(_keys);

    return hc;
  }
  
}
