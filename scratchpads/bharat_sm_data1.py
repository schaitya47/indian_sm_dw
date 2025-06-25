from Technical import NSE as tense
from Derivatives import Sensibull as sb,NSE as DSE
from Fundamentals import Tickertape, MoneyControl
import json
from datetime import datetime

#Created an instance of the NSE class
nse = tense()



# Some NSE basic functions this is available any NSE Object (Technical OR Derivatives)
# searching
# search_res = nse.search('Syrma SGS')
# print(search_res.get('symbols')[0].get('symbol'))

# # Last Traded date
# print(nse.get_last_traded_date())

# # Last traded Status and Nifty val
# print(nse.get_market_status_and_current_val())

# just provides link of important reports (not required to use)
# imp_reports_link = nse.get_important_reports()
# print(imp_reports_link)


# trade_df = nse.get_nse_turnover() #not working
# trade_df.head()#not working
# nse.get_all_indices() #not working
# index_df = nse.get_equities_data_from_index() #not working
# print(nse.get_nse_equity_meta_info('SYRMA')) #Not working
# nse.get_ohlc_data('EASEMYTRIP', is_index=False ) #not working
# nse.get_trade_info('CENTRALBK').T #not working
# nse.get_corporate_disclosures('EASEMYTRIP') #not working


dse = DSE()


# dse.get_options_expiry('NIFTY', is_index=True) # not working
# oi_pcr = dse.get_pcr('FINNIFTY', is_index=True) # not working
# dse.get_all_derivatives_enabled_stocks() #not working
# dse.get_equity_options_trade_info("ADANIPORTS") #not working

sb = sb()

# sb_nifty_token = sb.search_token('NIFTY') # gets the instrument token of NIFTY
# Returns all the contracts for the NIFTY index for the given date and atm strike price.
# greeks_df, atm_strike = sb.get_options_data_with_greeks(sb_nifty_token, num_look_ups_from_atm=10,expiry_date=datetime(2025, 6, 26))
# print(greeks_df, atm_strike)














