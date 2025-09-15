import CFTC_positioning as cot
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from scipy.stats import percentileofscore

# ----------------------------
# Asset and participant mappings
# ----------------------------

MARKETS_COMMODITIES = {
    "SOYBEANS": ["SOYBEANS - CHICAGO BOARD OF TRADE"],
    "SOYBEAN OIL": ["SOYBEAN OIL - CHICAGO BOARD OF TRADE"],
    "SOYBEAN MEAL": ["SOYBEAN MEAL - CHICAGO BOARD OF TRADE"],
    "CANOLA": ["CANOLA - ICE FUTURES U.S."],
    "GOLD": ["GOLD - COMMODITY EXCHANGE INC."],
    "SILVER": ["SILVER - COMMODITY EXCHANGE INC."],
    "PLATINUM": ["PLATINUM - NEW YORK MERCANTILE EXCHANGE"],
    "COPPER": ["COPPER- #1 - COMMODITY EXCHANGE INC."],
    "COBALT": ["COBALT - COMMODITY EXCHANGE INC."],
    "CORN": ["CORN - CHICAGO BOARD OF TRADE"],
    "CUTTON": ["COTTON - ICE FUTURES U.S."],
    "SUGAR": ["SUGAR NO. 11 - ICE FUTURES U.S."],
    "COFFEE C": ["COFFEE C - ICE FUTURES U.S."],
    "COCOA": ["COCOA - ICE FUTURES U.S."],
    "WHEAT-SRW": ["WHEAT-SRW - CHICAGO BOARD OF TRADE"],
    "WHEAT-HRW": ["WHEAT-HRW - CHICAGO BOARD OF TRADE"],
    'USGC HSFO (PLATTS)': ['USGC HSFO (PLATTS) - ICE FUTURES ENERGY DIV '],
    'FUEL OIL-3% USGC/3.5': ['FUEL OIL-3% USGC/3.5% FOB RDAM - ICE FUTURES ENERGY DIV'],
    'USGC HSFO-PLATTS/BRENT 1ST LN': ['USGC HSFO-PLATTS/BRENT 1ST LN  - ICE FUTURES ENERGY DIV'],
    'NY HARBOR ULSD': ['NY HARBOR ULSD - NEW YORK MERCANTILE EXCHANGE'],
    'UP DOWN GC ULSD VS HO SPR': ['UP DOWN GC ULSD VS HO SPR - NEW YORK MERCANTILE EXCHANGE'],
    'ETHANOL T2 FOB INCL DUTY': ['ETHANOL T2 FOB INCL DUTY - NEW YORK MERCANTILE EXCHANGE'],
    'ETHANOL': ['ETHANOL - NEW YORK MERCANTILE EXCHANGE'],
    'CRUDE DIFF-WCS HOUSTON/WTI 1ST': ['CRUDE DIFF-WCS HOUSTON/WTI 1ST - ICE FUTURES ENERGY DIV'],
    'CRUDE OIL, LIGHT SWEET-WTI': ['CRUDE OIL, LIGHT SWEET-WTI - ICE FUTURES EUROPE'],
    'CRUDE DIFF-TMX WCS 1A INDEX': ['CRUDE DIFF-TMX WCS 1A INDEX - ICE FUTURES ENERGY DIV'],
    'CRUDE DIFF-TMX SW 1A INDEX': ['CRUDE DIFF-TMX SW 1A INDEX - ICE FUTURES ENERGY DIV'],
    'CONDENSATE DIF-TMX C5 1A INDEX': ['CONDENSATE DIF-TMX C5 1A INDEX - ICE FUTURES ENERGY DIV'],
    'WTI-PHYSICAL': ['WTI-PHYSICAL - NEW YORK MERCANTILE EXCHANGE'],
    'WTI FINANCIAL CRUDE OIL': ['WTI FINANCIAL CRUDE OIL - NEW YORK MERCANTILE EXCHANGE'],
    'BRENT LAST DAY': ['BRENT LAST DAY - NEW YORK MERCANTILE EXCHANGE'],
    'WTI  HOUSTON ARGUS/WTI TR MO': ['WTI  HOUSTON ARGUS/WTI TR MO - NEW YORK MERCANTILE EXCHANGE'],
    'WTI MIDLAND ARGUS VS WTI TRADE': ['WTI MIDLAND ARGUS VS WTI TRADE - NEW YORK MERCANTILE EXCHANGE'],
    'GASOLINE RBOB': ['GASOLINE RBOB - NEW YORK MERCANTILE EXCHANGE'],
    'GULF COAST CBOB GAS A2 PL RBOB': ['GULF COAST CBOB GAS A2 PL RBOB - NEW YORK MERCANTILE EXCHANGE'],
    'GULF JET NY HEAT OIL SPR': ['GULF JET NY HEAT OIL SPR - NEW YORK MERCANTILE EXCHANGE'],
    'MARINE .5% FOB USGC/BRENT 1st': ['MARINE .5% FOB USGC/BRENT 1st - ICE FUTURES ENERGY DIV'],
    'GULF # 6 FUEL OIL CRACK': ['GULF # 6 FUEL OIL CRACK - NEW YORK MERCANTILE EXCHANGE']
}  

