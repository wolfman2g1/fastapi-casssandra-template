from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
import uvicorn
import logging
import logging.config
from service.logging_config import LOGGING_CONFIG
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry import trace
from service.settings import config
from service.api import ping



#Log setup
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

# tracing


LOCAL = False #<--------set to True to print to console instead

resource = Resource(attributes={
    SERVICE_NAME: f"{config.SERVICE_NAME}"
})

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(
    ConsoleSpanExporter()
    if LOCAL else
    OTLPSpanExporter(
        f'{config.OTLP_EXPORTER}',
        #NOTE: add org header id if tempo not multi-tenant ("X-Scope-OrgID": "61d8aa985c38ac8a3e7ebab5")
    )
)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)
def configure_app():
    logger.info("Using Config %s", config.ENV)
    app = FastAPI(docs_url="/api/v1/docs")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.include_router(ping.router)
    
    

    return app


if __name__ == "__main__":
    logger.info(f"Starting {config.SERVICE_NAME}")
    app = configure_app()
    uvicorn.run(app, host="0.0.0.0", port=5001)