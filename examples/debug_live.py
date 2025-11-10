import logging
import traceback
import inspect
import casabourse as cb

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
# augmenter le niveau pour requests/urllib3
logging.getLogger("urllib3").setLevel(logging.DEBUG)
logging.getLogger("requests").setLevel(logging.DEBUG)

def info(obj, name=None):
    try:
        print(f"\n--- {name or getattr(obj,'__name__',str(obj))} ---")
        print("callable:", callable(obj))
        print("defined in:", inspect.getsourcefile(obj))
        try:
            src = inspect.getsource(obj)
            print("source preview:\n", "\n".join(src.splitlines()[:40]))
        except Exception as e:
            print("could not get source:", e)
    except Exception:
        pass

def try_call(fn, *args, **kwargs):
    try:
        print(f"\nCalling {fn.__name__}({', '.join([repr(a) for a in args])}{', ' if kwargs else ''}{', '.join(f'{k}={v!r}' for k,v in kwargs.items())})")
        res = fn(*args, **kwargs)
        print("-> returned type:", type(res))
        # si pandas DataFrame, affiche un aperçu sûr
        try:
            import pandas as pd
            if isinstance(res, pd.DataFrame):
                print("DataFrame shape:", res.shape)
                print(res.head(5).to_dict())
            else:
                print("repr:", repr(res)[:1000])
        except Exception:
            print("repr:", repr(res)[:1000])
        return res
    except Exception as e:
        print("Exception raised:")
        traceback.print_exc()

def main():
    print("package path:", getattr(cb, "__file__", getattr(cb, "__path__", None)))
    # inspect des fonctions
    for name in ("get_live_market_data", "get_live_market_data_auto", "get_build_id_cached"):
        if hasattr(cb, name):
            info(getattr(cb, name), name)
        else:
            print(f"{name} introuvable dans casabourse")

    # récupérer build id et tester appels
    bid = None
    if hasattr(cb, "get_build_id_cached"):
        try:
            bid = cb.get_build_id_cached()
            print("build_id:", bid)
        except Exception:
            print("erreur get_build_id_cached:")
            traceback.print_exc()

    # 1) appel get_live_market_data sans build_id
    if hasattr(cb, "get_live_market_data"):
        try_call(cb.get_live_market_data)
    # 2) appel get_live_market_data avec build_id (si obtenu)
    if bid and hasattr(cb, "get_live_market_data"):
        try_call(cb.get_live_market_data, build_id=bid)

    # 3) appel get_live_market_data_auto
    if hasattr(cb, "get_live_market_data_auto"):
        try_call(cb.get_live_market_data_auto)

if __name__ == "__main__":
    main()