MARKETS_FX = {
    "EURO FX": ["EURO FX - CHICAGO MERCANTILE EXCHANGE"],
    "JAPANESE YEN": ["JAPANESE YEN - CHICAGO MERCANTILE EXCHANGE"],
    "BRITISH POUND STERLING": ["BRITISH POUND - CHICAGO MERCANTILE EXCHANGE"],
    "SWISS FRANC": ["SWISS FRANC - CHICAGO MERCANTILE EXCHANGE"],
    "CANADIAN DOLLAR": ["CANADIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE"],
    "AUSTRALIAN DOLLAR": ["AUSTRALIAN DOLLAR - CHICAGO MERCANTILE EXCHANGE"],
    "MEXICAN PESO": ["MEXICAN PESO - CHICAGO MERCANTILE EXCHANGE"],
    "NEW ZEALAND DOLLAR": ["NZ DOLLAR - CHICAGO MERCANTILE EXCHANGE"],
    'SOUTH AFRICAN RAND': ['SO AFRICAN RAND - CHICAGO MERCANTILE EXCHANGE'],
    "US DOLLAR INDEX": jp3 ["USD INDEX - ICE FUTURES U.S."]
} 

MARKETS_RATE = {
    "SOFR-1M": ["SOFR-1M - CHICAGO MERCANTILE EXCHANGE"],
    "SOFR-3M": ["SOFR-3M - CHICAGO MERCANTILE EXCHANGE"],
    "EURO SHORT TERM RATE": ["EURO SHORT TERM RATE - CHICAGO MERCANTILE EXCHANGE"],
    "ULTRA UST BOND": ["ULTRA UST BOND - CHICAGO BOARD OF TRADE"],
    "UST BOND": ["UST BOND - CHICAGO BOARD OF TRADE"],
    "UST 2Y NOTE": ["UST 2Y NOTE - CHICAGO BOARD OF TRADE"],
    "UST 5Y NOTE": ["UST 5Y NOTE - CHICAGO BOARD OF TRADE"],
    "UST 10Y NOTE": ["UST 10Y NOTE - CHICAGO BOARD OF TRADE"],
    "ULTRA UST 10Y": ["ULTRA UST 10Y - CHICAGO BOARD OF TRADE"],
    "MICRO 10 YEAR YIELD": ["MICRO 10 YEAR YIELD - CHICAGO BOARD OF TRADE"],
    "FED FUNDS": ["FED FUNDS - CHICAGO BOARD OF TRADE"]
} 

MARKETS_CRYPTO = {
    'BTC': ['BITCOIN - CHICAGO MERCANTILE EXCHANGE'],
    'MICRO BTC': ['MICRO BITCOIN - CHICAGO MERCANTILE EXCHANGE '],
    'ETH': ['ETHER CASH SETTLED - CHICAGO MERCANTILE EXCHANGE'],
    'XRP': ['XRP - CHICAGO MERCANTILE EXCHANGE '],
    'SOL': ['SOL - CHICAGO MERCANTILE EXCHANGE'],
    'DOGECOIN': ['DOGECOIN - COINBASE DERIVATIVES, LLC'],
    'CHAINLINK': ['CHAINLINK - COINBASE DERIVATIVES, LLC '],
    'AVAX': ['AVALANCHE - COINBASE DERIVATIVES, LLC']
}  

MARKETS_INDICES = {
    'VIX FUTURES': ['VIX FUTURES - CBOE FUTURES EXCHANGE'],
    'S&P 500 Consolidated': ['S&P 500 Consolidated - CHICAGO MERCANTILE EXCHANGE'],
    'MICRO E-MINI S&P 500 INDEX': ['MICRO E-MINI S&P 500 INDEX - CHICAGO MERCANTILE EXCHANGE'],
    'NASDAQ MINI': ['NASDAQ MINI - CHICAGO MERCANTILE EXCHANGE'],
    'E-MINI S&P 500': ['E-MINI S&P 500 - CHICAGO MERCANTILE EXCHANGE'],
    'MSCI EAFE': ['MSCI EAFE  - ICE FUTURES U.S.'],
    'MSCI EM INDEX': ['MSCI EM INDEX - ICE FUTURES U.S.'],
    'NIKKEI STOCK AVERAGE YEN DENOM': ['NIKKEI STOCK AVERAGE YEN DENOM - CHICAGO MERCANTILE EXCHANGE'],
    'BBG COMMODITY INDEX': ['BBG COMMODITY - CHICAGO BOARD OF TRADE']
}  

