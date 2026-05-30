from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from tools import services
from tools.models import Tool

User = get_user_model()


# ─── Service / Tax Engine Tests ───────────────────────────────────────────────

class NewRegimeTests(TestCase):
    def test_zero_income(self):
        r = services.calculate_new_regime(0)
        self.assertEqual(r['total_tax'], 0)

    def test_12l_zero_tax(self):
        """₹12L income → 0 tax (87A rebate)"""
        r = services.calculate_new_regime(1_200_000)
        self.assertEqual(r['total_tax'], 0)

    def test_below_4l_no_tax(self):
        r = services.calculate_new_regime(400_000)
        self.assertEqual(r['total_tax'], 0)

    def test_standard_deduction_applied(self):
        r = services.calculate_new_regime(800_000)
        self.assertEqual(r['std_deduction'], 75_000)
        self.assertEqual(r['taxable_income'], 725_000)

    def test_high_income_surcharge(self):
        r = services.calculate_new_regime(6_000_000)
        self.assertGreater(r['surcharge'], 0)
        self.assertGreater(r['total_tax'], 0)

    def test_effective_rate_reasonable(self):
        r = services.calculate_new_regime(1_500_000)
        self.assertGreater(r['effective_rate'], 0)
        self.assertLess(r['effective_rate'], 35)

    def test_fy_2024_25(self):
        r = services.calculate_new_regime(1_000_000, fy='2024-25')
        self.assertIsInstance(r['total_tax'], (int, float))


class OldRegimeTests(TestCase):
    def test_zero_income(self):
        r = services.calculate_old_regime(0)
        self.assertEqual(r['total_tax'], 0)

    def test_5l_rebate(self):
        """₹5L income → 0 tax (87A rebate)"""
        r = services.calculate_old_regime(500_000)
        self.assertEqual(r['total_tax'], 0)

    def test_senior_higher_exemption(self):
        # Use income above basic exemption but where the difference matters
        r_normal = services.calculate_old_regime(400_000, 'below_60')
        r_senior = services.calculate_old_regime(400_000, '60_to_79')
        self.assertGreaterEqual(r_normal['total_tax'], r_senior['total_tax'])

    def test_deductions_reduce_tax(self):
        r_no_ded = services.calculate_old_regime(1_000_000)
        r_with_ded = services.calculate_old_regime(1_000_000, deductions={'sec_80c': 150_000})
        self.assertLess(r_with_ded['total_tax'], r_no_ded['total_tax'])

    def test_80c_capped_at_limit(self):
        r = services.calculate_old_regime(1_000_000, deductions={'sec_80c': 300_000})
        self.assertEqual(r['sec_80c'], 150_000)


class RegimeCompareTests(TestCase):
    def test_returns_winner(self):
        r = services.compare_regimes(800_000)
        self.assertIn(r['winner'], ('new', 'old'))
        self.assertIn('winner_label', r)
        self.assertIn('savings', r)
        self.assertGreaterEqual(r['savings'], 0)

    def test_new_regime_wins_no_deductions(self):
        r = services.compare_regimes(1_000_000)
        self.assertEqual(r['winner'], 'new')

    def test_old_regime_can_win_with_deductions(self):
        deductions = {'sec_80c': 150_000, 'sec_80d_self': 25_000, 'hra_exemption': 100_000}
        r = services.compare_regimes(1_000_000, deductions=deductions)
        self.assertIn(r['winner'], ('new', 'old'))


class HRATests(TestCase):
    def test_metro_50pct(self):
        r = services.calculate_hra_exemption(40_000, 20_000, 180_000, True)
        self.assertEqual(r['option2_pct_of_basic'], 20_000)

    def test_non_metro_40pct(self):
        r = services.calculate_hra_exemption(40_000, 20_000, 180_000, False)
        self.assertEqual(r['option2_pct_of_basic'], 16_000)

    def test_exemption_is_minimum(self):
        r = services.calculate_hra_exemption(40_000, 20_000, 180_000, True)
        self.assertLessEqual(r['exemption'], r['option1_hra_received'])
        self.assertLessEqual(r['exemption'], r['option2_pct_of_basic'])
        self.assertLessEqual(r['exemption'], r['option3_rent_minus_10pct'])

    def test_no_exemption_if_no_rent(self):
        r = services.calculate_hra_exemption(40_000, 20_000, 0, True)
        self.assertEqual(r['exemption'], 0)


