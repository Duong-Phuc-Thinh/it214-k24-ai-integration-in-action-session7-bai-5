import time
import logging
import httpx
from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [GATEWAY FILTER] - %(levelname)s - %(message)s"
)
logger = logging.getLogger("ApiGateway")

app = FastAPI(title="API Gateway")

SERVICE_ROUTES = {
    "/api/customers": "http://127.0.0.1:8081",
    "/api/accounts": "http://127.0.0.1:8082",
    "/api/loans": "http://127.0.0.1:8083"
}

# Yêu cầu 4: Global Filter ghi log & thêm custom header X-Response-Time
@app.middleware("http")
async def logging_and_timing_filter(request: Request, call_next):
    start_time = time.perf_counter()
    method = request.method
    path = request.url.path

    logger.info(f"==> START: {method} {path}")

    response = await call_next(request)

    duration_ms = (time.perf_counter() - start_time) * 1000
    formatted_duration = f"{duration_ms:.2f}ms"

    # Thêm Header X-Response-Time vào response trả về client
    response.headers["X-Response-Time"] = formatted_duration

    logger.info(f"<== END: {method} {path} | Status: {response.status_code} | Execution Time: {formatted_duration}")
    return response

# Proxy định tuyến request tới các microservice đích
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway_proxy(request: Request, path: str):
    full_path = f"/{path}"
    target_host = None

    for route_prefix, host in SERVICE_ROUTES.items():
        if full_path.startswith(route_prefix):
            target_host = host
            break

    if not target_host:
        return JSONResponse(status_code=404, content={"detail": f"Route '{full_path}' not mapped in Gateway"})

    target_url = f"{target_host}{full_path}"
    if request.url.query:
        target_url += f"?{request.url.query}"

    body = await request.body()
    headers = dict(request.headers)
    headers.pop("host", None)

    async with httpx.AsyncClient() as client:
        try:
            proxy_res = await client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body,
                timeout=10.0
            )
            # Loại bỏ Content-Length để tránh xung đột định dạng
            resp_headers = dict(proxy_res.headers)
            resp_headers.pop("content-length", None)

            return Response(
                content=proxy_res.content,
                status_code=proxy_res.status_code,
                headers=resp_headers
            )
        except httpx.RequestError as exc:
            return JSONResponse(status_code=503, content={"detail": f"Service unavailable: {str(exc)}"})