PARTICIPANTS_FIN = {
    "Dealers": ("Dealer_Positions_Long_All", "Dealer_Positions_Short_All"),
    "AM/FI": ("Asset_Mgr_Positions_Long_All", "Asset_Mgr_Positions_Short_All"),
    "Lev Funds": ("Lev_Money_Positions_Long_All", "Lev_Money_Positions_Short_All"),
    "Non-Rept": ("NonRept_Positions_Long_All", "NonRept_Positions_Short_All")
}

PARTICIPANTS_COM = {
    "Commercials (Prod/Merc/Proc)": ("Prod_Merc_Positions_Long_All", "Prod_Merc_Positions_Short_All"),
    "Managed Money": ("M_Money_Positions_Long_All", "M_Money_Positions_Short_All"),
    "Swap Dealers": ("Swap_Dealer_Positions_Long_All", "Swap_Dealer_Positions_Short_All"),
    "Other Rept": ("Other_Rept_Positions_Long_All", "Other_Rept_Positions_Short_All"),
    "Non-Rept": ("NonRept_Positions_Long_All", "NonRept_Positions_Short_All")
}

PARTICIPANTS_FIN_OI = {
    "Dealers": ("Pct_of_OI_Dealer_Long_All", "Pct_of_OI_Dealer_Short_All"),
    "AM/FI": ("Pct_of_OI_Asset_Mgr_Long_All", "Pct_of_OI_Asset_Mgr_Short_All"),
    "Lev Funds": ("Pct_of_OI_Lev_Money_Long_All", "Pct_of_OI_Lev_Money_Short_All"),
    "Non-Rept": ("Pct_of_OI_NonRept_Long_All", "Pct_of_OI_NonRept_Short_All")
}

PARTICIPANTS_COM_OI = {
    "Commercials (Prod/Merc/Proc)": ("Pct_of_OI_Prod_Merc_Long_All", "Pct_of_OI_Prod_Merc_Short_All"),
    "Managed Money": ("Pct_of_OI_M_Money_Long_All", "Pct_of_OI_M_Money_Short_All"),
    "Swap Dealers": ("Pct_of_OI_Swap_Dealer_Long_All", "Pct_of_OI_Swap_Dealer_Short_All"),
    "Other Rept": ("Pct_of_OI_Other_Rept_Long_All", "Pct_of_OI_Other_Rept_Short_All"),
    "Non-Rept": ("Pct_of_OI_NonRept_Long_All", "Pct_of_OI_NonRept_Short_All")
}

# Function to get actual column names from the DataFrame
def get_available_columns(df, participant_type="financial"):
    """
    Dynamically identify available columns in the DataFrame
    """
    columns = df.columns.tolist()
    
    if participant_type == "financial":
        # Financial futures participants
        participants = {}
        
        # Look for Dealer columns
        dealer_long = [col for col in columns if 'Dealer' in col and 'Long' in col and 'All' in col]
        dealer_short = [col for col in columns if 'Dealer' in col and 'Short' in col and 'All' in col]
        if dealer_long and dealer_short:
            participants["Dealers"] = (dealer_long[0], dealer_short[0])
        
        # Look for Asset Manager columns
        am_long = [col for col in columns if 'Asset_Mgr' in col and 'Long' in col and 'All' in col]
        am_short = [col for col in columns if 'Asset_Mgr' in col and 'Short' in col and 'All' in col]
        if am_long and am_short:
            participants["AM/FI"] = (am_long[0], am_short[0])
        
        # Look for Leveraged Money columns
        lev_long = [col for col in columns if 'Lev_Money' in col and 'Long' in col and 'All' in col]
        lev_short = [col for col in columns if 'Lev_Money' in col and 'Short' in col and 'All' in col]
        if lev_long and lev_short:
            participants["Lev Funds"] = (lev_long[0], lev_short[0])
        
        # Look for Non-Reportable columns
        nr_long = [col for col in columns if 'NonRept' in col and 'Long' in col and 'All' in col]
        nr_short = [col for col in columns if 'NonRept' in col and 'Short' in col and 'All' in col]
        if nr_long and nr_short:
            participants["Non-Rept"] = (nr_long[0], nr_short[0])
            
    else:  # commodity
        participants = {}
        
        # Look for Producer/Merchant columns
        pm_long = [col for col in columns if 'Prod_Merc' in col and 'Long' in col and 'All' in col]
        pm_short = [col for col in columns if 'Prod_Merc' in col and 'Short' in col and 'All' in col]
        if pm_long and pm_short:
            participants["Commercials (Prod/Merc/Proc)"] = (pm_long[0], pm_short[0])
        
        # Look for Managed Money columns
        mm_long = [col for col in columns if 'M_Money' in col and 'Long' in col and 'All' in col]
        mm_short = [col for col in columns if 'M_Money' in col and 'Short' in col and 'All' in col]
        if mm_long and mm_short:
            participants["Managed Money"] = (mm_long[0], mm_short[0])
        
        # Look for Swap Dealer columns
        sd_long = [col for col in columns if 'Swap_Dealer' in col and 'Long' in col and 'All' in col]
        sd_short = [col for col in columns if 'Swap_Dealer' in col and 'Short' in col and 'All' in col]
        if sd_long and sd_short:
            participants["Swap Dealers"] = (sd_long[0], sd_short[0])
        
        # Look for Other Reportable columns
        or_long = [col for col in columns if 'Other_Rept' in col and 'Long' in col and 'All' in col]
        or_short = [col for col in columns if 'Other_Rept' in col and 'Short' in col and 'All' in col]
        if or_long and or_short:
            participants["Other Rept"] = (or_long[0], or_short[0])
        
        # Look for Non-Reportable columns
        nr_long = [col for col in columns if 'NonRept' in col and 'Long' in col and 'All' in col]
        nr_short = [col for col in columns if 'NonRept' in col and 'Short' in col and 'All' in col]
        if nr_long and nr_short:
            participants["Non-Rept"] = (nr_long[0], nr_short[0])
    
    return participants

