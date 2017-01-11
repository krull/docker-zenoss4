/*****************************************************************************
 * 
 * Copyright (C) Zenoss, Inc. 2008, all rights reserved.
 * 
 * This content is made available according to terms specified in
 * License.zenoss under the directory where your Zenoss product is installed.
 * 
 ****************************************************************************/


package com.zenoss.zenpacks.zenjmx;

import org.apache.commons.cli.CommandLine;
import org.apache.commons.cli.CommandLineParser;
import org.apache.commons.cli.Options;
import org.apache.commons.cli.ParseException;
import org.apache.commons.cli.PosixParser;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.log4j.Level;
import org.apache.log4j.Logger;
import org.apache.xmlrpc.webserver.XmlRpcServlet;
import org.eclipse.jetty.server.Connector;
import org.eclipse.jetty.server.Server;
import org.eclipse.jetty.server.bio.SocketConnector;
import org.eclipse.jetty.servlet.ServletHandler;
import org.eclipse.jetty.servlet.ServletHolder;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.HashMap;

public class ZenJmxMain {

    private static String ERROR = "40";
    private static String WARNING = "30";
    private static String INFO = "20";
    private static String DEBUG = "10";

    // logger
    private static final Log _logger = LogFactory.getLog(ZenJmxMain.class);

    /**
     * @param args
     */
    public static void main(String[] args) throws Exception
        {

        HashMap<String, Level> loggingLevel = new HashMap<String, Level>();
        loggingLevel.put(ERROR, Level.ERROR);
        loggingLevel.put(WARNING, Level.WARN);
        loggingLevel.put(INFO, Level.INFO);
        loggingLevel.put(DEBUG, Level.DEBUG);

        Configuration config = Configuration.instance();
        parseArguments(config, args);

        if ( config.propertyExists(OptionsFactory.LOG_SEVERITY) )
            {
            String levelOpt = config.getProperty(OptionsFactory.LOG_SEVERITY);
            Level level = loggingLevel.get(levelOpt);
            if ( level != null )
                {
                _logger.info("setting root logger to " + level);
                Logger.getRootLogger().setLevel(level);
                }
            else
                {
                _logger.warn("Ignoring unknown log severity " + levelOpt);
                }
            }

        String port = config.getProperty(OptionsFactory.LISTEN_PORT,
                OptionsFactory.DEFAULT_LISTENPORT);

        Server server = new Server();
        Connector connector = new SocketConnector();
        connector.setPort(Integer.parseInt(port));
        server.setConnectors(new Connector[] { connector });

        ServletHandler handler = new ServletHandler();

        ServletHolder holder = new ServletHolder(new XmlRpcServlet());
        handler.addServletWithMapping(holder, "/");
        // handler.start();
        handler.initialize();

        server.setHandler(handler);
        try
            {
            server.start();
            }
        catch (Exception e)
            {
            System.exit(10);
            }
        server.join();
        }

    /**
     * Parses the command line arguments
     */
    private static void parseArguments(Configuration config, String[] args)
            throws ParseException, NumberFormatException
        {

        OptionsFactory factory = OptionsFactory.instance();
        Options options = factory.createOptions();
        // parse the command line
        CommandLineParser parser = new PosixParser();
        CommandLine cmd = parser.parse(options, args);

        // get the config file argument and load it into the properties
        if ( cmd.hasOption(OptionsFactory.CONFIG_FILE) )
            {
            String filename = cmd.getOptionValue(OptionsFactory.CONFIG_FILE);
            try
                {
                config.load(new FileInputStream(filename));
                }
            catch (IOException e)
                {
                _logger.error("failed to load configuration file", e);
                }
            }
        else
            {
            _logger.warn("no config file option (--"
                    + OptionsFactory.CONFIG_FILE + ") specified");
            _logger.warn("only setting options based on command "
                    + "line arguments");
            }

        if ( _logger.isDebugEnabled() )
            {
            for (String arg : args)
                {
                _logger.debug("arg: " + arg);
                }
            }

        // interrogate the options and get the argument values
        overrideProperty(config, cmd, OptionsFactory.LISTEN_PORT);
        overrideProperty(config, cmd, OptionsFactory.LOG_SEVERITY);
        overrideOption(config, cmd, OptionsFactory.CONCURRENT_JMX_CALLS);
        // tell the user about the arguments
        _logger.info("zenjmxjava configuration:");
        _logger.info(config.toString());
        }

    /**
     * Checks the CommandLine for the property with the name provided. If
     * present it sets the name and value pair in the _config field.
     */
    private static void overrideProperty(Configuration config, CommandLine cmd,
            String name)
        {
        if ( cmd.hasOption(name) )
            {
            String value = cmd.getOptionValue(name);
            config.setProperty(name, value);
            }
        }

    /**
     * Checks the CommandLine for the option with the name provided. If present
     * it sets the name and value pair in the _config field using "true" as the
     * value of the option.
     */
    private static void overrideOption(Configuration config, CommandLine cmd,
            String option)
        {
        if ( cmd.hasOption(option) )
            {
            config.setProperty(option, "true");
            }
        }

}