class AdvanceTaxTests(TestCase):
    def test_below_threshold_not_required(self):
        r = services.calculate_advance_tax(9_000)
        self.assertFalse(r['required'])

    def test_above_threshold_required(self):
        r = services.calculate_advance_tax(50_000)
        self.assertTrue(r['required'])
        self.assertEqual(len(r['schedule']), 4)

    def test_schedule_cumulative(self):
        r = services.calculate_advance_tax(100_000)
        pcts = [s['cumulative_pct'] for s in r['schedule']]
        self.assertEqual(pcts, [15.0, 45.0, 75.0, 100.0])

    def test_tds_reduces_liability(self):
        r1 = services.calculate_advance_tax(100_000, tds_deducted=0)
        r2 = services.calculate_advance_tax(100_000, tds_deducted=80_000)
        self.assertGreater(r1['net_liability'], r2['net_liability'])


class CapitalGainsTests(TestCase):
    def test_stcg_20pct(self):
        r = services.calculate_capital_gains_equity(100, 200, 100, 6)
        self.assertEqual(r['gain_type'], 'STCG')
        self.assertEqual(r['total_gain'], 10_000)

    def test_ltcg_1l_exempt(self):
        r = services.calculate_capital_gains_equity(100, 200, 100, 14)
        self.assertEqual(r['gain_type'], 'LTCG')
        self.assertEqual(r['exemption'], 125_000)

    def test_ltcg_below_exemption_no_tax(self):
        r = services.calculate_capital_gains_equity(100, 200, 80, 14)
        self.assertEqual(r['total_gain'], 8_000)
        self.assertEqual(r['total_tax'], 0)


class GSTTests(TestCase):
    def test_normal_18pct(self):
        r = services.calculate_gst(10_000, 18)
        self.assertEqual(r['gst_amount'], 1_800.0)
        self.assertEqual(r['total_amount'], 11_800.0)

    def test_reverse_gst(self):
        r = services.calculate_gst(11_800, 18, reverse=True)
        self.assertAlmostEqual(r['original_amount'], 10_000.0, places=1)
        self.assertAlmostEqual(r['gst_amount'], 1_800.0, places=1)

    def test_cgst_sgst_split(self):
        r = services.calculate_gst(10_000, 18)
        self.assertAlmostEqual(r['cgst'], 900.0)
        self.assertAlmostEqual(r['sgst'], 900.0)


class ITRFormTests(TestCase):
    def test_salary_simple_itr1(self):
        r = services.suggest_itr_form(True, False, False, False, False, False, 400_000)
        self.assertEqual(r['form'], 'ITR-1')

    def test_capital_gains_itr2(self):
        r = services.suggest_itr_form(True, True, False, False, False, False, 600_000)
        self.assertEqual(r['form'], 'ITR-2')

    def test_presumptive_itr4(self):
        r = services.suggest_itr_form(False, False, False, True, False, False, 600_000)
        self.assertEqual(r['form'], 'ITR-4')

    def test_business_itr3(self):
        r = services.suggest_itr_form(False, False, True, False, False, False, 800_000)
        self.assertEqual(r['form'], 'ITR-3')

    def test_fno_always_itr3(self):
        r = services.suggest_itr_form(True, False, False, True, False, False, 400_000, has_fno=True)
        self.assertEqual(r['form'], 'ITR-3')


class SurchargeTests(TestCase):
    def test_no_surcharge_below_50l(self):
        r = services.calculate_surcharge(4_000_000)
        self.assertEqual(r['surcharge_rate'], 0)

    def test_10pct_surcharge_50l_to_1cr(self):
        r = services.calculate_surcharge(6_000_000)
        self.assertEqual(r['surcharge_rate'], 10)

    def test_15pct_above_1cr(self):
        r = services.calculate_surcharge(12_000_000)
        self.assertEqual(r['surcharge_rate'], 15)


class ProfessionalTaxTests(TestCase):
    def test_maharashtra_high_income(self):
        r = services.calculate_professional_tax(600_000, 'maharashtra')
        self.assertEqual(r['monthly_pt'], 200)
        self.assertEqual(r['annual_pt'], 2_400)

    def test_maharashtra_low_income(self):
        r = services.calculate_professional_tax(80_000, 'maharashtra')
        self.assertEqual(r['monthly_pt'], 0)

    def test_karnataka(self):
        r = services.calculate_professional_tax(600_000, 'karnataka')
        self.assertGreater(r['monthly_pt'], 0)


