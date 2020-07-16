import asyncio
from app import app
from app import config_service


# TODO: RUN ON LAMBDA CRON JOB
# TODO: NEED LAMBDA LOGGING
def run_bot() -> None:
    r = config_service.connect_to_reddit()
    asyncio.run(app.update_subscriptions(r))
    return None
