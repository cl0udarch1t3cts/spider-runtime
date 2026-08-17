from spider_executor.api import create_app
from spider_executor.runtime import create_control
from spider_executor.settings import Settings

settings = Settings()
control = create_control(settings)
app = create_app(control)
