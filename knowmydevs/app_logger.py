import logging

from knowmydevs.core.config import app_config

logging.basicConfig()
logging.getLogger().setLevel(app_config.log_level)

logger = logging.getLogger("knowmydevs")

