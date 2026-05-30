class GeoMarketMiddleware:
    """
    Detect user market (india/us) from Cloudflare CF-IPCountry header.
    Session override via ?market= query param.
    Sets request.market and request.country_code on every request.
    """

    US_COUNTRIES = {'US'}
    INDIA_COUNTRIES = {'IN'}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Query param override — saves to session
        market_param = request.GET.get('market', '').lower()
        if market_param in ('india', 'us'):
            request.session['market_override'] = market_param

        # Determine market
        market = self._detect_market(request)
        request.market = market
        request.country_code = self._get_country_code(request)

        response = self.get_response(request)
        return response

    INDIA_COUNTRIES = {'IN'}

    def _detect_market(self, request):
        # 1. /in/ URL prefix always means India
        if request.path.startswith('/in/') or request.path == '/in':
            return 'india'

        # 2. Session override (user manually switched)
        override = request.session.get('market_override')
        if override in ('india', 'us'):
            return override

        # 3. Cloudflare header (production)
        country = request.META.get('HTTP_CF_IPCOUNTRY', '').upper()

        # 4. Fallback: X-AppEngine-Country
        if not country:
            country = request.META.get('HTTP_X_APPENGINE_COUNTRY', '').upper()

        if country in self.INDIA_COUNTRIES:
            return 'india'

        # US is primary market — default for all undetected visitors
        return 'us'

    def _get_country_code(self, request):
        if request.path.startswith('/in/') or request.path == '/in':
            return 'IN'

        override = request.session.get('market_override')
        if override == 'us':
            return 'US'
        if override == 'india':
            return 'IN'

        country = request.META.get('HTTP_CF_IPCOUNTRY', '').upper()
        if not country:
            country = request.META.get('HTTP_X_APPENGINE_COUNTRY', '').upper()
        return country or 'US'
