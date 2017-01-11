/*****************************************************************************
 *
 * Copyright (C) Zenoss, Inc. 2008, all rights reserved.
 *
 * This content is made available according to terms specified in
 * License.zenoss under the directory where your Zenoss product is installed.
 *
 ****************************************************************************/


package com.zenoss.zenpacks.zenjmx;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import com.zenoss.jmx.JmxClient;
import com.zenoss.jmx.JmxException;
import com.zenoss.zenpacks.zenjmx.call.CallFactory;
import com.zenoss.zenpacks.zenjmx.call.ConfigurationException;
import com.zenoss.zenpacks.zenjmx.call.JmxCall;
import com.zenoss.zenpacks.zenjmx.call.Summary;
import com.zenoss.zenpacks.zenjmx.call.Utility;

public class ZenJmxService {
  private static final Log _logger = LogFactory.getLog(ZenJmxService.class);

  public Object collect(List<Map<?, ?>> dsConfigs) throws Exception {

    long start = System.currentTimeMillis();
    if (_logger.isDebugEnabled()) {
      _logger.debug("processing " + dsConfigs.size() + " datasources");
    }
    boolean concurrentCalls = Configuration.instance().propertyExists(
        OptionsFactory.CONCURRENT_JMX_CALLS);
    JMXCollector collector = new JMXCollector(dsConfigs, concurrentCalls);
    List<Map<String, String>> result = collector.collect();
    String msg = "finished processing %1$s datasources for device %2$s in %3$s ms";
    _logger.info(String.format(msg, dsConfigs.size(), collector._deviceId,
        (System.currentTimeMillis() - start)));
    return result;
  }

  public static class JMXCollector {
    private static final String SUMMARY = "summary";
    // logger
    private static final Log _logger = LogFactory.getLog(JMXCollector.class);
    boolean _concurrentServerCalls = false;
    boolean _authenticate;
    String _username;
    String _password;
    String _deviceId;
    ConfigAdapter _config;
    List<ConfigAdapter> _configs = new ArrayList<ConfigAdapter>();

    public JMXCollector(List<Map<?, ?>> dataSourceConfigs, boolean concurrent) {
      _concurrentServerCalls = concurrent;
      ConfigAdapter config = null;
      for (Map<?, ?> configMap : dataSourceConfigs) {
        if (_logger.isDebugEnabled()) {
          String configMsg = Arrays.toString(configMap.entrySet().toArray());
          _logger.debug("processing " + configMsg );
        }
        config = new ConfigAdapter(configMap);
        _configs.add(config);
      }
      // we assume all configs are to the same device
      // and to the same jmx server with same credentials
      if (config != null) {
        _authenticate = config.authenticate();
        _username = config.getUsername();
        _password = config.getPassword();
        _config = config;
        _deviceId = config.getDevice();
      }

    }

    /**
     * collects jmx values and returns a list of results.
     *
     * @return
     */
    public List<Map<String, String>> collect() {
      List<Map<String, String>> result = new LinkedList<Map<String, String>>();
      JmxClient client = null;

      try {
          client = createJmxClient();

          client.connect();
          result.addAll(doCollect(client));
      } catch (JmxException e) {
          String msg = "Error Connecting to Server ";
          Map<String, String> error = createDeviceConnectionError(this._config, msg, e);
          result.add(error);
      } catch (Throwable e) {
            Map<String, String> error = createUnexpectedError(this._config, e);
            result.add(error);

      } finally {
        if (client != null) {
          try {
            client.close();
          } catch (JmxException e) {
              Map<String, String> error = createDeviceConnectionError(this._config,
                      "error closing connection to server", e);
              result.add(error);
          }
        }
      }
      if (_logger.isDebugEnabled()) {
        for (Map<String, String> r: result){
          Map.Entry[] entries = r.entrySet().toArray(new Map.Entry[0]);
          String msg = Arrays.toString(entries);
          _logger.debug("returning " + msg);
        }
      }
      return result;
    }

    private List<Map<String, String>> doCollect(final JmxClient client) {

      // all calls should be to same server with same credentials
      int size = _configs.size();
      final List<Map<String, String>> results = Collections
          .synchronizedList(new ArrayList<Map<String, String>>(size));
      // used to keep track of running calls
      final Map<Summary, ConfigAdapter> summaries = Collections
          .synchronizedMap(new HashMap<Summary, ConfigAdapter>());
      ExecutorService es = null;
      // create an single or multi-threaded executor
      if (_concurrentServerCalls) {
        es = Executors.newCachedThreadPool();
      } else {
        es = Executors.newSingleThreadExecutor();
      }
      for (final ConfigAdapter config : _configs) {
        try {

          final JmxCall call = CallFactory.createCall(config);
          // create job to query and create result
          Runnable job = new Runnable() {
            public void run() {
              Summary summary = call.getSummary();
              // keep track of unfinished summaries
              summaries.put(summary, config);
              try {
                call.call(client);
                results.addAll(createResult(summary, config));
              } catch (JmxException e) {
                results.add(createError(summary, config, e));
              } finally {
                summaries.remove(summary);
              }
            }


          };
          // submit job to be run
          es.execute(job);
        } catch (ConfigurationException e) {
          Map<String, String> err = createError(config, e);
          results.add(err);
        }

      }
      // shutdown the executor service and wait for all pending jobs to
      // finish
      es.shutdown();
      try {
        es.awaitTermination(5 * 60 * 1000, TimeUnit.MILLISECONDS);
      } catch (InterruptedException e) {
        for (Entry<Summary, ConfigAdapter> entry : summaries.entrySet()) {
          results.add(createTimeOutError(entry.getKey(), entry.getValue()));
        }
      }
      return results;
    }

