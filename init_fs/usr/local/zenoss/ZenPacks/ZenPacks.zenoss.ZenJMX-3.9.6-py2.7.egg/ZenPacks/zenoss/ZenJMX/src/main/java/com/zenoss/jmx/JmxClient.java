/*****************************************************************************
 * 
 * Copyright (C) Zenoss, Inc. 2008, all rights reserved.
 * 
 * This content is made available according to terms specified in
 * License.zenoss under the directory where your Zenoss product is installed.
 * 
 ****************************************************************************/


package com.zenoss.jmx;

import java.io.IOException;
import java.lang.management.ManagementFactory;
import java.net.MalformedURLException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.management.MBeanServerConnection;
import javax.management.MalformedObjectNameException;
import javax.management.ObjectName;
import javax.management.openmbean.CompositeDataSupport;
import javax.management.openmbean.InvalidKeyException;
import javax.management.openmbean.TabularData;
import javax.management.remote.JMXConnector;
import javax.management.remote.JMXConnectorFactory;
import javax.management.remote.JMXServiceURL;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

/**
 * <p>
 * JmxClient is a Java client to JMX Agents. It supports authentication
 * information.
 * </p>
 * 
 * <p>
 * Users of JmxClient can connect to JMX Agents, authenticate, and obtain copies
 * of attribute values that exist on the server. Multi-value attributes are
 * supported via key attributes that can be passed.
 * </p>
 * 
 * <p>
 * $Author: chris $<br>
 * $Date: 2005/03/13 18:45:25 $
 * </p>
 * 
 * @author Christopher Blunck
 * @version $Revision: 1.6 $
 */
public class JmxClient {
    // url that describes the agent to connect to
    private JMXServiceURL _url;

    // credentials to offer when connecting to the JMX Agent
    private String[] _creds;

    // factory used to create connections to the url
    private JMXConnector _connector;

    // connection to remote JMX Agent
    private MBeanServerConnection _server;

    // flag used to track if we are connected to the server or not
    private boolean _connected;
    
    // logger
    private static final Log _logger = LogFactory.getLog(JmxClient.class);

    /**
     * Creates a JmxClient for interacting with the local Platform MBeanServer
     * 
     */
    public JmxClient()
        {
        _server = ManagementFactory.getPlatformMBeanServer(); 
        _connected = true;
        }
    /**
     * Creates a JmxClient that will interrogate the JMX Agent at the URL
     * provided.
     * 
     * @param url
     *            an Abstract Service URL for SLP, as defined in RFC 2609 and
     *            amended by RFC3111 (e.g. service:jmx:protocol:sap)
     * @throws IllegalArgumentException
     *             if the URL provided is malformed
     */
    public JmxClient(String url) throws IllegalArgumentException
        {

        try
            {
            _url = new JMXServiceURL(url);
            }
        catch (MalformedURLException e)
            {
            throw new IllegalArgumentException(e);
            }
        }

    /**
     * Sets authentication and authorization credentials
     */
    public void setCredentials(String[] creds)
        {
        _creds = creds;
        }

    /**
     * Connects to the JMX Agent
     * 
     * @throws JMXException
     *             if an exception occurs during connection
     */
    public void connect() throws JmxException
        {

        // short-circuit to avoid re-connecting
        if ( _connected )
            {
            return;
            }

        try
            {
            // honor the authentication credentials
            Map<String,Object> env = new HashMap<String,Object>();
            env.put(JMXConnector.CREDENTIALS, _creds);

            _connector = JMXConnectorFactory.connect(_url, env);
            _server = _connector.getMBeanServerConnection();
            }
        catch (IOException e)
            {
            throw new JmxException("Failed to connect to " + _url, e);
            }

        _connected = true;
        }

    /**
     * Closes the conncetion to the JMX Agent
     * 
     * @throws JmxException
     *             if an exception occurs while closing down the connection
     */
    public void close() throws JmxException
        {
        try
            {
            if ( _connected )
                {
                try
                    {
                    if(_connector != null)
                        {
                        _connector.close();
                        }
                    }
                catch (IOException e)
                    {
                    throw new JmxException(e);
                    }
                }
            }
        finally
            {
            _connected = false;
            _connector = null;
            _server = null;
            _creds = null;
            }
        }

    /**
     * Builds an ObjectName using the name provided
     * 
     * @param name
     *            the MBean name
     * @throws JmxException
     *             if the mbean name is not a properly formatted object name.
     */
    private ObjectName buildObjectName(String name) throws JmxException
        {

        // construct the object name, making sure it is properly formatted
        ObjectName on = null;
        try
            {
            on = new ObjectName(name);
            }
        catch (MalformedObjectNameException e)
            {
            throw new JmxException("object name is malformed: " + name);
            }

        return on;
        }

