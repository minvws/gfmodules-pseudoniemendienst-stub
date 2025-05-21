from app.config import (
    Config,
    ConfigApp,
    ConfigDatabase,
    ConfigStats,
    ConfigTelemetry,
    ConfigUraMiddleware,
    ConfigUvicorn,
    LogLevel,
)


def get_test_config() -> Config:
    return Config(
        app=ConfigApp(
            loglevel=LogLevel.error,
        ),
        database=ConfigDatabase(
            dsn="sqlite:///:memory:",
            create_tables=True,
        ),
        uvicorn=ConfigUvicorn(
            swagger_enabled=False,
            docs_url="/docs",
            redoc_url="/redoc",
            host="0.0.0.0",
            port=8503,
            reload=True,
            use_ssl=False,
            ssl_base_dir=None,
            ssl_cert_file=None,
            ssl_key_file=None,
        ),
        telemetry=ConfigTelemetry(
            enabled=False,
            endpoint=None,
            service_name=None,
            tracer_name=None,
        ),
        stats=ConfigStats(enabled=False, host=None, port=None, module_name=None),
        ura_middleware=ConfigUraMiddleware(
            override_authentication_ura=None,
            use_authentication_ura_allowlist=False,
            allowlist_cache_in_seconds=40,
        ),
    )