def get_oi_columns(df, participant_type="financial"):
    """
    Get Open Interest percentage columns
    """
    columns = df.columns.tolist()
    
    if participant_type == "financial":
        participants = {}
        
        # Look for Dealer OI columns
        dealer_long = [col for col in columns if 'Pct_of_OI_Dealer' in col and 'Long' in col]
        dealer_short = [col for col in columns if 'Pct_of_OI_Dealer' in col and 'Short' in col]
        if dealer_long and dealer_short:
            participants["Dealers"] = (dealer_long[0], dealer_short[0])
        
        # Look for Asset Manager OI columns
        am_long = [col for col in columns if 'Pct_of_OI_Asset_Mgr' in col and 'Long' in col]
        am_short = [col for col in columns if 'Pct_of_OI_Asset_Mgr' in col and 'Short' in col]
        if am_long and am_short:
            participants["AM/FI"] = (am_long[0], am_short[0])
        
        # Look for Leveraged Money OI columns
        lev_long = [col for col in columns if 'Pct_of_OI_Lev_Money' in col and 'Long' in col]
        lev_short = [col for col in columns if 'Pct_of_OI_Lev_Money' in col and 'Short' in col]
        if lev_long and lev_short:
            participants["Lev Funds"] = (lev_long[0], lev_short[0])
        
        # Look for Non-Reportable OI columns
        nr_long = [col for col in columns if 'Pct_of_OI_NonRept' in col and 'Long' in col]
        nr_short = [col for col in columns if 'Pct_of_OI_NonRept' in col and 'Short' in col]
        if nr_long and nr_short:
            participants["Non-Rept"] = (nr_long[0], nr_short[0])
            
    else:  # commodity
        participants = {}
        
        # Look for Producer/Merchant OI columns
        pm_long = [col for col in columns if 'Pct_of_OI_Prod_Merc' in col and 'Long' in col]
        pm_short = [col for col in columns if 'Pct_of_OI_Prod_Merc' in col and 'Short' in col]
        if pm_long and pm_short:
            participants["Commercials (Prod/Merc/Proc)"] = (pm_long[0], pm_short[0])
        
        # Look for Managed Money OI columns
        mm_long = [col for col in columns if 'Pct_of_OI_M_Money' in col and 'Long' in col]
        mm_short = [col for col in columns if 'Pct_of_OI_M_Money' in col and 'Short' in col]
        if mm_long and mm_short:
            participants["Managed Money"] = (mm_long[0], mm_short[0])
        
        # Look for Swap Dealer OI columns
        sd_long = [col for col in columns if 'Pct_of_OI_Swap_Dealer' in col and 'Long' in col]
        sd_short = [col for col in columns if 'Pct_of_OI_Swap_Dealer' in col and 'Short' in col]
        if sd_long and sd_short:
            participants["Swap Dealers"] = (sd_long[0], sd_short[0])
        
        # Look for Other Reportable OI columns
        or_long = [col for col in columns if 'Pct_of_OI_Other_Rept' in col and 'Long' in col]
        or_short = [col for col in columns if 'Pct_of_OI_Other_Rept' in col and 'Short' in col]
        if or_long and or_short:
            participants["Other Rept"] = (or_long[0], or_short[0])
        
        # Look for Non-Reportable OI columns
        nr_long = [col for col in columns if 'Pct_of_OI_NonRept' in col and 'Long' in col]
        nr_short = [col for col in columns if 'Pct_of_OI_NonRept' in col and 'Short' in col]
        if nr_long and nr_short:
            participants["Non-Rept"] = (nr_long[0], nr_short[0])
    
    return participants