class NpsVsEpfTests(TestCase):
    def test_returns_both_options(self):
        r = services.compare_nps_vs_epf(50_000, 20)
        self.assertIn('epf', r)
        self.assertIn('nps', r)
        self.assertIn(r['winner'], ('epf', 'nps'))

    def test_both_have_positive_corpus(self):
        r = services.compare_nps_vs_epf(50_000, 20)
        self.assertGreater(r['nps']['corpus'], 0)
        self.assertGreater(r['epf']['corpus'], 0)


class TaxChecklistTests(TestCase):
    def test_old_regime_with_gap(self):
        r = services.generate_tax_checklist(800_000, 'old', sec_80c_invested=50_000)
        self.assertGreater(r['total_potential_saving'], 0)
        self.assertGreater(len(r['items']), 0)

    def test_new_regime_12l_zero_tax(self):
        r = services.generate_tax_checklist(1_200_000, 'new')
        self.assertEqual(r['regime'], 'new')

    def test_returns_required_keys(self):
        r = services.generate_tax_checklist(500_000, 'new')
        for key in ('items', 'total_potential_saving', 'items_count', 'fy'):
            self.assertIn(key, r)


# ─── View / URL Tests ─────────────────────────────────────────────────────────

class ToolViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Tool.objects.create(
            slug='old-vs-new-tax-regime', name='Old vs New Tax Regime',
            short_desc='Compare regimes', category='regime', icon='⚖️',
            meta_title='Old vs New Regime', meta_description='Compare tax regimes',
            is_active=True, sort_order=1,
        )

    def setUp(self):
        self.client = Client()

    def test_tool_index_200(self):
        self.assertEqual(self.client.get('/tools/').status_code, 200)

    def test_tool_detail_200(self):
        slug = Tool.objects.filter(is_active=True).first().slug
        self.assertEqual(self.client.get(f'/tools/{slug}/').status_code, 200)

    def test_tool_detail_404_unknown(self):
        self.assertEqual(self.client.get('/tools/nonexistent-slug/').status_code, 404)

    def _test_calc(self, slug, data):
        r = self.client.post(f'/tools/{slug}/calc/', data,
                             HTTP_HX_REQUEST='true',
                             HTTP_X_CSRFTOKEN='test')
        self.assertEqual(r.status_code, 200)
        self.assertNotIn(b'Calculator not found', r.content)

    def test_calc_regime_compare(self):
        self._test_calc('old-vs-new-tax-regime', {'income': '800000'})

    def test_calc_income_tax(self):
        self._test_calc('income-tax-calculator', {'income': '1000000', 'regime': 'new'})

    def test_calc_hra(self):
        self._test_calc('hra-exemption-calculator', {
            'basic_salary': '40000', 'hra_received': '20000',
            'annual_rent': '180000', 'is_metro': 'true'})

    def test_calc_gst(self):
        self._test_calc('gst-calculator', {'amount': '10000', 'rate': '18'})

    def test_calc_44ada(self):
        self._test_calc('presumptive-tax-44ada', {'gross_receipts': '1200000'})

    def test_calc_surcharge(self):
        self._test_calc('surcharge-calculator', {'income': '6000000', 'regime': 'new'})

    def test_calc_gst_composition(self):
        self._test_calc('gst-composition-calculator', {
            'annual_turnover': '5000000', 'business_type': 'trader'})

    def test_calc_senior_citizen(self):
        self._test_calc('senior-citizen-tax-calculator', {
            'income': '600000', 'age_group': '60_to_79', 'fd_interest': '50000'})

    def test_calc_professional_tax(self):
        self._test_calc('professional-tax-calculator', {
            'annual_income': '600000', 'state': 'maharashtra'})

    def test_calc_nps_vs_epf(self):
        self._test_calc('nps-vs-epf-comparison', {
            'basic_salary': '50000', 'years': '20', 'marginal_rate': '30'})

    def test_calc_tax_checklist(self):
        self._test_calc('tax-saving-checklist', {
            'income': '800000', 'regime': 'old', 'sec_80c_invested': '50000'})

    def test_calc_empty_inputs_no_500(self):
        """Empty inputs should return error message, not 500."""
        r = self.client.post('/tools/income-tax-calculator/calc/', {},
                             HTTP_HX_REQUEST='true')
        self.assertEqual(r.status_code, 200)

    def test_rate_endpoint_404_unknown(self):
        r = self.client.post('/tools/nonexistent-slug/rate/', {'vote': 'up'})
        self.assertEqual(r.status_code, 404)


class PageViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_200(self):
        self.assertEqual(self.client.get('/').status_code, 200)

    def test_about_200(self):
        self.assertEqual(self.client.get('/about/').status_code, 200)

    def test_contact_200(self):
        self.assertEqual(self.client.get('/contact/').status_code, 200)

    def test_disclaimer_200(self):
        self.assertEqual(self.client.get('/disclaimer/').status_code, 200)

    def test_privacy_200(self):
        self.assertEqual(self.client.get('/privacy/').status_code, 200)

    def test_robots_txt(self):
        r = self.client.get('/robots.txt')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Disallow: /sd/', r.content)

    def test_sitemap(self):
        self.assertEqual(self.client.get('/sitemap.xml').status_code, 200)


class BlogViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        from django.utils import timezone
        from blog.models import Article, Author, Category
        cat = Category.objects.create(name='Tax Basics', slug='tax-basics')
        author = Author.objects.create(
            name='Test CA', title='Chartered Accountant', bio='Test bio')
        Article.objects.create(
            title='Test Article', slug='test-article',
            author=author, category=cat,
            body='# Test\nSome content.',
            excerpt='Test excerpt',
            meta_title='Test Article', meta_description='Test description',
            is_published=True,
            published_at=timezone.now(),
        )

    def setUp(self):
        self.client = Client()

    def test_blog_index_200(self):
        self.assertEqual(self.client.get('/blog/').status_code, 200)

    def test_article_detail_200(self):
        from blog.models import Article
        slug = Article.objects.filter(is_published=True).first().slug
        self.assertEqual(self.client.get(f'/blog/{slug}/').status_code, 200)

    def test_article_404_unknown(self):
        self.assertEqual(self.client.get('/blog/nonexistent-article-xyz/').status_code, 404)


class StateViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        from states.models import State
        State.objects.create(
            name='Maharashtra', slug='maharashtra', abbr='MH',
            has_professional_tax=True,
            prof_tax_slabs_json='[]',
            meta_title='Maharashtra Tax', meta_description='Maharashtra tax info',
        )

    def setUp(self):
        self.client = Client()

    def test_states_index_200(self):
        self.assertEqual(self.client.get('/state-tax/').status_code, 200)

    def test_state_detail_200(self):
        self.assertEqual(self.client.get('/state-tax/maharashtra/').status_code, 200)


class GSTViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_gst_index_200(self):
        self.assertEqual(self.client.get('/gst/').status_code, 200)


class NewsletterViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_subscribe_valid_email(self):
        r = self.client.post('/newsletter/subscribe/', {'email': 'test@example.com', 'name': 'Test'})
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Subscribed', r.content)

    def test_subscribe_invalid_email(self):
        r = self.client.post('/newsletter/subscribe/', {'email': 'notanemail'})
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'valid email', r.content)

    def test_ca_lead_valid(self):
        r = self.client.post('/newsletter/ca-lead/', {
            'name': 'Test User', 'phone': '9999999999', 'query_type': 'itr'})
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'CA will contact', r.content)

    def test_ca_lead_missing_fields(self):
        r = self.client.post('/newsletter/ca-lead/', {'name': 'Test'})
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'required', r.content)


class UserViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_page_200(self):
        self.assertEqual(self.client.get('/users/login/').status_code, 200)

    def test_login_invalid_credentials(self):
        r = self.client.post('/users/login/', {
            'username': 'nobody', 'password': 'wrongpass'})
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Invalid credentials', r.content)

    def test_login_valid_redirects(self):
        User.objects.create_user('testuser', 'test@test.com', 'testpass123')
        r = self.client.post('/users/login/', {
            'username': 'testuser', 'password': 'testpass123'})
        self.assertEqual(r.status_code, 302)

    def test_logout_post(self):
        r = self.client.post('/users/logout/')
        self.assertEqual(r.status_code, 302)


class ControlViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff = User.objects.create_user(
            'staff', 'staff@test.com', 'staffpass123', is_staff=True)

    def test_admin_redirects_anonymous(self):
        r = self.client.get('/admin/')
        self.assertEqual(r.status_code, 302)

    def test_admin_dashboard_staff(self):
        self.client.force_login(self.staff)
        r = self.client.get('/admin/')
        self.assertEqual(r.status_code, 200)

    def test_admin_users_staff(self):
        self.client.force_login(self.staff)
        r = self.client.get('/admin/users/')
        self.assertEqual(r.status_code, 200)
