import pprint
from datetime import datetime
import casabourse as cb

pp = pprint.PrettyPrinter(indent=2).pprint

def safe_print_df_head(df, name, n=5):
    if df is None:
        print(f"{name}: no data")
    else:
        print(f"{name}: {len(df)} rows — head:")
        try:
            print(df.head(n).to_dict())
        except Exception:
            print(df.head(n))

def main():
    print("build_id (cached):", cb.get_build_id_cached())

    # Live market
    df_live = cb.get_live_market_data()
    safe_print_df_head(df_live, "live_market")

    # Live market (auto)
    df_live_auto = cb.get_live_market_data_auto()
    safe_print_df_head(df_live_auto, "live_market_auto")

    # Historical for a ticker
    # OK
    hist = cb.get_historical_data_auto("IAM", "2024-01-01", "2024-12-31")
    safe_print_df_head(hist, "historical_IAM", 3)

    # Symbol id lookups
    sid_afm = cb.get_symbol_id_from_ticker_auto("AFM")
    print("symbol id AFM:", sid_afm)

    multi = cb.get_multiple_symbol_ids(["AFM", "IAM", "ATW"])
    print("multiple symbol ids:", multi)

    # Market analytics
    print("\nTop gainers (5):")
    pp(cb.get_top_gainers(5).to_dict() if cb.get_top_gainers(5) is not None else "no data")

    print("\nTop losers (5):")
    pp(cb.get_top_losers(5).to_dict() if cb.get_top_losers(5) is not None else "no data")

    print("\nMost active (by volume):")
    pp(cb.get_most_active(5, by='volume').to_dict() if cb.get_most_active(5, by='volume') is not None else "no data")

    print("\nSector performance:")
    pp(cb.get_sector_performance().to_dict() if cb.get_sector_performance() is not None else "no data")

    print("\nMarket summary:")
    pp(cb.get_market_summary() if cb.get_market_summary() is not None else "no data")

    # Export example (writes a file)
    print("\nExport market data -> example CSV")
    try:
        fname = cb.export_market_data(format='csv')
        print("exported:", fname)
    except Exception as e:
        print("export failed:", e)

    # Volume overview (session)
    try:
        df_global, df_top, df_central, df_blocs, df_autres = cb.get_volume_overview()
        safe_print_df_head(df_global, "volume_global")
        safe_print_df_head(df_top, "volume_top")
    except Exception as e:
        print("volume_overview error:", e)

    # Volume data range
    df_vol = cb.get_volume_data("2024-01-01", datetime.now().strftime("%Y-%m-%d"))
    safe_print_df_head(df_vol, "volume_data")

    # Capitalization overview
    cap = cb.get_capitalization_overview()
    if cap:
        print("\nCapitalisation global head:")
        safe_print_df_head(cap.get('global_cap'), "capital_global")

    # Indices
    indices_all = cb.get_all_indices_overview()
    print("\nIndices categories count:", 0 if indices_all is None else len(indices_all))

    df_indices = cb.get_indices_list_with_capitalization()
    safe_print_df_head(df_indices, "indices_with_cap")

    available = cb.get_available_indices_for_composition()
    safe_print_df_head(available, "available_indices_for_composition")

    main_indices = cb.get_main_indices()
    safe_print_df_head(main_indices, "main_indices")

    # Index composition and quotation
    comp_msi20 = cb.get_index_composition("MSI20")
    safe_print_df_head(comp_msi20, "MSI20_composition")

    batch = cb.get_index_composition_batch(["MSI20", "MASI"])
    print("batch keys:", list(batch.keys()) if isinstance(batch, dict) else batch)

    q = cb.get_index_quotation("MSI20")
    safe_print_df_head(q, "index_quotation_MSI20")

    # Index historical data (example)
    df_idx = cb.get_index_data_by_name("MASI 20", datetime.now().strftime("%Y-%m-%d"), periode='1H')
    safe_print_df_head(df_idx, "index_data_MASI20_1H")

if __name__ == "__main__":
    main()
