from twisted.python import log
from twisted.web._newclient import Request, HTTP11ClientProtocol, BadHeaders, ResponseFailed, \
                                   RequestNotSent, TransportProxyProducer, HTTPClientParser, RequestGenerationFailed
from twisted.web.client import Agent, _parse
from twisted.python.failure import Failure
from twisted.web.http_headers import Headers
from twisted.internet.defer import Deferred, succeed, fail, maybeDeferred, DeferredSemaphore
from twisted.internet.error import ConnectionDone

try:
    from twisted.internet.ssl import ClientContextFactory
except ImportError:
    class WebClientContextFactory(object):
        """
        A web context factory which doesn't work because the necessary SSL
        support is missing.
        """
        def getContext(self, hostname, port):
            raise NotImplementedError("SSL support unavailable")
else:
    class WebClientContextFactory(ClientContextFactory):
        """
        A web context factory which ignores the hostname and port and does no
        certificate verification.
        """
        def getContext(self, hostname, port):
            return ClientContextFactory.getContext(self)
            
class ZenRequest(Request):
    def __init__(self, method, uri, headers, bodyProducer, persistent=False):
        self.method = method
        self.uri = uri
        self.headers = headers
        self.bodyProducer = bodyProducer
        self.persistent = persistent
        
    def _writeHeaders(self, transport, TEorCL):
        hosts = self.headers.getRawHeaders('host', ())
        if len(hosts) != 1:
            raise BadHeaders("Exactly one Host header required")
        # In the future, having the protocol version be a parameter to this
        # method would probably be good.  It would be nice if this method
        # weren't limited to issueing HTTP/1.1 requests.
        requestLines = []
        requestLines.append(
            '%s %s HTTP/1.1\r\n' % (self.method, self.uri))
        if self.persistent:
            requestLines.append('Connection: Keep-Alive\r\n')
        else:
            requestLines.append('Connection: close\r\n')
        if TEorCL is not None:
            requestLines.append(TEorCL)
        for name, values in self.headers.getAllRawHeaders():
            requestLines.extend(['%s: %s\r\n' % (name, v) for v in values])
        requestLines.append('\r\n')
        transport.writeSequence(requestLines)

        
class ZenHTTP11ClientProtocol(HTTP11ClientProtocol):
	
    @property
    def state(self):
        return self._state
	
    def request(self, request):
        """
        Issue C{request} over C{self.transport} and return a L{Deferred} which
        will fire with a L{Response} instance or an error.
        @param request: The object defining the parameters of the request to
           issue.
        @type request: L{Request}
        @rtype: L{Deferred}
        @return: The deferred may errback with L{RequestGenerationFailed} if
            the request was not fully written to the transport due to a local
            error.  It may errback with L{RequestTransmissionFailed} if it was
            not fully written to the transport due to a network error.  It may
            errback with L{ResponseFailed} if the request was sent (not
            necessarily received) but some or all of the response was lost.  It
            may errback with L{RequestNotSent} if it is not possible to send
            any more requests using this L{HTTP11ClientProtocol}.
        """
        if self._state != 'QUIESCENT':
            return fail(RequestNotSent())
        self._state = 'TRANSMITTING'
        _requestDeferred = maybeDeferred(request.writeTo, self.transport)
        self._finishedRequest = Deferred()
        # Keep track of the Request object in case we need to call stopWriting
        # on it.
        self._currentRequest = request
        self._transportProxy = TransportProxyProducer(self.transport)
        self._parser = HTTPClientParser(request, self._finishResponse)
        self._parser.makeConnection(self._transportProxy)
        self._responseDeferred = self._parser._responseDeferred
        def cbRequestWrotten(ignored):
            if self._state == 'TRANSMITTING':
                self._state = 'WAITING'
                self._responseDeferred.chainDeferred(self._finishedRequest)
        def ebRequestWriting(err):
            if self._state == 'TRANSMITTING':
                self._state = 'GENERATION_FAILED'
                self.transport.loseConnection()
                self._finishedRequest.errback(
                    Failure(RequestGenerationFailed([err])))
            else:
                log.err(err, "foo")
        _requestDeferred.addCallbacks(cbRequestWrotten, ebRequestWriting)
        return self._finishedRequest
        
    def _finishResponse(self, rest):
        """
        Called by an L{HTTPClientParser} to indicate that it has parsed a
        complete response.

        @param rest: A C{str} giving any trailing bytes which were given to
            the L{HTTPClientParser} which were not part of the response it
            was parsing.
        """
        assert self._state in ('WAITING', 'TRANSMITTING')

        if self._state == 'WAITING':
            self._state = 'QUIESCENT'
        else:
            # The server sent the entire response before we could send the
            # whole request.  That sucks.  Oh well.  Fire the request()
            # Deferred with the response.  But first, make sure that if the
            # request does ever finish being written that it won't try to fire
            # that Deferred.
            self._state = 'TRANSMITTING_AFTER_RECEIVING_RESPONSE'
            self._responseDeferred.chainDeferred(self._finishedRequest)

        reason = ConnectionDone("synthetic!")
        connHeaders = self._parser.connHeaders.getRawHeaders('connection')
        if (connHeaders is not None) and ('close' in connHeaders):
            self._giveUp(Failure(reason))
        else:
            # It's persistent connection
            self._disconnectParser(reason)        
	
