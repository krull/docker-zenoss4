/*****************************************************************************
 * 
 * Copyright (C) Zenoss, Inc. 2008, all rights reserved.
 * 
 * This content is made available according to terms specified in
 * License.zenoss under the directory where your Zenoss product is installed.
 * 
 ****************************************************************************/


package com.zenoss.zenpacks.zenjmx.call;


/**
 * <p> Represents a problem that occurred as a result of
 * configuration.  </p>
 *
 * <p>$Author: chris $</p>
 *
 * @author Christopher Blunck
 * @version $Revision: 1.6 $
 */
public class ConfigurationException 
  extends Exception {

  /**
   * Creates a ConfigurationException based on a message and an
   * exception that caused the ConfigurationException.
   */
  public ConfigurationException(String message, Throwable t) {
    super(message, t);
  }


  /**
   * Creates a ConfigurationException given a message
   */
  public ConfigurationException(String message) {
    super(message);
  }
}