# ----------------------------
# Fetch data
# ----------------------------
@st.cache_data
def fetch_cot_data():
    fin_df = cot.cot_all(cot_report_type="traders_in_financial_futures_futopt")
    com_df = cot.cot_all(cot_report_type="disaggregated_futopt")

    fin_assets = {**MARKETS_FX, **MARKETS_RATE, **MARKETS_CRYPTO, **MARKETS_INDICES}
    asset_dfs_fin = {}
    asset_dfs_com = {}

    # Financial assets
    for asset, exact_names in fin_assets.items():
        matches = fin_df[fin_df["Market_and_Exchange_Names"].isin(exact_names)]
        if not matches.empty:
            asset_dfs_fin[asset] = matches.copy()

    # Commodity assets
    for asset, exact_names in MARKETS_COMMODITIES.items():
        matches = com_df[com_df["Market_and_Exchange_Names"].isin(exact_names)]
        if not matches.empty:
            asset_dfs_com[asset] = matches.copy()

    return asset_dfs_fin, asset_dfs_com

# ----------------------------
# Compute percentiles
# ----------------------------
def compute_latest_percentiles(asset_dfs, months_list=[12, 18], cot_type="financial"):
    summary_list = []
    participants_map = PARTICIPANTS_FIN if cot_type == "financial" else PARTICIPANTS_COM

    for asset, df in asset_dfs.items():
        df = df.copy()
        df["Date"] = pd.to_datetime(df["Report_Date_as_YYYY-MM-DD"], errors="coerce")
        df = df.dropna(subset=["Date"]).sort_values("Date")
        latest_row = df.iloc[-1]

        total_long = sum(latest_row[cols[0]] for cols in participants_map.values())
        total_short = sum(latest_row[cols[1]] for cols in participants_map.values())
        total_net = total_long - total_short

        asset_summary = {
            "asset": asset,
            "total_long": int(total_long),
            "total_short": int(total_short),
            "total_net": int(total_net)
        }

        for months in months_list:
            cutoff = pd.Timestamp.today() - pd.DateOffset(months=months)
            df_hist = df[df["Date"] >= cutoff]

            for p_name, (long_col, short_col) in participants_map.items():
                long_val = latest_row.get(long_col, 0)
                short_val = latest_row.get(short_col, 0)
                net_val = long_val - short_val

                long_pct = percentileofscore(df_hist[long_col].dropna(), long_val)
                short_pct = percentileofscore(df_hist[short_col].dropna(), short_val)
                net_pct = percentileofscore((df_hist[long_col]-df_hist[short_col]).dropna(), net_val)

                asset_summary[f"{p_name} Long Percentile {months}m"] = round(long_pct, 2)
                asset_summary[f"{p_name} Short Percentile {months}m"] = round(short_pct, 2)
                asset_summary[f"{p_name} Net Percentile {months}m"] = round(net_pct, 2)

        summary_list.append(asset_summary)
    return pd.DataFrame(summary_list)

# ----------------------------
# Plot 4 stacked charts
# ----------------------------
def plot_4rows(asset, asset_dfs, cot_type="financial", months_back=18):
    df = asset_dfs[asset].copy()
    df["Date"] = pd.to_datetime(df["Report_Date_as_YYYY-MM-DD"], errors="coerce")
    df = df.dropna(subset=["Date"]).sort_values("Date")

    cutoff = pd.Timestamp.today() - pd.DateOffset(months=months_back)
    df = df[df["Date"] >= cutoff]

    participants_map = PARTICIPANTS_FIN if cot_type == "financial" else PARTICIPANTS_COM

    fig = make_subplots(rows=4, cols=1, subplot_titles=[p for p in participants_map.keys()])

    row = 1
    for p_name, (long_col, short_col) in participants_map.items():
        # Longs
        fig.add_trace(go.Bar(
            x=df["Date"], y=df[long_col],
            name=f"{p_name} Long", marker_color="green"
        ), row=row, col=1)

        # Shorts
        fig.add_trace(go.Bar(
            x=df["Date"], y=-df[short_col],
            name=f"{p_name} Short", marker_color="red"
        ), row=row, col=1)

        # Net
        net_val = df[long_col] - df[short_col]
        fig.add_trace(go.Scatter(
            x=df["Date"], y=net_val,
            mode="lines+markers",
            name=f"{p_name} Net", line=dict(color="purple")
        ), row=row, col=1)

        row += 1

    fig.update_layout(
        height=1200, width=1200,
        title=dict(text=f"{asset} Positions (Last {months_back} Months)", x=0.5, xanchor="center"),
        barmode="relative"
    )
    return fig


