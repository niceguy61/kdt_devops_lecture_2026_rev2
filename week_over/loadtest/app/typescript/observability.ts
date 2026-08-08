
import { Request, Response, NextFunction } from 'express';
export function observability(opts:{serviceName:string}){
  return (req:Request, res:Response, next:NextFunction)=>{
    const traceId = (req.headers['x-trace-id'] as string) || `trc_${Math.random().toString(36).slice(2,8)}`;
    const start = Date.now();
    (req as any).errorCode = null;
    res.setHeader('X-Trace-Id', traceId);
    res.on('finish', ()=>{
      const log = {
        service: opts.serviceName,
        traceId,
        method: req.method,
        path: req.path,
        status: res.statusCode,
        latency: Date.now()-start,
        errorCode: (req as any).errorCode || null,
        ip: req.ip
      };
      console.log(JSON.stringify(log));
    });
    next();
  }
}