    /**
     * Queries the JMX Agent and retrieves the attribute requested
     * 
     * @param objectName
     *            the name of the MBean
     * @param attribute
     *            the attribute to query
     * @return the Attribute that was read from the server
     * @throws JMXException
     *             if an error occurs while querying
     */
    public Object query(String objectName, String attributeName)
            throws JmxException
        {

        // make sure we're connected
        if ( !_connected )
            {
            throw new JmxException("not connected");
            }

        // make sure the mbean described by the object name is registered
        ObjectName on = buildObjectName(objectName);
        checkRegistration(on);

        // get the attribute on the mbean requested
        Object attribute = null;
        try
            {
            attribute = _server.getAttribute(on, attributeName);
            }
        catch (Exception e)
            {
            String message = "error occurred while accessing attribute '"
                    + attributeName + "' on object '" + on + "'";
            throw new JmxException(message, e);
            }

        return attribute;
        }

    /**
     * Invokes the requested operation on the MBean provided, returning the
     * result as an Object.
     * 
     * @param objectName
     *            the name of the MBean
     * @param operation
     *            the name of the method to invoke on the MBean
     * @param params
     *            parameters to be passed to the operation
     * @param types
     *            array of class names (in String format) that represent the
     *            types of the parameters.
     * @throws JmxException
     *             if any exception occurs during processing
     */
    public Object invoke(String objectName, String operation, Object[] params,
            String[] types) throws JmxException
        {

        // make sure we're connected
        if ( !_connected )
            {
            throw new JmxException("not connected");
            }

        // make sure the mbean described by the object name is registered
        ObjectName on = buildObjectName(objectName);
        checkRegistration(on);

        // invoke the operation
        Object result = null;
        try
            {
            result = _server.invoke(on, operation, params, types);
            }
        catch (Exception e)
            {
            throw new JmxException("error occurred while invoking method", e);
            }

        return result;
        }

    /**
     * Verifies that the ObjectName provided is registered in the JMX Agent. If
     * the ObjectName is not registered a JmxException is raised
     * 
     * @param on
     *            the MBean name to check
     * @throws JmxException
     *             if no MBean is located with the name provided in the
     *             ObjectName
     */
    private void checkRegistration(ObjectName on) throws JmxException
        {

        try
            {
            if ( !_server.isRegistered(on) )
                {
                throw new JmxException("no MBean registered with name: " + on);
                }
            }
        catch (IOException e)
            {
            String msg = "error occurred while checking if mbean with name '"
                    + on + "' is registered";
            throw new JmxException(msg, e);
            }
        }

    /**
     * Queries the Jmx Agent and retrieves a multi-value attribute. Extracts the
     * attribute with the key provided.
     * 
     * @param objectName
     *            the name of the MBean
     * @param attribute
     *            the multi-value attribute to query
     * @param keys
     *            the keys of the multi-value attributes to query
     * @return a Map<String, Object> where the key is the attribute name and the
     *         value is the value retreived from the JMX Agent
     * @throws JmxException
     *             if an error occurs while querying
     */
    public Map<String, Object> query(String objectName, String attribute,
            List<String> keys, String dataPath) throws JmxException
        {

        _logger.debug("using the following keys: " + keys);
        _logger.debug("using the following attribute: " + attribute);
        _logger.debug("using the following string: " + objectName);
        String path = dataPath;
        // issue the query
        Object value = query(objectName, attribute);

        if ( path != null && path.length() > 0 )
            {
            _logger.debug("Extracting data with path " + path);
            try
                {
                value = ValueExtractor.getDataValue(value, path);
                }
            catch (IllegalArgumentException e)
                {

                _logger.warn("Could not process path " + path + " on object "
                        + value, e);
                throw new JmxException("Could not process path " + path
                        + " on object of type " + value.getClass().getName());
                }
            catch (RuntimeException e)
                {
                _logger.warn("error processing path " + path + " on object "
                        + value, e);
                throw new JmxException("error processing path " + path, e);
                }
            }

        // marshal composite values into
        Map<String, Object> values = null;

        if ( value instanceof CompositeDataSupport 
                || value instanceof TabularData
                || value instanceof Map )
            {
            values = mapValues(value, keys);
            }
        // if the attribute wasn't multi-value just return the attribute
        else
            {
            _logger.debug("dealing with other data");
            values = new HashMap<String, Object>();
            values.put(keys.iterator().next(), value);
            }

        return values;
        }

    private Map<String, Object> mapValues(Object obj, List<String> dataPointKeys)
        {
        HashMap<String, Object> values = new HashMap<String, Object>();
        for (String dataPoint : dataPointKeys)
            {
            try
                {
                _logger.debug(
                    "Extracting value for datapoint '" + dataPoint + "'");
                Object value = ValueExtractor.getDataValue(obj, dataPoint);
                values.put(dataPoint, value);
                }
            catch (Exception e)
                {
                _logger.warn(
                    "Failed to extract value for datapoint '" 
                    + dataPoint + "'; " + e.getMessage());
                }
            }
        return values;
        }
    

}