# ----------------------------
# Plot Open Interest charts
# ----------------------------
def plot_oi_4rows(asset, asset_dfs, cot_type="financial", months_back=18):
    df = asset_dfs[asset].copy()
    df["Date"] = pd.to_datetime(df["Report_Date_as_YYYY-MM-DD"], errors="coerce")
    df = df.dropna(subset=["Date"]).sort_values("Date")

    cutoff = pd.Timestamp.today() - pd.DateOffset(months=months_back)
    df = df[df["Date"] >= cutoff]

    # Use correct participant mappings for OI
    participants_map = PARTICIPANTS_FIN_OI if cot_type == "financial" else PARTICIPANTS_COM_OI

    fig = make_subplots(rows=4, cols=1, subplot_titles=[p for p in participants_map.keys()])

    row = 1
    for p_name, (long_col, short_col) in participants_map.items():
        # Long OI as positive
        oi_long = df[long_col]

        # Short OI as negative
        oi_short = -df[short_col]

        # Plot Long OI
        fig.add_trace(go.Bar(
            x=df["Date"], y=oi_long,
            name=f"{p_name} Long OI", marker_color="green"
        ), row=row, col=1)

        # Plot Short OI
        fig.add_trace(go.Bar(
            x=df["Date"], y=oi_short,
            name=f"{p_name} Short OI", marker_color="red"
        ), row=row, col=1)

        # Net OI as a line
        net_oi = df[long_col] - df[short_col]
        fig.add_trace(go.Scatter(
            x=df["Date"], y=net_oi,
            mode="lines+markers",
            name=f"{p_name} Net OI", line=dict(color="purple")
        ), row=row, col=1)

        row += 1

    fig.update_layout(
        height=1200, width=1200,
        title=dict(text=f"{asset} Open Interest (Last {months_back} Months)", x=0.5, xanchor="center"),
        barmode="relative"
    )
    return fig


# ----------------------------
# Streamlit App
# ----------------------------
st.title("CFTC Market Participants Positioning")

asset_dfs_fin, asset_dfs_com = fetch_cot_data()
percentiles_com = compute_latest_percentiles(asset_dfs_com, cot_type="commodity")
percentiles_fin = compute_latest_percentiles(asset_dfs_fin, cot_type="financial")

pages = {
    "Commodity Futures": MARKETS_COMMODITIES,
    "FX Futures": MARKETS_FX,
    "Rate Futures": MARKETS_RATE,
    "Crypto Futures": MARKETS_CRYPTO,
    "Equity Index Futures": MARKETS_INDICES
}

page = st.sidebar.selectbox("Select Market Page", list(pages.keys()))
assets = list(pages[page].keys())
selected_asset = st.sidebar.selectbox(f"Select Asset ({page})", assets)

# Choose which asset_dfs and percentiles_df to use
if page == "Commodity Futures":
    df_dict = asset_dfs_com
    pct_df = percentiles_com
    cot_type = "commodity"
else:
    df_dict = asset_dfs_fin
    pct_df = percentiles_fin
    cot_type = "financial"

# Get latest available date for this asset
latest_date = None
if selected_asset in df_dict:
    df_temp = df_dict[selected_asset].copy()
    df_temp["Date"] = pd.to_datetime(df_temp["Report_Date_as_YYYY-MM-DD"], errors="coerce")
    df_temp = df_temp.dropna(subset=["Date"])
    if not df_temp.empty:
        latest_date = df_temp["Date"].max().strftime("%Y-%m-%d")

# ----------------------------
# Show Charts
# ----------------------------
st.subheader(f"{selected_asset} Positioning" + (f" (Latest: {latest_date})" if latest_date else ""))
st.plotly_chart(plot_4rows(selected_asset, df_dict, cot_type=cot_type, months_back=18))

# ----------------------------
# Show Open Interest Charts
# ----------------------------
st.subheader(f"{selected_asset} OI Percentages" + (f" (Latest: {latest_date})" if latest_date else ""))
st.plotly_chart(plot_oi_4rows(selected_asset, df_dict, cot_type=cot_type, months_back=18))


# ----------------------------
# Show Percentiles
# ----------------------------
st.subheader(f"{selected_asset} Positioning Percentiles" + (f" (Latest: {latest_date})" if latest_date else ""))
participants_map = PARTICIPANTS_FIN if cot_type == "financial" else PARTICIPANTS_COM

def color_percentiles(val):
    """Red (0%) → Green (100%)"""
    if pd.isna(val):
        return ''
    red = int(255 * (100 - val) / 100)
    green = int(255 * val / 100)
    return f'background-color: rgb({red},{green},0)'

for p_name, _ in participants_map.items():
    st.markdown(f"**{p_name}**")
    # Get all participant columns, exclude 'asset'
    cols = [col for col in pct_df.columns if col.startswith(p_name)]
    df_show = pct_df[pct_df["asset"] == selected_asset][cols].copy()
    
    # Apply color styling
    styled_df = df_show.style.applymap(color_percentiles).format("{:.2f}")
    
    # Render without index
    st.markdown(styled_df.hide(axis="index").to_html(), unsafe_allow_html=True)

