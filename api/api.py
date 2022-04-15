from .routings import app

def api_startup(port=80, host='0.0.0.0', debug=False, use_reloader=False):
    print(f"Starting up HTTP server on post {port}")
    app.run(port=port, host=host, debug=debug, use_reloader=use_reloader)