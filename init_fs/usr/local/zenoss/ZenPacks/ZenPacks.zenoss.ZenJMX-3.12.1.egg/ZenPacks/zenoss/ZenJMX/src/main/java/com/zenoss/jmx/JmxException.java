/*****************************************************************************
 * 
 * Copyright (C) Zenoss, Inc. 2008, all rights reserved.
 * 
 * This content is made available according to terms specified in
 * License.zenoss under the directory where your Zenoss product is installed.
 * 
 ****************************************************************************/


package com.zenoss.jmx;

/**
 * <p>
 * Tagging interfaces for all JmxExceptions.
 * </p>
 * 
 * <p>
 * $Author: chris $<br>
 * $Date: 2007/07/30 18:45:25 $
 * </p>
 * 
 * @author Christopher Blunck
 * @version $Revision: 1.6 $
 */
public class JmxException extends Exception {

    /**
     * Creates a JmxException based on some lower level exception that occurred.
     */
    public JmxException(Throwable t)
        {
        super(t);
        }

    /**
     * Creates a JmxException with a message
     */
    public JmxException(String message)
        {
        super(message);
        }

    /**
     * Creates a JmxException with a message and a Throwable
     */
    public JmxException(String message, Throwable t)
        {
        super(message, t);
        }

    @Override
    public String getMessage()
        {
        String msg = super.getMessage();
        if ( this.getCause() != null )
            {
            msg += " [Nested Exception: " + this.getCause().toString() + "]";
            }
        return msg;
        }
}
