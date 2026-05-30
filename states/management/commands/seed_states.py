import json
from django.core.management.base import BaseCommand
from states.models import State

# PT slabs: list of {"up_to": monthly_income_limit_or_null, "monthly_tax": amount}
# up_to=null means "above previous limit"

STATES = [
    {
        'name': 'Andhra Pradesh', 'slug': 'andhra-pradesh', 'abbr': 'AP',
        'gst_state_code': '37', 'has_professional_tax': True,
        'prof_tax_slabs_json': json.dumps([
            {'up_to': 15000, 'monthly_tax': 0},
            {'up_to': 20000, 'monthly_tax': 150},
            {'up_to': None, 'monthly_tax': 200},
        ]),
        'special_notes': 'Andhra Pradesh levies professional tax on salaried individuals and self-employed professionals. Maximum PT is ₹2,400 per year.',
        'meta_title': 'Andhra Pradesh Income Tax & Professional Tax FY 2025-26',
        'meta_description': 'Income tax guide and professional tax slabs for Andhra Pradesh FY 2025-26. Max PT ₹2,400/year. Free tax calculator.',
    },
    {
        'name': 'Arunachal Pradesh', 'slug': 'arunachal-pradesh', 'abbr': 'AR',
        'gst_state_code': '12', 'has_professional_tax': False,
        'prof_tax_slabs_json': json.dumps([]),
        'special_notes': 'Arunachal Pradesh does not levy professional tax on individuals.',
        'meta_title': 'Arunachal Pradesh Income Tax Guide FY 2025-26',
        'meta_description': 'Income tax guide for Arunachal Pradesh FY 2025-26. No professional tax. Free income tax calculator.',
    },
    {
        'name': 'Assam', 'slug': 'assam', 'abbr': 'AS',
        'gst_state_code': '18', 'has_professional_tax': True,
        'prof_tax_slabs_json': json.dumps([
            {'up_to': 10000, 'monthly_tax': 0},
            {'up_to': 15000, 'monthly_tax': 150},
            {'up_to': None, 'monthly_tax': 208},
        ]),
        'special_notes': 'Assam levies professional tax. Maximum annual PT is ₹2,500.',
        'meta_title': 'Assam Income Tax & Professional Tax FY 2025-26',
        'meta_description': 'Income tax guide and professional tax slabs for Assam FY 2025-26. Max PT ₹2,500/year. Free calculator.',
    },
    {
        'name': 'Bihar', 'slug': 'bihar', 'abbr': 'BR',
        'gst_state_code': '10', 'has_professional_tax': False,
        'prof_tax_slabs_json': json.dumps([]),
        'special_notes': 'Bihar does not levy professional tax on individuals.',
        'meta_title': 'Bihar Income Tax Guide FY 2025-26',
        'meta_description': 'Income tax guide for Bihar FY 2025-26. No professional tax. Use free income tax calculator.',
    },
    {
        'name': 'Chhattisgarh', 'slug': 'chhattisgarh', 'abbr': 'CG',
        'gst_state_code': '22', 'has_professional_tax': True,
        'prof_tax_slabs_json': json.dumps([
            {'up_to': 15000, 'monthly_tax': 0},
            {'up_to': 25000, 'monthly_tax': 150},
            {'up_to': None, 'monthly_tax': 200},
        ]),
        'special_notes': 'Chhattisgarh levies professional tax up to ₹2,400 per year.',
        'meta_title': 'Chhattisgarh Income Tax & Professional Tax FY 2025-26',
        'meta_description': 'Income tax guide and professional tax slabs for Chhattisgarh FY 2025-26. Max PT ₹2,400/year.',
    },
    {
        'name': 'Delhi', 'slug': 'delhi', 'abbr': 'DL',
        'gst_state_code': '07', 'has_professional_tax': False,
        'prof_tax_slabs_json': json.dumps([]),
        'special_notes': 'Delhi (NCT) does not levy professional tax. Income tax is governed by the central government.',
        'meta_title': 'Delhi Income Tax Calculator FY 2025-26 — Free',
        'meta_description': 'Income tax guide for Delhi FY 2025-26. No professional tax in Delhi. Free income tax calculator for Delhi residents.',
    },
    {
        'name': 'Goa', 'slug': 'goa', 'abbr': 'GA',
        'gst_state_code': '30', 'has_professional_tax': True,
        'prof_tax_slabs_json': json.dumps([
            {'up_to': 15000, 'monthly_tax': 0},
            {'up_to': 25000, 'monthly_tax': 150},
            {'up_to': None, 'monthly_tax': 200},
        ]),
        'special_notes': 'Goa levies professional tax. Maximum annual professional tax is ₹2,400.',
        'meta_title': 'Goa Income Tax & Professional Tax FY 2025-26',
        'meta_description': 'Income tax guide and professional tax slabs for Goa FY 2025-26. Max PT ₹2,400/year. Free tax calculator.',
    },
    {
        'name': 'Gujarat', 'slug': 'gujarat', 'abbr': 'GJ',
        'gst_state_code': '24', 'has_professional_tax': True,
        'prof_tax_slabs_json': json.dumps([
            {'up_to': 5999, 'monthly_tax': 0},
            {'up_to': 8999, 'monthly_tax': 80},
            {'up_to': 11999, 'monthly_tax': 150},
            {'up_to': None, 'monthly_tax': 200},
        ]),
        'special_notes': 'Gujarat levies professional tax with income-linked slabs. Maximum annual PT is ₹2,400.',
        'meta_title': 'Gujarat Income Tax & Professional Tax FY 2025-26',
        'meta_description': 'Professional tax slabs for Gujarat FY 2025-26. ₹80–₹200/month based on salary. Income tax calculator for Gujarat.',
    },
    {
        'name': 'Haryana', 'slug': 'haryana', 'abbr': 'HR',
        'gst_state_code': '06', 'has_professional_tax': False,
        'prof_tax_slabs_json': json.dumps([]),
        'special_notes': 'Haryana does not levy professional tax on individuals.',
        'meta_title': 'Haryana Income Tax Guide FY 2025-26',
        'meta_description': 'Income tax guide for Haryana FY 2025-26. No professional tax. Free income tax calculator for Haryana residents.',
    },
    {
        'name': 'Himachal Pradesh', 'slug': 'himachal-pradesh', 'abbr': 'HP',
        'gst_state_code': '02', 'has_professional_tax': False,
        'prof_tax_slabs_json': json.dumps([]),
        'special_notes': 'Himachal Pradesh does not levy professional tax.',
        'meta_title': 'Himachal Pradesh Income Tax Guide FY 2025-26',
        'meta_description': 'Income tax guide for Himachal Pradesh FY 2025-26. No professional tax. Free income tax calculator.',
    },
    {
        'name': 'Jharkhand', 'slug': 'jharkhand', 'abbr': 'JH',
        'gst_state_code': '20', 'has_professional_tax': True,
        'prof_tax_slabs_json': json.dumps([
            {'up_to': 25000, 'monthly_tax': 0},
            {'up_to': None, 'monthly_tax': 100},
        ]),
        'special_notes': 'Jharkhand levies professional tax at ₹100/month for income above ₹25,000/month.',
        'meta_title': 'Jharkhand Income Tax & Professional Tax FY 2025-26',
        'meta_description': 'Income tax guide and professional tax for Jharkhand FY 2025-26. ₹100/month PT above ₹25K salary.',
    },
    {
        'name': 'Karnataka', 'slug': 'karnataka', 'abbr': 'KA',
        'gst_state_code': '29', 'has_professional_tax': True,
        'prof_tax_slabs_json': json.dumps([
            {'up_to': 14999, 'monthly_tax': 0},
            {'up_to': 29999, 'monthly_tax': 150},
            {'up_to': None, 'monthly_tax': 200},
        ]),
        'special_notes': 'Karnataka has one of India\'s highest professional tax rates. ₹200/month (₹300 in February) for income above ₹30,000/month. Employers must deduct and remit PT.',
        'meta_title': 'Karnataka Income Tax & Professional Tax FY 2025-26',
        'meta_description': 'Professional tax in Karnataka: ₹200/month for salary above ₹30K. Income tax calculator for Bangalore and Karnataka residents.',
    },
    {
        'name': 'Kerala', 'slug': 'kerala', 'abbr': 'KL',
        'gst_state_code': '32', 'has_professional_tax': True,
        'prof_tax_slabs_json': json.dumps([
            {'up_to': 11999, 'monthly_tax': 0},
            {'up_to': 17999, 'monthly_tax': 120},
            {'up_to': 29999, 'monthly_tax': 180},
            {'up_to': None, 'monthly_tax': 208},
        ]),
        'special_notes': 'Kerala levies professional tax. Maximum annual PT is ₹2,496.',
        'meta_title': 'Kerala Income Tax & Professional Tax FY 2025-26',
        'meta_description': 'Professional tax slabs for Kerala FY 2025-26. Max ₹2,496/year. Income tax calculator for Kerala residents.',
    },
    {
        'name': 'Madhya Pradesh', 'slug': 'madhya-pradesh', 'abbr': 'MP',
        'gst_state_code': '23', 'has_professional_tax': True,
        'prof_tax_slabs_json': json.dumps([
            {'up_to': 18750, 'monthly_tax': 0},
            {'up_to': None, 'monthly_tax': 208},
        ]),
        'special_notes': 'Madhya Pradesh levies professional tax at ₹208/month for income above ₹18,750/month.',
        'meta_title': 'Madhya Pradesh Income Tax & Professional Tax FY 2025-26',
        'meta_description': 'Professional tax in Madhya Pradesh: ₹208/month above ₹18,750 salary. Income tax calculator for MP residents.',
    },
    {
        'name': 'Maharashtra', 'slug': 'maharashtra', 'abbr': 'MH',
        'gst_state_code': '27', 'has_professional_tax': True,
        'prof_tax_slabs_json': json.dumps([
            {'up_to': 7500, 'monthly_tax': 0},
            {'up_to': 10000, 'monthly_tax': 175},
            {'up_to': None, 'monthly_tax': 200},
        ]),
        'special_notes': 'Maharashtra professional tax: ₹175/month for ₹7,500–₹10,000 and ₹200/month above ₹10,000 (₹300 in February). Annual max ₹2,500.',
        'meta_title': 'Maharashtra Income Tax & Professional Tax FY 2025-26',
        'meta_description': 'Professional tax in Maharashtra: ₹200/month for salary above ₹10K. ₹300 in February. Income tax calculator for Mumbai, Pune.',
    },
    {
        'name': 'Manipur', 'slug': 'manipur', 'abbr': 'MN',
        'gst_state_code': '14', 'has_professional_tax': True,
        'prof_tax_slabs_json': json.dumps([
            {'up_to': 5000, 'monthly_tax': 0},
            {'up_to': 7500, 'monthly_tax': 50},
            {'up_to': None, 'monthly_tax': 100},
        ]),
        'special_notes': 'Manipur levies professional tax. Maximum annual PT is ₹1,200.',
        'meta_title': 'Manipur Income Tax & Professional Tax FY 2025-26',
        'meta_description': 'Income tax guide and professional tax for Manipur FY 2025-26. Max PT ₹1,200/year.',
    },
    {
        'name': 'Meghalaya', 'slug': 'meghalaya', 'abbr': 'ML',
        'gst_state_code': '17', 'has_professional_tax': True,
        'prof_tax_slabs_json': json.dumps([
            {'up_to': 4999, 'monthly_tax': 0},
            {'up_to': 7499, 'monthly_tax': 58},
            {'up_to': 9999, 'monthly_tax': 83},
            {'up_to': None, 'monthly_tax': 208},
        ]),
        'special_notes': 'Meghalaya levies professional tax on salaried individuals.',
        'meta_title': 'Meghalaya Income Tax & Professional Tax FY 2025-26',
        'meta_description': 'Income tax guide and professional tax slabs for Meghalaya FY 2025-26. Free tax calculator.',
    },
    {
        'name': 'Mizoram', 'slug': 'mizoram', 'abbr': 'MZ',
        'gst_state_code': '15', 'has_professional_tax': True,
        'prof_tax_slabs_json': json.dumps([
            {'up_to': 5000, 'monthly_tax': 0},
            {'up_to': 8333, 'monthly_tax': 75},
            {'up_to': None, 'monthly_tax': 208},
        ]),
        'special_notes': 'Mizoram levies professional tax on salaried and self-employed individuals.',
        'meta_title': 'Mizoram Income Tax & Professional Tax FY 2025-26',
        'meta_description': 'Income tax guide and professional tax for Mizoram FY 2025-26. Free income tax calculator.',
    },
    {
        'name': 'Nagaland', 'slug': 'nagaland', 'abbr': 'NL',
        'gst_state_code': '13', 'has_professional_tax': True,
        'prof_tax_slabs_json': json.dumps([
            {'up_to': 5000, 'monthly_tax': 0},
            {'up_to': 10000, 'monthly_tax': 75},
            {'up_to': None, 'monthly_tax': 208},
        ]),
        'special_notes': 'Nagaland levies professional tax on salaried individuals.',
        'meta_title': 'Nagaland Income Tax & Professional Tax FY 2025-26',
        'meta_description': 'Income tax guide and professional tax for Nagaland FY 2025-26.',
    },
    {
        'name': 'Odisha', 'slug': 'odisha', 'abbr': 'OD',
        'gst_state_code': '21', 'has_professional_tax': True,
        'prof_tax_slabs_json': json.dumps([
            {'up_to': 13304, 'monthly_tax': 0},
            {'up_to': 25000, 'monthly_tax': 125},
            {'up_to': None, 'monthly_tax': 200},
        ]),
        'special_notes': 'Odisha levies professional tax. Maximum annual PT is ₹2,400.',
        'meta_title': 'Odisha Income Tax & Professional Tax FY 2025-26',
        'meta_description': 'Professional tax slabs for Odisha FY 2025-26. Max ₹2,400/year. Income tax calculator for Odisha residents.',
    },
    {
        'name': 'Punjab', 'slug': 'punjab', 'abbr': 'PB',
        'gst_state_code': '03', 'has_professional_tax': False,
        'prof_tax_slabs_json': json.dumps([]),
        'special_notes': 'Punjab does not levy professional tax on individuals.',
        'meta_title': 'Punjab Income Tax Guide FY 2025-26',
        'meta_description': 'Income tax guide for Punjab FY 2025-26. No professional tax. Free income tax calculator for Punjab residents.',
    },
    {
        'name': 'Rajasthan', 'slug': 'rajasthan', 'abbr': 'RJ',
        'gst_state_code': '08', 'has_professional_tax': False,
        'prof_tax_slabs_json': json.dumps([]),
        'special_notes': 'Rajasthan abolished professional tax in 2006 and does not levy it currently.',
        'meta_title': 'Rajasthan Income Tax Guide FY 2025-26',
        'meta_description': 'Income tax guide for Rajasthan FY 2025-26. No professional tax. Free income tax calculator for Jaipur and Rajasthan.',
    },
    {
        'name': 'Sikkim', 'slug': 'sikkim', 'abbr': 'SK',
        'gst_state_code': '11', 'has_professional_tax': True,
        'prof_tax_slabs_json': json.dumps([
            {'up_to': 20000, 'monthly_tax': 0},
            {'up_to': 30000, 'monthly_tax': 125},
            {'up_to': None, 'monthly_tax': 208},
        ]),
        'special_notes': 'Sikkim levies professional tax. Note: Old settlers/Sikkimese domicile residents have special income tax exemptions under Section 10(26AAA).',
        'meta_title': 'Sikkim Income Tax & Professional Tax FY 2025-26',
        'meta_description': 'Income tax and professional tax guide for Sikkim FY 2025-26. Special exemption under Sec 10(26AAA) for Sikkim domicile.',
    },
    {
        'name': 'Tamil Nadu', 'slug': 'tamil-nadu', 'abbr': 'TN',
        'gst_state_code': '33', 'has_professional_tax': True,
        'prof_tax_slabs_json': json.dumps([
            {'up_to': 21000, 'monthly_tax': 0},
            {'up_to': 30000, 'monthly_tax': 135},
            {'up_to': 45000, 'monthly_tax': 315},
            {'up_to': 60000, 'monthly_tax': 690},
            {'up_to': 75000, 'monthly_tax': 1025},
            {'up_to': None, 'monthly_tax': 1250},
        ]),
        'special_notes': 'Tamil Nadu has higher professional tax rates compared to most states. Maximum annual PT is ₹2,500.',
        'meta_title': 'Tamil Nadu Income Tax & Professional Tax FY 2025-26',
        'meta_description': 'Professional tax slabs for Tamil Nadu FY 2025-26. Higher rates: up to ₹1,250/month. Income tax calculator for Chennai and TN.',
    },
    {
        'name': 'Telangana', 'slug': 'telangana', 'abbr': 'TG',
        'gst_state_code': '36', 'has_professional_tax': True,
        'prof_tax_slabs_json': json.dumps([
            {'up_to': 15000, 'monthly_tax': 0},
            {'up_to': 20000, 'monthly_tax': 150},
            {'up_to': None, 'monthly_tax': 200},
        ]),
        'special_notes': 'Telangana levies professional tax. Maximum annual PT is ₹2,400.',
        'meta_title': 'Telangana Income Tax & Professional Tax FY 2025-26',
        'meta_description': 'Professional tax in Telangana: ₹200/month for salary above ₹20K. Income tax calculator for Hyderabad and Telangana.',
    },
    {
        'name': 'Tripura', 'slug': 'tripura', 'abbr': 'TR',
        'gst_state_code': '16', 'has_professional_tax': True,
        'prof_tax_slabs_json': json.dumps([
            {'up_to': 7500, 'monthly_tax': 0},
            {'up_to': 15000, 'monthly_tax': 150},
            {'up_to': None, 'monthly_tax': 208},
        ]),
        'special_notes': 'Tripura levies professional tax on salaried individuals.',
        'meta_title': 'Tripura Income Tax & Professional Tax FY 2025-26',
        'meta_description': 'Income tax guide and professional tax slabs for Tripura FY 2025-26.',
    },
    {
        'name': 'Uttar Pradesh', 'slug': 'uttar-pradesh', 'abbr': 'UP',
        'gst_state_code': '09', 'has_professional_tax': False,
        'prof_tax_slabs_json': json.dumps([]),
        'special_notes': 'Uttar Pradesh does not levy professional tax on individuals.',
        'meta_title': 'Uttar Pradesh Income Tax Guide FY 2025-26',
        'meta_description': 'Income tax guide for Uttar Pradesh FY 2025-26. No professional tax. Free income tax calculator for UP residents.',
    },
    {
        'name': 'Uttarakhand', 'slug': 'uttarakhand', 'abbr': 'UK',
        'gst_state_code': '05', 'has_professional_tax': True,
        'prof_tax_slabs_json': json.dumps([
            {'up_to': 15000, 'monthly_tax': 0},
            {'up_to': 25000, 'monthly_tax': 100},
            {'up_to': None, 'monthly_tax': 200},
        ]),
        'special_notes': 'Uttarakhand levies professional tax. Maximum annual PT is ₹2,400.',
        'meta_title': 'Uttarakhand Income Tax & Professional Tax FY 2025-26',
        'meta_description': 'Professional tax in Uttarakhand FY 2025-26. Max ₹2,400/year. Income tax calculator for Uttarakhand residents.',
    },
    {
        'name': 'West Bengal', 'slug': 'west-bengal', 'abbr': 'WB',
        'gst_state_code': '19', 'has_professional_tax': True,
        'prof_tax_slabs_json': json.dumps([
            {'up_to': 10000, 'monthly_tax': 0},
            {'up_to': 15000, 'monthly_tax': 110},
            {'up_to': 25000, 'monthly_tax': 130},
            {'up_to': 40000, 'monthly_tax': 150},
            {'up_to': None, 'monthly_tax': 200},
        ]),
        'special_notes': 'West Bengal levies professional tax. Kolkata residents pay up to ₹200/month. Maximum annual PT is ₹2,400.',
        'meta_title': 'West Bengal Income Tax & Professional Tax FY 2025-26',
        'meta_description': 'Professional tax slabs for West Bengal FY 2025-26. Up to ₹200/month. Income tax calculator for Kolkata and WB residents.',
    },
]


class Command(BaseCommand):
    help = 'Seed 28 Indian state tax pages'

    def handle(self, *args, **options):
        self.stdout.write('Seeding states...')
        created = 0
        for data in STATES:
            obj, c = State.objects.get_or_create(slug=data['slug'], defaults=data)
            if not c:
                for k, v in data.items():
                    setattr(obj, k, v)
                obj.save()
            self.stdout.write(f'  {obj.name} ({"created" if c else "updated"})')
            if c:
                created += 1
        self.stdout.write(self.style.SUCCESS(
            f'\nDone. {created} created, {State.objects.count()} total states.'
        ))
