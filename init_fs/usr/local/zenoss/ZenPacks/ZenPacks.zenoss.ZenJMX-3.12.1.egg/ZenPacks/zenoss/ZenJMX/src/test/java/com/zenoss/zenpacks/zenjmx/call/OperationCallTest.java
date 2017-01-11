/*****************************************************************************
 * 
 * Copyright (C) Zenoss, Inc. 2008, all rights reserved.
 * 
 * This content is made available according to terms specified in
 * License.zenoss under the directory where your Zenoss product is installed.
 * 
 ****************************************************************************/


package com.zenoss.zenpacks.zenjmx.call;

import static com.zenoss.zenpacks.zenjmx.call.CallFactory.DATA_POINT;
import junit.framework.*;
import junit.textui.TestRunner;

import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;

import javax.management.MBeanServer;
import javax.management.MBeanServerFactory;
import javax.management.MalformedObjectNameException;
import javax.management.ObjectName;
import javax.management.remote.JMXConnectorServer;
import javax.management.remote.JMXConnectorServerFactory;
import javax.management.remote.JMXServiceURL;


/**
 * <p>
 * Tests the methods in the OperationAttributeCall class. Don't feel reassured
 * though - the extensiveness of the test is lacking...
 * </p>
 * 
 * <p>
 * $Author: chris $
 * </p>
 * 
 * @author Christopher Blunck
 * @version $Revision: 1.6 $
 */
