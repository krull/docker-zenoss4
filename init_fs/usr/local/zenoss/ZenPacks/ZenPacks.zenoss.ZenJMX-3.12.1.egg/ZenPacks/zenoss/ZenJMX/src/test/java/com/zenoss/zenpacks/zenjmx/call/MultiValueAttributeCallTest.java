/*****************************************************************************
 * 
 * Copyright (C) Zenoss, Inc. 2008, all rights reserved.
 * 
 * This content is made available according to terms specified in
 * License.zenoss under the directory where your Zenoss product is installed.
 * 
 ****************************************************************************/


package com.zenoss.zenpacks.zenjmx.call;

import junit.framework.*;
import junit.textui.TestRunner;

import java.util.List;
import java.util.ArrayList;


/**
 * <p> Tests the methods in the MultiValueAttributeCall class.  Don't
 * feel reassured though - the extensiveness of the test is
 * lacking...  </p>
 *
 * <p>$Author: chris $</p>
 *
 * @author Christopher Blunck
 * @version $Revision: 1.6 $
 */
public class MultiValueAttributeCallTest
  extends TestCase {

  // the configuration for the call
  private static final String URL = 
    "service:jmx:jmxrmi://localhost:12345/mbean";
  private static final boolean AUTHENTICATE = true;
  private static final String USERNAME = "username";
  private static final String PASSWORD = "password";
  private static final String OBJECT_NAME = "mbean";
  private static final String ATTR_NAME = "attribute";
  private static final String ATTR_TYPE = "attribute type";

  private static List<String> KEYS;
  private static List<String> TYPES;

  private AttributeCall _call1;
  private AttributeCall _call2;


  static {
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
  public MultiValueAttributeCallTest(String method) {
    super(method);
  }


  /**
   * Called before each method is invoked
   */
  public void setUp() { 
//    _call1 = 
//      new MultiValueAttributeCall(URL, AUTHENTICATE, 
//                                  USERNAME, PASSWORD, 
//                                  OBJECT_NAME, ATTR_NAME,
//                                  KEYS, TYPES);
//
//    _call2 = 
//      new MultiValueAttributeCall(URL, AUTHENTICATE, 
//                                  USERNAME, PASSWORD, 
//                                  OBJECT_NAME, ATTR_NAME,
//                                  KEYS, TYPES);
  }


  /**
   * Called after each method finishes execution
   */
  public void tearDown() { 
    _call1 = null;
    _call2 = null;
  }


  /**
   * Defines the list of test methods to run.  By default we'll run
   * 'em all.
   */
  public static Test suite() {
    TestSuite suite = new TestSuite(MultiValueAttributeCallTest.class);
    return suite;
  }

  
  /**
   * Runs all the tests via the command line.
   */
  public static void main(String[] args) {
    TestRunner.run(MultiValueAttributeCallTest.class);
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
}
