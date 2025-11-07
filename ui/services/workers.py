import threading

def run_async(fn, on_success=None, on_error=None):
    def _t():
        try:
            res = fn()
            if on_success: on_success(res)
        except Exception as e:
            if on_error: on_error(e)
    threading.Thread(target=_t, daemon=True).start()