    private JmxClient createJmxClient() throws ConfigurationException {
      JmxClient jmxClient = null;
      String url = Utility.getUrl(_config);
      jmxClient = new JmxClient(url);
      if (_authenticate) {
        String[] creds = new String[] { _username, _password };
        jmxClient.setCredentials(creds);
      }

      return jmxClient;
    }

    private List<Map<String, String>> createResult(Summary summary,
            ConfigAdapter config) {
      if (_logger.isDebugEnabled()) {
        _logger.debug(summary.toString());
      }
      List<Map<String, String>> results = new ArrayList<Map<String, String>>();

      Map<String, Object> values = summary.getResults();

      for (String key : values.keySet()) {
        Object value = values.get(key);
        if (value == null) {
          _logger.warn("(" + summary.getCallId()
              + "): null value for data point: " + key);
          continue;
        }
        HashMap<String, String> result = new HashMap<String, String>();
        results.add(result);
        populateEventFields(result, config);
        result.put("value", value.toString());
        result.put("dpId", key);
      }
      return results;
    }

    private Map<String, String> createError(Summary summary,
        ConfigAdapter config, Exception e) {
      String msg = "DataSource %1$s; Error calling mbean %2$s: Exception: %3$s";
      msg = String.format(msg, config.getDatasourceId(), summary
          .getObjectName(), e.getMessage());
      Map<String, String> error = createError(config, e);
      error.put(SUMMARY, msg);
      return error;
    }

    private Map<String, String> createTimeOutError(Summary summary,
        ConfigAdapter config) {
      String msg = "DataSource %1$s; Timed out %2$s on mbean %3$s ";
      msg = String.format(msg, config.getDatasourceId(), summary
          .getCallSummary(), summary.getObjectName());
      Map<String, String> error = createError(config, msg);
      return error;
    }


    private HashMap<String, String> createDeviceError(ConfigAdapter config, String msg) {
        HashMap<String, String> error = new HashMap<String, String>();

        populateEventFields(error, config, true);
        error.put(SUMMARY, msg);

        return error;
      }
    private HashMap<String, String> createError(ConfigAdapter config, String msg) {
      HashMap<String, String> error = new HashMap<String, String>();

      populateEventFields(error, config);
      error.put(SUMMARY, msg);

      return error;
    }

    private Map<String, String> createDeviceConnectionError(ConfigAdapter config,
                                                            String msg, Throwable e) {

      Utility.debugStack(e);

      String errorMsg = "%1$s; %2$s ";
      errorMsg = String.format(errorMsg, msg, e.getMessage());
      HashMap<String, String> error = createDeviceError(config, errorMsg);

      error.put(ConfigAdapter.EVENT_CLASS, "/Status/JMX/Connection");
      //Make sure the connection error has the connection key so that they dedup
      error.put(ConfigAdapter.EVENT_KEY, config.getConnectionKey());
      return error;
    }

    private Map<String, String> createUnexpectedError(ConfigAdapter config,
                                                      Throwable e) {
      Utility.debugStack(e);
      String errorMsg = "Unexpected Error; Exception %s ";
      errorMsg = String.format(errorMsg, e.getMessage());
      HashMap<String, String> error = createDeviceError(config, errorMsg);
      error.put(ConfigAdapter.EVENT_CLASS, "/Status/JMX");
      error.put(ConfigAdapter.EVENT_KEY, "unexpected_error");

      return error;
    }

    private Map<String, String> createError(ConfigAdapter config, Exception e) {
      String msg = "";
      if (e != null)
        Utility.debugStack(e);
        msg = e.getMessage();
      HashMap<String, String> error = createError(config, msg);
      return error;
    }

    private void populateEventFields(Map<String,String> evt,
            ConfigAdapter config){
        this.populateEventFields(evt, config, false);
    }

    private void populateEventFields(Map<String,String> evt,
            ConfigAdapter config, boolean deviceOnly)
        {
        evt.put(ConfigAdapter.DEVICE, config.getDevice());
        evt.put(ConfigAdapter.EVENT_CLASS, config.getEventClass());
        if (!deviceOnly){
            evt.put(ConfigAdapter.DATASOURCE_ID, config.getDatasourceId());
            String eventKey = config.getEventKey();
            if (eventKey == null || "".equals(eventKey.trim()))
                {
                //narrow down events to a datasource so that they can be cleared
                eventKey = config.getDatasourceId();
                }
            evt.put(ConfigAdapter.EVENT_KEY, eventKey);
            evt.put(ConfigAdapter.COMPONENT_KEY, config.getComponent());
            evt.put(ConfigAdapter.RRD_PATH, config.getRrdPath());
            }
        }
  }

}
