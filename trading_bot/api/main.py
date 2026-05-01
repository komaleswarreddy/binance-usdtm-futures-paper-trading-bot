"""
FastAPI backend: place testnet futures orders via JSON API.
Run from trading_bot: uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import requests
import uvicorn
from binance.error import ClientError, ServerError
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.schemas import (
    OrderErrorResponse,
    OrderRequest,
    OrderRequestSummary,
    OrderSuccessResponse,
)
from bot.client import DEFAULT_TESTNET_BASE_URL
from bot.logging_config import setup_logging
from bot.pipeline import execute_parsed_order, parse_order_inputs

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
LOG_FILE = BASE_DIR / "logs" / "api.log"

load_dotenv()
setup_logging(str(LOG_FILE), verbose=False)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Binance Futures Testnet Order API",
    description="USDT-M orders against https://testnet.binancefuture.com",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if (FRONTEND_DIR / "static").is_dir():
    app.mount(
        "/static",
        StaticFiles(directory=str(FRONTEND_DIR / "static")),
        name="static",
    )


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "testnet_base_url": DEFAULT_TESTNET_BASE_URL,
    }


@app.post("/api/orders", response_model=OrderSuccessResponse)
def create_order(body: OrderRequest):
    try:
        sym, side_v, ot, qty, price_v = parse_order_inputs(
            body.symbol,
            body.side,
            body.type,
            body.quantity,
            body.price,
        )
    except ValueError as e:
        logger.warning("Validation failed: %s", e)
        raise HTTPException(status_code=400, detail=str(e)) from e

    summary = OrderRequestSummary(
        symbol=sym,
        side=side_v,
        type=ot,
        quantity=qty,
        price=price_v,
    )
    logger.info(
        "API order submit symbol=%s side=%s type=%s qty=%s price=%s",
        sym,
        side_v,
        ot,
        qty,
        price_v,
    )

    try:
        resp = execute_parsed_order(sym, side_v, ot, qty, price_v, base_url=None)
    except ValueError as e:
        logger.error("Configuration error: %s", e)
        raise HTTPException(status_code=400, detail=str(e)) from e
    except ClientError as e:
        logger.exception("Binance client error")
        raise HTTPException(
            status_code=502,
            detail={
                "error": "binance_client_error",
                "message": e.error_message,
                "code": e.error_code,
                "http_status": e.status_code,
            },
        ) from e
    except ServerError as e:
        logger.exception("Binance server error")
        raise HTTPException(
            status_code=502,
            detail={
                "error": "binance_server_error",
                "message": e.message,
                "http_status": e.status_code,
            },
        ) from e
    except requests.RequestException as e:
        logger.exception("Network error")
        raise HTTPException(
            status_code=503,
            detail={"error": "network_error", "message": str(e)},
        ) from e

    logger.info("API order success: %s", json.dumps(resp, default=str))
    return OrderSuccessResponse(
        request=summary,
        response=resp,
    )


@app.get("/")
def serve_app():
    index = FRONTEND_DIR / "index.html"
    if not index.is_file():
        return {
            "message": "Frontend not found. Open /docs for API.",
            "api": "/api/orders",
        }
    return FileResponse(index)


def main():
    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
    )


if __name__ == "__main__":
    main()
