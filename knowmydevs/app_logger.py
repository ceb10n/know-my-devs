import logging

from knowmydevs.core.config import app_config

logging.basicConfig()
logging.getLogger().setLevel(app_config.log_level)
logging.getLogger("urllib3").setLevel(logging.ERROR)

logger = logging.getLogger("knowmydevs")

