
// 공통 라이브러리 형태
@Component
public class ObservabilityFilter extends OncePerRequestFilter {
    @Value("${service.name:unknown}") String serviceName;
    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res, FilterChain chain) throws Exception {
        String traceId = Optional.ofNullable(req.getHeader("X-Trace-Id")).orElse("trc_"+UUID.randomUUID().toString().substring(0,8));
        MDC.put("traceId", traceId);
        long start = System.currentTimeMillis();
        try {
            chain.doFilter(req,res);
        } finally {
            long latency = System.currentTimeMillis()-start;
            String errorCode = (String) req.getAttribute("errorCode");
            log.info("service={}, traceId={}, status={}, latency={}, errorCode={}", serviceName, traceId, res.getStatus(), latency, errorCode);
            MDC.clear();
        }
    }
}
// 팀 사용: request.setAttribute("errorCode","E002");
