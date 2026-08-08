@Component
public class LoggingFilter extends OncePerRequestFilter {
    private static final Logger log = LoggerFactory.getLogger(LoggingFilter.class);

    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res, FilterChain chain) throws IOException, ServletException {
        String traceId = Optional.ofNullable(req.getHeader("X-Trace-Id")).orElse("trc_"+UUID.randomUUID().toString().substring(0,8));
        long start = System.currentTimeMillis();
        try {
            chain.doFilter(req, res);
        } finally {
            long latency = System.currentTimeMillis() - start;
            // JSON 로그 10필드 + errorCode
            log.info("{\"service\":\"order-api\",\"traceId\":\"%s\",\"method\":\"%s\",\"path\":\"%s\",\"status\":%d,\"latency\":%d,\"errorCode\":null}".formatted(traceId, req.getMethod(), req.getRequestURI(), res.getStatus(), latency));
            res.setHeader("X-Trace-Id", traceId);
        }
    }
}
// logback-spring.xml에서 <appender class="net.logstash.logback.appender.LogstashTcpSocketAppender"> 로 Loki 전송