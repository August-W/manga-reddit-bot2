import asyncio
from app import app
from app import config_service


# TODO: RUN ON LAMBDA CRON JOB
# TODO: NEED LAMBDA LOGGING
def run_bot() -> None:
    r, conf = config_service.connect_to_reddit()
    app.update_subscriptions(r, conf)
    return None

# THIS IS JUST FOR LOCAL TESTING
run_bot()