# ----------------------------
# Show Open Interest Section
# ----------------------------
if latest_date:
    st.subheader(f"{selected_asset} OI (Latest: {latest_date})")
else:
    st.subheader(f"{selected_asset} OI")

if selected_asset in df_dict:
    df_temp = df_dict[selected_asset].copy()
    df_temp["Date"] = pd.to_datetime(df_temp["Report_Date_as_YYYY-MM-DD"], errors="coerce")
    df_temp = df_temp.dropna(subset=["Date"]).sort_values("Date")

    if not df_temp.empty:
        latest_row = df_temp.iloc[-1]

        # Map participants
        participants_map = PARTICIPANTS_FIN if cot_type == "financial" else PARTICIPANTS_COM

        for p_name, (long_col, short_col) in participants_map.items():
            st.markdown(f"**{p_name}**")

            # Construct dictionary for OI + Pct of OI
            oi_data = {
                "Long OI": latest_row.get(long_col, 0),
                "Short OI": latest_row.get(short_col, 0),
                "Net OI": latest_row.get(long_col, 0) - latest_row.get(short_col, 0),
                "% Long OI": latest_row.get(f"Pct_of_OI_{long_col.replace('_Positions_', '_')}", 0),
                "% Short OI": latest_row.get(f"Pct_of_OI_{short_col.replace('_Positions_', '_')}", 0),
                "% Net OI": (latest_row.get(f"Pct_of_OI_{long_col.replace('_Positions_', '_')}", 0)
                             - latest_row.get(f"Pct_of_OI_{short_col.replace('_Positions_', '_')}", 0))
            }

            st.dataframe(pd.DataFrame([oi_data]), use_container_width=True, hide_index=True)

    else:
        st.info("No open interest data available for this asset.")
        
