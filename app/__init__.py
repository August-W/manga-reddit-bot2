from app import app, config_service


def run_bot() -> None:
    print("***** JOB STARTING *****")
    r, conf = config_service.connect_to_reddit()
    app.update_subscriptions(r, conf)
    return None