public class OperationCallTest
  extends TestCase {

  // the configuration for the call
  private static final String URL = 
    "service:jmx:rmi:///jndi/rmi://localhost:9999/server";
  private static final boolean AUTHENTICATE = true;
  private static final String USERNAME = "username";
  private static final String PASSWORD = "password";
  private static final String OBJECT_NAME = "mbean";
  private static final String ATTR_NAME = "attribute";
  private static final String ATTR_TYPE = "attribute type";
  private static Object[] PARAM_VALUES;
  private static String[] PARAM_TYPES;
  private static List<String> KEYS;
  private static List<String> TYPES;
  // the calls we will test
  
  private static OperationCall _call1;
  private static OperationCall _call2;

  
  private static ObjectName mbeanObjectName;
  private static JMXConnectorServer JMXServer = null;
  // staticly initialize the arrays and lists we will pass to the calls
  static {
    PARAM_VALUES = new Object[] {
      "param1", "param2"
    };

    PARAM_TYPES = new String[] {
      "java.lang.String", "java.lang.String"
    };

    KEYS = new ArrayList<String>();
    KEYS.add("key1");
    KEYS.add("key2");

    TYPES = new ArrayList<String>();
    TYPES.add("java.lang.String");
    TYPES.add("java.lang.Double");
  }


  /**
     * Constructs a test that invokes a specific test method
     */
  public OperationCallTest(String method) {
    super(method);
  }


  /**
     * Called before each method is invoked. Sets up the two call objects we
     * will use.
     */
  public void setUp() throws Exception{ 
//    _call1 = 
//      new OperationCall(URL, AUTHENTICATE, 
//                        USERNAME, PASSWORD, 
//                        OBJECT_NAME, ATTR_NAME,
//                        PARAM_VALUES,
//                        PARAM_TYPES,
//                        KEYS, TYPES);
//
//    _call2 = 
//      new OperationCall(URL, AUTHENTICATE, 
//                        USERNAME, PASSWORD, 
//                        OBJECT_NAME, ATTR_NAME,
//                        PARAM_VALUES,
//                        PARAM_TYPES,
//                        KEYS, TYPES);
//    MBeanServer mbs = MBeanServerFactory.createMBeanServer();
//    registerMbean(mbs);
//    startMBeanServer(mbs);
  }

  
  private static void startMBeanServer(MBeanServer mbs)throws Exception{
      JMXServiceURL url = new JMXServiceURL(
      "service:jmx:rmi:///jndi/rmi://localhost:9999/server");
      // Need to start an RMI registry for this to work
      // eg. "rmiresgistry 9999 &"
      JMXServer =
          JMXConnectorServerFactory.newJMXConnectorServer(url, null, mbs);

      JMXServer.start();
  }
  
  
  private static void registerMbean(MBeanServer mbs) throws Exception{
      
      
//      // Get default domain
//      //
//      String domain = mbs.getDefaultDomain();
//
//      // Create and register the SimpleStandard MBean
//      //
//      String mbeanClassName = ZenJMXTest.class.getName();
//      String mbeanObjectNameStr =
//          domain + ":type=" + mbeanClassName + ",index=1";
//      createSimpleMBean(mbs, mbeanClassName, mbeanObjectNameStr);
      
  }

  private static void createSimpleMBean(MBeanServer mbs, 
          String mbeanClassName, String mbeanObjectNameStr) throws Exception {
      
          mbeanObjectName = 
              ObjectName.getInstance(mbeanObjectNameStr);
          mbs.createMBean(mbeanClassName, mbeanObjectName);
      
  }
  /**
     * Called after each method finishes execution
     */
  public void tearDown() throws Exception { 
//    _call1 = null;
//    _call2 = null;
//    if(JMXServer != null){
//        JMXServer.stop();
//    }
//    JMXServer = null;
  }


  /**
     * Defines the list of test methods to run. By default we'll run 'em all.
     */
  public static Test suite() {
    TestSuite suite = new TestSuite(OperationCallTest.class);
    return suite;
  }

  
  /**
     * Runs all the tests via the command line.
     */
  public static void main(String[] args) {
    TestRunner.run(OperationCallTest.class);
  }


  /*
     * TEST METHODS BEGIN HERE
     */

  /**
     * Tests the hashCode() method
     */
  public void testHashCode() {
//    assertEquals(_call1.hashCode(), _call2.hashCode());
  }


  /**
     * Tests the equals() method
     */
  public void testEquals() {
//    assertTrue(_call1.equals(_call2));
  }
  
  public void testOperationStringResult() throws Exception
  {
//      List<String> keyList = new ArrayList<String>();
//      keyList.add("key");
//      List<String> typeList = new ArrayList<String>();
//      typeList.add("type");
//      List<String>emptyList = Collections.emptyList(); 
//      
//      OperationCall call = 
//      new OperationCall(URL, 
//              false,"", "", 
//              mbeanObjectName.getCanonicalName(),
//              "operationStringResult",
//              new Object[0],
//              new String[0],
//              keyList,typeList);
//      call.call();
//      assertEquals("operationStringResult", ZenJMXTest.lastCall);
//      Object[] lastArgs = ZenJMXTest.lastArgs;
//      assertTrue(Arrays.equals(new Object[0], ZenJMXTest.lastArgs));
//      assertEquals("blam", ZenJMXTest.lastReturn);

  }
  public void testOperationStrinResultAndStringArg() throws Exception
  {
//      List<String> keyList = new ArrayList<String>();
//      keyList.add("key");
//      List<String> typeList = new ArrayList<String>();
//      typeList.add("type");
//      Object[] args = new Object[]{"myArg"};
//      OperationCall call = getCall("operationStrinResultAndStringArg", "myArg",
//              "java.lang.String");
//      new OperationCall(URL, 
//              false,"", "", 
//              mbeanObjectName.getCanonicalName(),
//              "operationStrinResultAndStringArg",
//              args,
//              new String[]{"java.lang.String"},
//              keyList,typeList);
//      call.call();
//      assertEquals("operationStrinResultAndStringArg", ZenJMXTest.lastCall);
//      assertTrue(Arrays.equals(args, ZenJMXTest.lastArgs));
//      assertEquals("myArg", ZenJMXTest.lastReturn);

  }
  
  public void testOperationStringArgs() throws Exception
  {
//      List<String> keyList = new ArrayList<String>();
//      keyList.add("key");
//      List<String> typeList = new ArrayList<String>();
//      typeList.add("type");
//      Object[] args = new Object[]{"myArg0", "myArg1"};
//      OperationCall call = getCall("operationStringArgs", "myArg0, myArg1",
//              "java.lang.String, java.lang.String");
//      call.call();
//      assertEquals("operationStringArgs", ZenJMXTest.lastCall);
//      assertTrue(Arrays.equals(args, ZenJMXTest.lastArgs));
//      assertEquals("myArg0myArg1", ZenJMXTest.lastReturn);

  }
  
  public void testOperationIntResultAnIntArg() throws Exception
  {
//      List<String> keyList = new ArrayList<String>();
//      keyList.add("key");
//      List<String> typeList = new ArrayList<String>();
//      typeList.add("type");
//      int arg = 1;
//      OperationCall call = getCall("operationIntResultAnIntArg", "1", "int");
//      call.call();
//      assertEquals("operationIntResultAnIntArg", ZenJMXTest.lastCall);
//      assertTrue(Arrays.equals(new Object[]{arg}, ZenJMXTest.lastArgs));
//      assertEquals(arg, ZenJMXTest.lastReturn);

  }
  
  
//  public OperationCall getCall(String operation,String args, String types) throws Exception
//  {
////      Map config = new HashMap();
////      
////      config.put("jmxPort", "9999");
////      config.put("rmiContext", "server");
////      config.put("jmxProtocol","RMI");
////      config.put("manageIp", "localhost");
////      config.put(JmxCall.AUTHENTICATE,Boolean.FALSE);
////      config.put(OperationCall.OPERATION_PARAM_TYPES, types);
////      config.put(OperationCall.OPERATION_PARAM_VALUES, args);
////      config.put(CallFactory.DATA_POINT, new Object[]{"myDataPoint"});
////      config.put(JmxCall.TYPES, new Object[]{"rrdType"});
////      config.put(JmxCall.OBJECT_NAME, mbeanObjectName.getCanonicalName());
////      config.put(OperationCall.OPERATION_NAME, operation);
////      OperationCall call =  OperationCall.fromValue(config);
////      return call;
//  }
}