# ----------------------------
# Streamlit App
# ----------------------------
def main():
    st.set_page_config(page_title="CFTC Market Participants Positioning", layout="wide")
    st.title("CFTC Market Participants Positioning")

    # Add error handling for data loading
    try:
        with st.spinner("Loading COT data..."):
            asset_dfs_fin, asset_dfs_com = fetch_cot_data()
        
        if not asset_dfs_fin and not asset_dfs_com:
            st.error("No data could be loaded. Please check your internet connection and try again.")
            return
            
        percentiles_com = compute_latest_percentiles(asset_dfs_com, cot_type="commodity")
        percentiles_fin = compute_latest_percentiles(asset_dfs_fin, cot_type="financial")

        pages = {
            "Commodity Futures": MARKETS_COMMODITIES,
            "FX Futures": MARKETS_FX,
            "Rate Futures": MARKETS_RATE,
            "Crypto Futures": MARKETS_CRYPTO,
            "Equity Index Futures": MARKETS_INDICES
        }

        page = st.sidebar.selectbox("Select Market Page", list(pages.keys()))
        assets = list(pages[page].keys())
        selected_asset = st.sidebar.selectbox(f"Select Asset ({page})", assets)

        # Choose which asset_dfs and percentiles_df to use
        if page == "Commodity Futures":
            df_dict = asset_dfs_com
            pct_df = percentiles_com
            cot_type = "commodity"
        else:
            df_dict = asset_dfs_fin
            pct_df = percentiles_fin
            cot_type = "financial"

        if selected_asset not in df_dict:
            st.warning(f"No data available for {selected_asset}")
            return

        # Get latest available date for this asset
        latest_date = None
        df_temp = df_dict[selected_asset].copy()
        df_temp["Date"] = pd.to_datetime(df_temp["Report_Date_as_YYYY-MM-DD"], errors="coerce")
        df_temp = df_temp.dropna(subset=["Date"])
        if not df_temp.empty:
            latest_date = df_temp["Date"].max().strftime("%Y-%m-%d")

        # ----------------------------
        # Show Charts
        # ----------------------------
        st.subheader(f"{selected_asset} Positioning" + (f" (Latest: {latest_date})" if latest_date else ""))
        
        chart = plot_4rows(selected_asset, df_dict, cot_type=cot_type, months_back=18)
        if chart:
            st.plotly_chart(chart, use_container_width=True)

        # ----------------------------
        # Show Open Interest Charts
        # ----------------------------
        st.subheader(f"{selected_asset} OI Percentages" + (f" (Latest: {latest_date})" if latest_date else ""))
        
        oi_chart = plot_oi_4rows(selected_asset, df_dict, cot_type=cot_type, months_back=18)
        if oi_chart:
            st.plotly_chart(oi_chart, use_container_width=True)

        # ----------------------------
        # Show Percentiles
        # ----------------------------
        st.subheader(f"{selected_asset} Positioning Percentiles" + (f" (Latest: {latest_date})" if latest_date else ""))
        
        # Get actual participants for this asset
        sample_df = df_dict[selected_asset]
        participants_map = get_available_columns(sample_df, cot_type)

        def color_percentiles(val):
            """Red (0%) → Green (100%)"""
            if pd.isna(val):
                return ''
            red = int(255 * (100 - val) / 100)
            green = int(255 * val / 100)
            return f'background-color: rgb({red},{green},0)'

        if not pct_df.empty and selected_asset in pct_df['asset'].values:
            for p_name, _ in participants_map.items():
                st.markdown(f"**{p_name}**")
                # Get all participant columns, exclude 'asset'
                cols = [col for col in pct_df.columns if col.startswith(p_name)]
                if cols:
                    df_show = pct_df[pct_df["asset"] == selected_asset][cols].copy()
                    
                    if not df_show.empty:
                        # Apply color styling
                        styled_df = df_show.style.applymap(color_percentiles).format("{:.2f}")
                        
                        # Render without index
                        st.markdown(styled_df.hide(axis="index").to_html(), unsafe_allow_html=True)
                    else:
                        st.info(f"No percentile data available for {p_name}")
        else:
            st.info("No percentile data available for this asset")

        # ----------------------------
        # Show Raw Data Summary
        # ----------------------------
        st.subheader(f"{selected_asset} Current Positions Summary")
        
        if not pct_df.empty and selected_asset in pct_df['asset'].values:
            summary_data = pct_df[pct_df["asset"] == selected_asset][['total_long', 'total_short', 'total_net']].copy()
            summary_data.columns = ['Total Long', 'Total Short', 'Total Net']
            st.dataframe(summary_data, use_container_width=True, hide_index=True)
        else:
            st.info("No summary data available for this asset")

        # ----------------------------
        # Show Open Interest Section
        # ----------------------------
        st.subheader(f"{selected_asset} Open Interest Breakdown" + (f" (Latest: {latest_date})" if latest_date else ""))

        df_temp = df_dict[selected_asset].copy()
        df_temp["Date"] = pd.to_datetime(df_temp["Report_Date_as_YYYY-MM-DD"], errors="coerce")
        df_temp = df_temp.dropna(subset=["Date"]).sort_values("Date")

        if not df_temp.empty:
            latest_row = df_temp.iloc[-1]

            # Get actual participants and OI columns
            participants_map = get_available_columns(df_temp, cot_type)
            oi_map = get_oi_columns(df_temp, cot_type)

            for p_name, (long_col, short_col) in participants_map.items():
                st.markdown(f"**{p_name}**")

                # Get corresponding OI columns
                oi_long_col = None
                oi_short_col = None
                if p_name in oi_map:
                    oi_long_col, oi_short_col = oi_map[p_name]

                # Construct dictionary for OI + Pct of OI
                oi_data = {
                    "Long OI": int(latest_row.get(long_col, 0)),
                    "Short OI": int(latest_row.get(short_col, 0)),
                    "Net OI": int(latest_row.get(long_col, 0) - latest_row.get(short_col, 0)),
                }
                
                # Add percentage data if available
                if oi_long_col and oi_short_col:
                    oi_data.update({
                        "% Long OI": round(latest_row.get(oi_long_col, 0), 2),
                        "% Short OI": round(latest_row.get(oi_short_col, 0), 2),
                        "% Net OI": round(latest_row.get(oi_long_col, 0) - latest_row.get(oi_short_col, 0), 2)
                    })

                st.dataframe(pd.DataFrame([oi_data]), use_container_width=True, hide_index=True)

        else:
            st.info("No open interest data available for this asset.")

        # ----------------------------
        # Show Data Info
        # ----------------------------
        with st.expander("Data Information"):
            st.markdown("""
            **About this data:**
            - Data source: CFTC Commitment of Traders (COT) reports
            - Update frequency: Weekly (Tuesdays)
            - Financial futures use "Traders in Financial Futures" format
            - Commodity futures use "Disaggregated" format
            
            **Participant Categories:**
            
            **Financial Futures:**
            - **Dealers**: Banks and other financial institutions
            - **AM/FI**: Asset Managers and Fixed Income funds
            - **Lev Funds**: Leveraged funds (hedge funds, CTAs)
            - **Non-Rept**: Non-reportable positions (smaller traders)
            
            **Commodity Futures:**
            - **Commercials**: Producers, merchants, processors
            - **Managed Money**: Hedge funds, CTAs, other money managers
            - **Swap Dealers**: Banks and swap dealers
            - **Other Rept**: Other reportable positions
            - **Non-Rept**: Non-reportable positions (smaller traders)
            
            **Percentiles:** Show where current positions rank vs historical data (0% = lowest, 100% = highest)
            """)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        logger.error(f"Main app error: {str(e)}")
        
        # Show debug info in development
        if st.checkbox("Show debug information"):
            st.exception(e)

if __name__ == "__main__":
    main()