from webui import WebUI

from crm import create_app

app = create_app()
crm_UI = WebUI(app, debug=True)
crm_UI.run()