class ZenAgent(Agent):
    """
    L{Agent} is a very basic HTTP client.  It supports I{HTTP} and I{HTTPS}
    scheme URIs (but performs no certificate checking by default).  It also
    supports persistent connections.
    @ivar _reactor: The L{IReactorTCP} and L{IReactorSSL} implementation which
        will be used to set up connections over which to issue requests.
    @ivar _contextFactory: A web context factory which will be used to create
        SSL context objects for any SSL connections the agent needs to make.
    @since: 9.0
    @ivar persistent: Set to C{True} when you use HTTP persistent connecton.
    @type persistent: C{bool} 

    @ivar maxConnectionsPerHostName: Max number of HTTP connections per a server.  The
        default value is 1.  This is effective only when the
        C{self.persistent} is C{True}.
        RFC 2616 says "A single-user client SHOULD NOT maintain more than 2
        connections with any server or proxy."
    @type maxConnectionsPerHostName: C{int}

    @ivar _semaphores: A dictioinary mapping a tuple (scheme, host, port)
        to an instance of L{DeferredSemaphore}.  It is used to limit the
        number of connections to a server when C{self.persistent==True}.

    @ivar _protocolCache: A dictioinary mapping a tuple (scheme, host, port)
        to a list of instances of L{HTTP11ClientProtocol}.  It is used to
        cache the connections to the servers when C{self.persistent==True}.

    """
    _protocol = ZenHTTP11ClientProtocol
    maxConnectionsPerHostName = 2
 
    def __init__(self, reactor, contextFactory=WebClientContextFactory(),
                 persistent=False, maxConnectionsPerHostName=2):
        self._reactor = reactor
        self._contextFactory = contextFactory
        self.persistent = persistent
        self.maxConnectionsPerHostName = maxConnectionsPerHostName
        self._semaphores = {}
        self._protocolCache = {}
        
    def request(self, method, uri, headers=None, bodyProducer=None):
        """
        Issue a new request.
        @param method: The request method to send.
        @type method: C{str}
        @param uri: The request URI send.
        @type uri: C{str}
        @param scheme: A string like C{'http'} or C{'https'} (the only two
            supported values) to use to determine how to establish the
            connection.
 
        @param host: A C{str} giving the hostname which will be connected to in
            order to issue a request.

        @param port: An C{int} giving the port number the connection will be on.

        @param path: A C{str} giving the path portion of the request URL.
        @param headers: The request headers to send.  If no I{Host} header is
            included, one will be added based on the request URI.
        @type headers: L{Headers}
        @param bodyProducer: An object which will produce the request body or,
            if the request body is to be empty, L{None}.
        @type bodyProducer: L{IBodyProducer} provider
        @return: A L{Deferred} which fires with the result of the request (a
            L{Response} instance), or fails if there is a problem setting up a
            connection over which to issue the request.  It may also fail with
            L{SchemeNotSupported} if the scheme of the given URI is not
            supported.
        @rtype: L{Deferred}
        """
        scheme, host, port, path = _parse(uri)
        if headers is None:
            headers = Headers()
        if not headers.hasHeader('host'):
            # This is a lot of copying.  It might be nice if there were a bit
            # less.
            headers = Headers(dict(headers.getAllRawHeaders()))
            headers.addRawHeader(
                'host', self._computeHostValue(scheme, host, port))
        if self.persistent:
            sem = self._semaphores.get((scheme, host, port))
            if sem is None:
                sem = DeferredSemaphore(self.maxConnectionsPerHostName)
                self._semaphores[scheme, host, port] = sem
            return sem.run(self._request, method, scheme, host, port, path,
                           headers, bodyProducer)
        else:
            return self._request(
                method, scheme, host, port, path, headers, bodyProducer)

    def _request(self, method, scheme, host, port, path, headers, bodyProducer):
        """
        Issue a new request.
        @param method: The request method to send.
        @type method: C{str}
        @param uri: The request URI send.
        @type uri: C{str}
        @param headers: The request headers to send.  If no I{Host} header is
            included, one will be added based on the request URI.
        @type headers: L{Headers}
        @param bodyProducer: An object which will produce the request body or,
            if the request body is to be empty, L{None}.
        @type bodyProducer: L{IBodyProducer} provider
        @return: A L{Deferred} which fires with the result of the request (a
            L{Response} instance), or fails if there is a problem setting up a
            connection over which to issue the request.  It may also fail with
            L{SchemeNotSupported} if the scheme of the given URI is not
            supported.
        @rtype: L{Deferred}
        """
        protos = self._protocolCache.setdefault((scheme, host, port), [])
        maybeDisconnected = False
        #while protos:
        #    # connection exists
        #    p = protos.pop(0)
        d = None
        for p in protos:
            if p.state == 'QUIESCENT':
                # available existing connection
                d = succeed(p)
                maybeDisconnected = True
                break
        if not d:
            # new connection
            d = self._connect(scheme, host, port)
        
        req = ZenRequest(method, path, headers, bodyProducer,
                          persistent=self.persistent)
        
        def saveProtocol(response, proto):
            if self.persistent and proto not in protos:
                protos.append(proto)
            return response

        def cbConnected(proto):
            def ebRequest(f):
                # Previous connection is unavailable.
                if f.check(ResponseFailed):
                    for reason in f.value.reasons:
                        if (isinstance(reason, Failure) and
                            isinstance(reason.value, ConnectionDone)):
                            # Maybe timeout has been exeeded before I send
                            # the request. So I retry again.
                            def retry(proto):
                                d = proto.request(req)
                                d.addCallback(saveProtocol, proto)
                                return d
                            d = self._connect(scheme, host, port)
                            d.addCallback(retry)
                            return d
                return f
            d = proto.request(req)
            d.addCallback(saveProtocol, proto)
            if maybeDisconnected:
                d.addErrback(ebRequest)
            return d

        d.addCallback(cbConnected)
        return d

    def closeCachedConnections(self):
        """
        Close all the cached persistent connections.
        """
        for protos in self._protocolCache.itervalues():
            for p in protos:
                p.transport.loseConnection()
        self._protocolCache = {}
