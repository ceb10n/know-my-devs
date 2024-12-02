import logging

from knowmydevs.core.config import app_config

logging.basicConfig()
logging.getLogger("urllib3").setLevel(logging.ERROR)
logging.getLogger("knowmydevs").setLevel(app_config.log_level)


logger = logging.getLogger("knowmydevs")

