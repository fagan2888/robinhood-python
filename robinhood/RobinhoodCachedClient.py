from __future__ import print_function

import getpass
import json
import os

from .exceptions import MfaRequired
from .RobinhoodClient import RobinhoodClient
from .util import get_last_id_from_url

cache_root_path = '.robinhood'
if not os.path.exists(cache_root_path):
  os.makedirs(cache_root_path)

# Cache modes
CACHE_FIRST = 'CACHE_FIRST'
FORCE_LIVE = 'FORCE_LIVE'
FORCE_CACHE = 'FORCE_CACHE'

class RobinhoodCachedClient(RobinhoodClient):
  def __init__(self):
    super(RobinhoodCachedClient, self).__init__()

  def login(self, force_login=False):
    cache_path = os.path.join(cache_root_path, 'auth_token')
    if os.path.exists(cache_path) and not force_login:
      with open(cache_path, 'r') as cache_file:
        self.set_auth_token(cache_file.read())
    else:
      # Get a new auth token
      username = input('Username: ')
      password = getpass.getpass()

      try:
        auth_token = self.set_auth_token_with_credentials(username, password)
      except MfaRequired:
        mfa = input('MFA: ')
        auth_token = self.set_auth_token_with_credentials(username, password, mfa)

      with open(cache_path, 'w') as cache_file:
        cache_file.write(auth_token)

  def logout(self):
    cache_path = os.path.join(cache_root_path, 'auth_token')
    if os.path.exists(cache_path):
      os.remove(cache_path)

  def _simple_call(self, cache_name, method, cache_mode, args=[], kwargs={}, binary=False):
    cache_path = os.path.join(cache_root_path, cache_name)
    binary_flag = 'b' if binary else ''
    if os.path.exists(cache_path) and cache_mode != FORCE_LIVE:
      with open(cache_path, 'r' + binary_flag) as cache_file:
        if binary:
          return cache_file.read()
        else:
          return json.load(cache_file)
    elif cache_mode == FORCE_CACHE:
      return None
    else:
      live_content = method(*args, **kwargs)
      with open(cache_path, 'w' + binary_flag) as cache_file:
        if binary:
          cache_file.write(live_content)
        else:
          json.dump(live_content, cache_file)
      return live_content

  def get_user(self, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'user',
      super(RobinhoodCachedClient, self).get_user,
      cache_mode
    )

  def get_user_basic_info(self, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'user_basic_info',
      super(RobinhoodCachedClient, self).get_user_basic_info,
      cache_mode
    )

  def get_user_additional_info(self, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'user_additional_info',
      super(RobinhoodCachedClient, self).get_user_additional_info,
      cache_mode
    )

  def get_referral_code(self, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'referral_code',
      super(RobinhoodCachedClient, self).get_referral_code,
      cache_mode
    )

  def get_subscription_fees(self, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'subscription_fees',
      super(RobinhoodCachedClient, self).get_subscription_fees,
      cache_mode
    )

  def get_subscriptions(self, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'subscriptions',
      super(RobinhoodCachedClient, self).get_subscriptions,
      cache_mode
    )

  def get_markets(self, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'markets',
      super(RobinhoodCachedClient, self).get_markets,
      cache_mode
    )

  def download_document_by_id(self, document_id, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'document_pdf_{}'.format(document_id),
      super(RobinhoodCachedClient, self).download_document_by_id,
      cache_mode,
      args=[document_id],
      binary=True
    )

  def get_document_by_id(self, document_id):
    return self._simple_call(
      'document_{}'.format(document_id),
      super(RobinhoodCachedClient, self).get_document_by_id,
      # Documents don't change, never force live
      CACHE_FIRST,
      args=[document_id]
    )

  def get_watchlists(self, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'watchlists',
      super(RobinhoodCachedClient, self).get_watchlists,
      cache_mode
    )

  def get_watchlist_instruments(self, watchlist_name, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'watchlist_instruments_{}'.format(watchlist_name),
      super(RobinhoodCachedClient, self).get_watchlist_instruments,
      cache_mode,
      args=[watchlist_name]
    )

  def get_notification_settings(self, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'notification_settings',
      super(RobinhoodCachedClient, self).get_notification_settings,
      cache_mode
    )

  def get_notification_devices(self, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'notification_devices',
      super(RobinhoodCachedClient, self).get_notification_devices,
      cache_mode
    )

  def get_account(self, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'account',
      super(RobinhoodCachedClient, self).get_account,
      cache_mode
    )

  def get_investment_profile(self, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'investment_profile',
      super(RobinhoodCachedClient, self).get_investment_profile,
      cache_mode
    )

  def get_similar_to(self, instrument_id, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'similar_to_{}'.format(instrument_id),
      super(RobinhoodCachedClient, self).get_similar_to,
      cache_mode,
      args=[instrument_id]
    )

  def get_popularity(self, instrument_id, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'popularity_{}'.format(instrument_id),
      super(RobinhoodCachedClient, self).get_popularity,
      cache_mode,
      args=[instrument_id]
    )

  def get_rating(self, instrument_id, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'rating_{}'.format(instrument_id),
      super(RobinhoodCachedClient, self).get_rating,
      cache_mode,
      args=[instrument_id]
    )

  def get_instrument_reasons_for_personal_tag(self, tag, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'instrument_reasons_for_personal_tag_{}'.format(tag),
      super(RobinhoodCachedClient, self).get_instrument_reasons_for_personal_tag,
      cache_mode,
      args=[tag]
    )

  def get_instrument_ids_for_tag(self, tag, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'tag_{}'.format(tag),
      super(RobinhoodCachedClient, self).get_instrument_ids_for_tag,
      cache_mode,
      args=[tag]
    )

  def get_instrument_by_id(self, instrument_id, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'instrument_{}'.format(instrument_id),
      super(RobinhoodCachedClient, self).get_instrument_by_id,
      cache_mode,
      args=[instrument_id]
    )

  def get_instrument_by_symbol(self, symbol, cache_mode=CACHE_FIRST):
    symbol_instrument_id_cache_path = os.path.join(cache_root_path, 'symbol_instrument_id_{}'.format(symbol))
    if os.path.exists(symbol_instrument_id_cache_path):
      with open(symbol_instrument_id_cache_path, 'r') as symbol_instrument_id_cache_file:
        instrument_id = symbol_instrument_id_cache_file.read()
      return self.get_instrument_by_id(instrument_id, cache_mode=cache_mode)

    instrument = self._simple_call(
      'instrument_{}'.format(symbol),
      super(RobinhoodCachedClient, self).get_instrument_by_symbol,
      cache_mode,
      args=[symbol]
    )
    instrument_id = instrument['id']

    os.rename(
      os.path.join(cache_root_path, 'instrument_{}'.format(symbol)), 
      os.path.join(cache_root_path, 'instrument_{}'.format(instrument_id))
    )
    with open(symbol_instrument_id_cache_path, 'w') as symbol_instrument_id_cache_file:
      symbol_instrument_id_cache_file.write(instrument_id)

    return instrument

  def get_instrument_split_history(self, instrument_id, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'instrument_split_history_{}'.format(instrument_id),
      super(RobinhoodCachedClient, self).get_instrument_split_history,
      cache_mode,
      args=[instrument_id]
    )

  def get_quote(self, instrument_id, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'quote_{}'.format(instrument_id),
      super(RobinhoodCachedClient, self).get_quote,
      cache_mode,
      args=[instrument_id]
    )

  def get_dividend_by_id(self, dividend_id, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'dividend_{}'.format(dividend_id),
      super(RobinhoodCachedClient, self).get_dividend_by_id,
      cache_mode,
      args=[dividend_id]
    )

  def get_ach_relationship_by_id(self, relationship_id, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'ach_relationship_{}'.format(relationship_id),
      super(RobinhoodCachedClient, self).get_ach_relationship_by_id,
      cache_mode,
      args=[relationship_id]
    )

  def get_ach_transfer_by_id(self, transfer_id, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'ach_transfer_{}'.format(transfer_id),
      super(RobinhoodCachedClient, self).get_ach_transfer_by_id,
      cache_mode,
      args=[transfer_id]
    )

  def get_popular_stocks(self, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'popular_stocks',
      super(RobinhoodCachedClient, self).get_popular_stocks,
      cache_mode
    )

  def get_sp500_movers(self, direction, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'sp500_movers_{}'.format(direction),
      super(RobinhoodCachedClient, self).get_sp500_movers,
      cache_mode,
      args=[direction]
    )

  def get_portfolio(self, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'portfolio',
      super(RobinhoodCachedClient, self).get_portfolio,
      cache_mode
    )

  def get_position_by_instrument_id(self, instrument_id, use_account_number=None, cache_mode=CACHE_FIRST):
    account_number = use_account_number or self.get_account()['account_number']
    return self._simple_call(
      'position_{}'.format(instrument_id),
      super(RobinhoodCachedClient, self).get_position_by_instrument_id,
      cache_mode,
      args=[account_number, instrument_id]
    )

  def get_news(self, symbol, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'news_{}'.format(symbol),
      super(RobinhoodCachedClient, self).get_news,
      cache_mode,
      args=[symbol]
    )

  def get_tags(self, instrument_id, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'tags_{}'.format(instrument_id),
      super(RobinhoodCachedClient, self).get_tags,
      cache_mode,
      args=[instrument_id]
    )

  def get_fundamental(self, instrument_id, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'fundamental_{}'.format(instrument_id),
      super(RobinhoodCachedClient, self).get_fundamental,
      cache_mode,
      args=[instrument_id]
    )

  def get_referrals(self, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'referrals',
      super(RobinhoodCachedClient, self).get_referrals,
      cache_mode
    )

  def get_order_by_id(self, order_id, cache_mode=CACHE_FIRST):
    return self._simple_call(
      'order_{}'.format(order_id),
      super(RobinhoodCachedClient, self).get_order_by_id,
      cache_mode,
      args=[order_id]
    )

  def _search_and_cache_call(
      self,
      search_method,
      item_to_id_method,
      item_cache_name_template,
      search_args=[],
      search_kwargs={}):
    results = []
    live_search_content = search_method(*search_args, **search_kwargs)
    for live_item in live_search_content:
      results.append(live_item)
      item_id = item_to_id_method(live_item)
      item_cache_path = os.path.join(cache_root_path, item_cache_name_template.format(item_id))
      with open(item_cache_path, 'w') as item_cache_file:
        json.dump(live_item, item_cache_file)
    return results

  def _list_call(
      self,
      list_cache_name,
      list_method,
      item_method,
      item_to_id_method,
      item_cache_name_template,
      cache_mode,
      list_args=[],
      list_kwargs={}):
    results = []
    list_cache_path = os.path.join(cache_root_path, list_cache_name)
    if os.path.exists(list_cache_path) and cache_mode != FORCE_LIVE:
      with open(list_cache_path, 'r') as list_cache_file:
        list_json = json.load(list_cache_file)
        for item_id in list_json:
          results.append(item_method(item_id, cache_mode=cache_mode))
    else:
      live_list_content = self._search_and_cache_call(
          list_method,
          item_to_id_method,
          item_cache_name_template,
          search_args=list_args,
          search_kwargs=list_kwargs)
      live_list_ids = []
      for live_item in live_list_content:
        item_id = item_to_id_method(live_item)
        live_list_ids.append(item_id)
        results.append(live_item)
      with open(list_cache_path, 'w') as list_cache_file:
        json.dump(live_list_ids, list_cache_file)
    return results

  def get_documents(self, cache_mode=CACHE_FIRST):
    return self._list_call(
      'documents',
      super(RobinhoodCachedClient, self).get_documents,
      self.get_document_by_id,
      lambda document: document['id'],
      'document_{}',
      cache_mode
    )

  def get_ach_transfers(self, cache_mode=CACHE_FIRST):
    return self._list_call(
      'ach_transfers',
      super(RobinhoodCachedClient, self).get_ach_transfers,
      self.get_ach_transfer_by_id,
      lambda ach_transfer: ach_transfer['id'],
      'ach_transfer_{}',
      cache_mode
    )

  def get_dividends(self, cache_mode=CACHE_FIRST):
    return self._list_call(
      'dividends',
      super(RobinhoodCachedClient, self).get_dividends,
      self.get_dividend_by_id,
      lambda dividend: dividend['id'],
      'dividend_{}',
      cache_mode
    )

  def get_positions(self, include_old=False, cache_mode=CACHE_FIRST):
    return self._list_call(
      'positions_' + ('all' if include_old else  'current'),
      super(RobinhoodCachedClient, self).get_positions,
      self.get_position_by_instrument_id,
      lambda position: get_last_id_from_url(position['instrument']),
      'position_{}',
      cache_mode,
      list_kwargs={'include_old': include_old}
    )

  def get_orders(self, instrument_id=False, cache_mode=CACHE_FIRST):
    return self._list_call(
      'instrument_orders_{}'.format(instrument_id) if instrument_id else 'orders',
      super(RobinhoodCachedClient, self).get_orders,
      self.get_order_by_id,
      lambda order: order['id'],
      'order_{}',
      cache_mode,
      list_kwargs={'instrument_id': instrument_id}
    )

  def _search_call(
      self,
      item_ids,
      search_method,
      item_to_id_method,
      item_cache_name_template,
      item_method,
      cache_mode):
    items = []
    unfound_item_ids = item_ids[:]
    if cache_mode != FORCE_LIVE:
      for item_id in item_ids:
        item = item_method(item_id, cache_mode=FORCE_CACHE)
        if item:
          unfound_item_ids.remove(item_id)
          items.append(item)

    if unfound_item_ids:
      live_search_content = self._search_and_cache_call(
          search_method,
          item_to_id_method,
          item_cache_name_template,
          search_args=[unfound_item_ids])
      items.extend(live_search_content)

    return items

  def get_instruments(self, instrument_ids, cache_mode=CACHE_FIRST):
    return self._search_call(
        instrument_ids,
        super(RobinhoodCachedClient, self).get_instruments,
        lambda instrument: instrument['id'],
        'instrument_{}',
        self.get_instrument_by_id,
        cache_mode)

  def get_fundamentals(self, instrument_ids, cache_mode=CACHE_FIRST):
    return self._search_call(
        instrument_ids,
        super(RobinhoodCachedClient, self).get_fundamentals,
        lambda fundamental: get_last_id_from_url(fundamental['instrument']),
        'fundamental_{}',
        self.get_fundamental,
        cache_mode)

  def get_popularities(self, instrument_ids, cache_mode=CACHE_FIRST):
    return self._search_call(
        instrument_ids,
        super(RobinhoodCachedClient, self).get_popularities,
        lambda popularity: get_last_id_from_url(popularity['instrument']),
        'popularity_{}',
        self.get_popularity,
        cache_mode)

  def get_ratings(self, instrument_ids, cache_mode=CACHE_FIRST):
    return self._search_call(
        instrument_ids,
        super(RobinhoodCachedClient, self).get_ratings,
        lambda rating: rating['instrument_id'],
        'rating_{}',
        self.get_rating,
        cache_mode)

  def get_quotes(self, instrument_ids, cache_mode=CACHE_FIRST):
    return self._search_call(
        instrument_ids,
        super(RobinhoodCachedClient, self).get_quotes,
        lambda quote: get_last_id_from_url(quote['instrument']),
        'quote_{}',
        self.get_quote,
        cache_mode)

  # TODO: get_prices
  # TODO: get_historical_quotes
