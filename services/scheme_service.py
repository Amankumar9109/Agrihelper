import os
import json
import logging
from datetime import datetime, timedelta
from extensions import db
from models.scheme import GovernmentScheme

logger = logging.getLogger(__name__)

# Canonical Official Schemes Data
CORE_SCHEMES_CATALOG = [
    {
        "code": "PM-KISAN",
        "name": "Pradhan Mantri Kisan Samman Nidhi (PM-KISAN)",
        "category": "Financial Aid",
        "tagline": "Direct income support of ₹6,000 per year directly to farmer bank accounts in three equal 4-monthly installments.",
        "description": "PM-KISAN is a Central Sector Scheme with 100% funding from Government of India. It provides income support to all landholding farmer families across the country to enable them to take care of agricultural expenses as well as domestic needs.",
        "benefits": "₹6,000 per year transferred directly to bank accounts via DBT in three equal installments of ₹2,000 every 4 months (April-July, August-November, December-March).",
        "eligibility": "All landholding farmer families having cultivable landholding in their names. Subject to exclusion criteria: institutional landholders, farmer families holding constitutional posts, serving/retired government employees, and income-tax payers in last assessment year.",
        "documents_required": "Aadhaar Card, Land ownership papers (Khata/Khasra/ROR), Active Bank Account linked with Aadhaar, Active Mobile number.",
        "how_to_apply": "1. Visit the official portal pmkisan.gov.in and click on 'New Farmer Registration'.\n2. Enter Aadhaar number, state, district, and captcha.\n3. Fill in land record details and bank account info.\n4. You can also apply via Common Service Centers (CSC) or local Patwari/State Nodal Officer.",
        "official_url": "https://pmkisan.gov.in/",
        "nodal_ministry": "Ministry of Agriculture & Farmers Welfare",
        "badge": "Direct DBT",
        "legacy_route": "policy.p1"
    },
    {
        "code": "PMFBY",
        "name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "category": "Crop Insurance",
        "tagline": "Comprehensive crop insurance cover from pre-sowing to post-harvest against natural calamities, pests, and diseases.",
        "description": "PMFBY provides comprehensive crop risk insurance cover against non-preventable natural risks at an extremely affordable premium rate for farmers (1.5% for Rabi, 2% for Kharif, 5% for annual commercial/horticultural crops), with the remaining subsidy borne equally by Central and State Governments.",
        "benefits": "Financial support to farmers suffering crop loss or damage arising out of unforeseen events (drought, flood, unseasonal rain, pest outbreak, localized hailstorm, post-harvest cyclonic damage). Claim settlement credited directly to Aadhaar-seeded accounts.",
        "eligibility": "All farmers including sharecroppers and tenant farmers growing notified insurable crops in notified areas are eligible.",
        "documents_required": "Land Possession Certificate (LPC) or tenancy agreement, Sowing Certificate/declaration, Bank passbook copy, Aadhaar card.",
        "how_to_apply": "1. Apply online at pmfby.gov.in through the Farmer Corner.\n2. Or apply through commercial/cooperative banks where you hold your crop loan.\n3. Or visit nearest Common Service Center (CSC) or insurance agent before the cut-off date.",
        "official_url": "https://pmfby.gov.in/",
        "nodal_ministry": "Ministry of Agriculture & Farmers Welfare",
        "badge": "Subsidized Premium",
        "legacy_route": "policy.p2"
    },
    {
        "code": "SHC",
        "name": "Soil Health Card Scheme (SHC)",
        "category": "Inputs & Testing",
        "tagline": "Periodic soil nutrient report providing crop-wise balanced fertilizer dosages to lower input cost and restore soil fertility.",
        "description": "The Soil Health Card Scheme promotes soil testing and judicious use of nutrients. Each card carries the nutrient status of 12 parameters: Macro-nutrients (N, P, K), Secondary nutrients (S), Micro-nutrients (Zn, Fe, Cu, Mn, Bo), and Physical parameters (pH, EC, Organic Carbon).",
        "benefits": "Free soil nutrient analysis card issued every 3 years. Helps farmers reduce unnecessary fertilizer expenditure by up to 15-20% while increasing crop yield by 10-15%.",
        "eligibility": "All farmers across all States and Union Territories of India are eligible.",
        "documents_required": "Farm location details (Khasra number), Aadhaar Card, Mobile number.",
        "how_to_apply": "1. Soil samples are collected by the State Agriculture Department / Krishi Vigyan Kendra (KVK) staff from a grid.\n2. Farmers can also submit their own soil samples to the nearest testing lab.\n3. Download card online at soilhealth.dac.gov.in using state, district, and farmer name.",
        "official_url": "https://soilhealth.dac.gov.in/",
        "nodal_ministry": "Ministry of Agriculture & Farmers Welfare",
        "badge": "Free Testing",
        "legacy_route": "policy.p3"
    },
    {
        "code": "eNAM",
        "name": "National Agriculture Market (e-NAM)",
        "category": "Market Access",
        "tagline": "Pan-India electronic trading portal uniting 1,360+ wholesale APMC mandis to facilitate better price discovery.",
        "description": "e-NAM is an online trading platform for agricultural commodities across India. It networks existing APMC mandis to create a unified national market, enabling farmers to showcase produce to buyers across India and receive instant online payments directly into their bank accounts.",
        "benefits": "Transparent auction process, online weighing, automated assaying quality reports, freedom from local middleman cartels, and direct e-payment into bank account within 24 hours of sale.",
        "eligibility": "Any farmer, FPO (Farmer Producer Organization), trader, or commission agent registered with an e-NAM integrated APMC mandi.",
        "documents_required": "Aadhaar Card, Bank passbook copy, APMC registration / mandi gate pass entry.",
        "how_to_apply": "1. Register at enam.gov.in under 'Registration' as a Farmer or FPO.\n2. Bring agricultural produce to the nearest e-NAM enabled APMC yard.\n3. Get produce weighed and assayed for quality.\n4. Bid will be conducted electronically and proceeds sent to your bank account.",
        "official_url": "https://enam.gov.in/",
        "nodal_ministry": "Ministry of Agriculture & Farmers Welfare",
        "badge": "National Mandi",
        "legacy_route": "policy.p4"
    },
    {
        "code": "KCC",
        "name": "Kisan Credit Card (KCC)",
        "category": "Credit & Loans",
        "tagline": "Timely short-term agricultural credit up to ₹3 Lakh at an effective interest rate of only 4% per annum.",
        "description": "KCC provides farmers with timely credit for agricultural operations, post-harvest expenses, farm asset maintenance, and allied activities (dairy, poultry, fisheries). Includes ₹3 Lakh limit with Interest Subvention (2%) and Prompt Repayment Incentive (3%), resulting in a net 4% interest rate.",
        "benefits": "Revolving credit limit valid for 5 years with annual review. ATM-cum-debit card issued. Collateral-free loan up to ₹1.60 Lakh. Built-in personal accident insurance up to ₹50,000.",
        "eligibility": "All farmers, individual/joint borrowers, tenant farmers, oral lessees, sharecroppers, and Self-Help Groups (SHGs) of farmers. Now also extended to Animal Husbandry and Fisheries.",
        "documents_required": "Duly completed application form, Proof of identity (Aadhaar/Voter ID), Land record documents certified by revenue authority, Crop cultivation certificate.",
        "how_to_apply": "1. Download the one-page simplified KCC form from agricoop.nic.in or commercial bank websites.\n2. Submit to your local commercial, cooperative, or Regional Rural Bank (RRB) branch.\n3. Banks are mandated to issue KCC within 14 days of receiving completed application.",
        "official_url": "https://www.myscheme.gov.in/schemes/kcc",
        "nodal_ministry": "Ministry of Agriculture & Farmers Welfare / RBI / NABARD",
        "badge": "4% Low Interest",
        "legacy_route": "policy.p5"
    },
    {
        "code": "PM-KUSUM",
        "name": "Pradhan Mantri Kisan Urja Suraksha evam Utthaan Mahabhiyan (PM-KUSUM)",
        "category": "Irrigation & Solar",
        "tagline": "Up to 60% government subsidy to install standalone off-grid solar agricultural pumps and solarize existing grid-connected tube wells.",
        "description": "PM-KUSUM provides energy security to farmers by subsidizing off-grid solar water pumping systems (3 HP to 10 HP) and supporting solar power plants on barren farm lands, enabling farmers to earn additional income by selling surplus solar electricity to DISCOMs.",
        "benefits": "60% direct capital subsidy (30% Central Govt + 30% State Govt). The farmer only pays 10% upfront cost, and the remaining 30% can be financed via bank loan. Eliminates diesel pump fuel expenses completely.",
        "eligibility": "Individual farmers, groups of farmers, cooperatives, panchayats, Farmer Producer Organisations (FPOs) and Water User Associations (WUAs).",
        "documents_required": "Aadhaar Card, Land ownership papers, Bank passbook, Electricity connection details (if solarizing existing pump).",
        "how_to_apply": "1. Apply online via your State Renewable Energy Development Agency portal (e.g., MEDA in Maharashtra, UPNEDA in UP, GUVNL in Gujarat).\n2. Upload land and bank records.\n3. Inspect site and deposit farmer contribution to receive solar pump setup.",
        "official_url": "https://pmkusum.mnre.gov.in/",
        "nodal_ministry": "Ministry of New and Renewable Energy",
        "badge": "60% Subsidy",
        "legacy_route": None
    },
    {
        "code": "PMKSY",
        "name": "Pradhan Mantri Krishi Sinchayee Yojana (PMKSY - Per Drop More Crop)",
        "category": "Irrigation & Solar",
        "tagline": "45% to 55% financial assistance on installing precision micro-irrigation (Drip & Sprinkler systems).",
        "description": "PMKSY focuses on expanding cultivable area under assured irrigation, improving on-farm water use efficiency through micro-irrigation systems (Per Drop More Crop), promoting precision water technologies, and groundwater recharge.",
        "benefits": "Financial subsidy of 55% for Small & Marginal farmers and 45% for Other farmers for setting up Drip Irrigation and Sprinkler systems. Saves 40-50% water while increasing crop yield by 20-30%.",
        "eligibility": "All landholding farmers having an assured source of water on their farm.",
        "documents_required": "Aadhaar Card, Land record copy (7/12 extract / Khata), Water source certificate, Bank details.",
        "how_to_apply": "1. Apply via the State Horticulture or Agriculture portal (e.g., Mahadbt in Maharashtra, DBT Agriculture Bihar).\n2. Select registered micro-irrigation vendor.\n3. Subsidy is disbursed directly to beneficiary account after field inspection.",
        "official_url": "https://pmksy.gov.in/",
        "nodal_ministry": "Ministry of Agriculture & Farmers Welfare",
        "badge": "55% Water Subsidy",
        "legacy_route": None
    },
    {
        "code": "PKVY",
        "name": "Paramparagat Krishi Vikas Yojana (PKVY)",
        "category": "Organic Farming",
        "tagline": "₹50,000 per hectare financial aid for adopting traditional chemical-free organic farming in clusters.",
        "description": "PKVY promotes organic farming through a cluster-based approach and Participatory Guarantee System (PGS) certification. It provides support from soil building, bio-fertilizer inputs, and certification to post-harvest branding and marketing.",
        "benefits": "Financial assistance of ₹50,000 per hectare over 3 years. Out of this, ₹31,000/ha is directly provided for organic inputs (seeds, bio-fertilizers, vermicompost), and ₹8,800/ha for value addition and packaging.",
        "eligibility": "Farmers forming a cluster of minimum 20 hectares or 50 farmers committing to complete chemical-free organic cultivation.",
        "documents_required": "Aadhaar Card, Land ownership document, Cluster membership declaration, Bank account details.",
        "how_to_apply": "1. Contact the local District Agricultural Officer (DAO) or Krishi Vigyan Kendra.\n2. Form or join an existing organic farming cluster in your village/panchayat.\n3. Register on the Jaivik Kheti portal (jaivikkheti.in).",
        "official_url": "https://pgsindia-ncof.gov.in/",
        "nodal_ministry": "Ministry of Agriculture & Farmers Welfare",
        "badge": "₹50,000/Ha Aid",
        "legacy_route": None
    },
    {
        "code": "SMAM",
        "name": "Sub-Mission on Agricultural Mechanization (SMAM)",
        "category": "Inputs & Testing",
        "tagline": "40% to 50% subsidy on modern farm machinery, tractors, rotavators, and custom hiring centers.",
        "description": "SMAM aims to increase the reach of farm mechanization to small and marginal farmers and regions where power availability is low, by providing subsidies for individual machinery purchase and setting up Custom Hiring Centers (CHCs).",
        "benefits": "40% to 50% subsidy for individual small/marginal/SC/ST/women farmers for purchasing tractors, power tillers, rotavators, seed drills, and sprayers. Up to ₹10 Lakh subsidy (40%) to establish a Custom Hiring Center.",
        "eligibility": "All farmers across India. Special preference and higher subsidy percentage given to small/marginal farmers and women farmers.",
        "documents_required": "Aadhaar Card, Land document, Caste certificate (if applicable), Bank passbook, Quotation from authorized dealer.",
        "how_to_apply": "1. Register on the mechanized DBT portal (agrimachinery.nic.in).\n2. Select required farm equipment and authorized dealer.\n3. Upload documents and track subsidy sanction status online.",
        "official_url": "https://agrimachinery.nic.in/",
        "nodal_ministry": "Ministry of Agriculture & Farmers Welfare",
        "badge": "Up to 50% Subsidy",
        "legacy_route": None
    },
    {
        "code": "AIF",
        "name": "Agriculture Infrastructure Fund (AIF)",
        "category": "Credit & Loans",
        "tagline": "3% interest subvention and credit guarantee on medium-to-long term loans up to ₹2 Crore for post-harvest farm infrastructure.",
        "description": "AIF provides a medium-long term debt financing facility for post-harvest management infrastructure and community farming assets like warehouses, cold storages, sorting/grading units, and primary processing centers.",
        "benefits": "3% per annum interest subvention for loans up to ₹2 Crore for a maximum tenure of 7 years. Credit guarantee coverage under CGTMSE for loans up to ₹2 Crore without demanding collateral.",
        "eligibility": "Farmers, FPOs, PACS, Agri-entrepreneurs, Startups, and Central/State agencies.",
        "documents_required": "Detailed Project Report (DPR), Land title/lease agreement, KYC documents, Bank loan application.",
        "how_to_apply": "1. Apply directly through the AIF portal (agriinfra.dac.gov.in).\n2. Select your preferred lending bank and submit your DPR online.\n3. Ministry and bank process the application within 45 days.",
        "official_url": "https://agriinfra.dac.gov.in/",
        "nodal_ministry": "Ministry of Agriculture & Farmers Welfare",
        "badge": "3% Subvention",
        "legacy_route": None
    },
    {
        "code": "MIDH",
        "name": "Mission for Integrated Development of Horticulture (MIDH)",
        "category": "Inputs & Testing",
        "tagline": "Holistic financial assistance for polyhouse farming, fruit orchards, nurseries, shade net houses, and post-harvest cold chains.",
        "description": "MIDH is a centrally sponsored scheme for the holistic growth of the horticulture sector covering fruits, vegetables, root & tuber crops, mushrooms, spices, flowers, aromatic plants, coconut, cashew, and cocoa.",
        "benefits": "Up to 50% subsidy for constructing protected cultivation structures (polyhouses, green houses, shade net houses), setting up high-tech nurseries, and planting elite fruit cultivars.",
        "eligibility": "Farmers, growers' associations, FPOs, self-help groups, and agricultural entrepreneurs.",
        "documents_required": "Land record extract, Project estimate from certified architect/engineer, Soil and water test reports, Aadhaar and bank details.",
        "how_to_apply": "1. Submit application to District Horticulture Officer (DHO) or State Horticulture Mission portal.\n2. Obtain administrative approval before beginning polyhouse/nursery construction.",
        "official_url": "https://midh.gov.in/",
        "nodal_ministry": "Ministry of Agriculture & Farmers Welfare",
        "badge": "High Subsidy",
        "legacy_route": None
    },
    {
        "code": "AHIDF",
        "name": "Animal Husbandry Infrastructure Development Fund (AHIDF)",
        "category": "Credit & Loans",
        "tagline": "Incentivizing dairy processing, meat processing, animal feed plants, and cattle breed multiplication farms.",
        "description": "AHIDF aims to incentivize investments by individual entrepreneurs, private companies, MSMEs, Farmers Producer Organizations (FPOs) and Section 8 companies to establish dairy processing, meat processing, and animal feed plants.",
        "benefits": "3% interest subvention for up to 8 years. Credit guarantee up to 25% of the total credit facility provided through NABARD.",
        "eligibility": "Farmers, Dairy Cooperatives, FPOs, MSMEs, and Private Agricultural Enterprises.",
        "documents_required": "Detailed Project Report, Land documents, Company/FPO registration, Bank details, Environmental clearances.",
        "how_to_apply": "1. Register and submit application on the AHIDF portal (ahidf.udyamimitra.in).\n2. Selected lending institutions review and sanction subsidized credit facility.",
        "official_url": "https://ahidf.udyamimitra.in/",
        "nodal_ministry": "Ministry of Fisheries, Animal Husbandry and Dairying",
        "badge": "Dairy & Livestock",
        "legacy_route": None
    }
]

def sync_schemes_cache(force=False):
    """
    Synchronizes the government schemes database table.
    Seeds if empty or if last update is > 24 hours old or force=True.
    """
    total = GovernmentScheme.query.count()
    if total > 0 and not force:
        latest = GovernmentScheme.query.order_by(GovernmentScheme.last_updated.desc()).first()
        if latest and (datetime.utcnow() - latest.last_updated) < timedelta(hours=24):
            return total

    # Seed or update schemes
    upserted = 0
    for data in CORE_SCHEMES_CATALOG:
        scheme = GovernmentScheme.query.filter_by(code=data['code']).first()
        if not scheme:
            scheme = GovernmentScheme(
                code=data['code'],
                name=data['name'],
                category=data['category'],
                tagline=data.get('tagline'),
                description=data['description'],
                benefits=data['benefits'],
                eligibility=data['eligibility'],
                documents_required=data.get('documents_required'),
                how_to_apply=data['how_to_apply'],
                official_url=data['official_url'],
                nodal_ministry=data.get('nodal_ministry', 'Ministry of Agriculture'),
                badge=data.get('badge'),
                legacy_route=data.get('legacy_route'),
                is_active=True,
                last_updated=datetime.utcnow()
            )
            db.session.add(scheme)
            upserted += 1
        else:
            # Update existing attributes
            scheme.name = data['name']
            scheme.category = data['category']
            scheme.tagline = data.get('tagline')
            scheme.description = data['description']
            scheme.benefits = data['benefits']
            scheme.eligibility = data['eligibility']
            scheme.documents_required = data.get('documents_required')
            scheme.how_to_apply = data['how_to_apply']
            scheme.official_url = data['official_url']
            scheme.nodal_ministry = data.get('nodal_ministry')
            scheme.badge = data.get('badge')
            scheme.legacy_route = data.get('legacy_route')
            scheme.last_updated = datetime.utcnow()
            upserted += 1

    db.session.commit()
    logger.info(f"Synchronized {upserted} government schemes in database.")
    return GovernmentScheme.query.count()

def get_all_schemes(category=None, search=None):
    """
    Retrieves schemes from database with optional category filtering and search term.
    """
    sync_schemes_cache() # Ensure fresh cache
    query = GovernmentScheme.query.filter_by(is_active=True)

    if category and category.strip() and category.strip().lower() != 'all':
        query = query.filter(GovernmentScheme.category.ilike(f"%{category.strip()}%"))

    if search and search.strip():
        term = f"%{search.strip()}%"
        query = query.filter(
            db.or_(
                GovernmentScheme.name.ilike(term),
                GovernmentScheme.code.ilike(term),
                GovernmentScheme.description.ilike(term),
                GovernmentScheme.benefits.ilike(term),
                GovernmentScheme.tagline.ilike(term)
            )
        )

    return query.order_by(GovernmentScheme.id.asc()).all()

def get_scheme_by_id(scheme_id):
    sync_schemes_cache()
    return GovernmentScheme.query.get(scheme_id)

def get_scheme_by_code(code):
    sync_schemes_cache()
    return GovernmentScheme.query.filter_by(code=code.strip()).first()

def evaluate_eligibility(land_size, farm_type, primary_need):
    """
    Rule-based eligibility recommendation engine for farmers:
    - land_size: 'marginal' (<1 ha), 'small' (1-2 ha), 'medium_large' (>2 ha)
    - farm_type: 'crops', 'horticulture', 'organic', 'dairy'
    - primary_need: 'cash', 'insurance', 'solar_pump', 'irrigation', 'machinery', 'credit', 'market'
    """
    sync_schemes_cache()
    all_schemes = GovernmentScheme.query.filter_by(is_active=True).all()
    results = []

    for s in all_schemes:
        match_score = 0
        reasons = []

        # Category & Need Matching
        if primary_need == 'cash' and s.code == 'PM-KISAN':
            match_score += 95
            reasons.append("Provides ₹6,000/year direct cash transfer for cultivating farmers.")
        elif primary_need == 'insurance' and s.code == 'PMFBY':
            match_score += 95
            reasons.append("Guarantees low-cost comprehensive crop insurance protection.")
        elif primary_need == 'solar_pump' and s.code == 'PM-KUSUM':
            match_score += 95
            reasons.append("Offers 60% direct subsidy on solar irrigation water pump setups.")
        elif primary_need == 'irrigation' and s.code in ['PMKSY', 'PM-KUSUM']:
            match_score += 90
            reasons.append("Provides 55% subsidy for installing drip and sprinkler irrigation.")
        elif primary_need == 'machinery' and s.code == 'SMAM':
            match_score += 90
            reasons.append("Offers 40-50% subsidy on tractors and farm implements.")
        elif primary_need == 'credit' and s.code in ['KCC', 'AIF', 'AHIDF']:
            match_score += 90
            reasons.append("Provides subsidized credit up to ₹3 Lakh at just 4% interest rate.")
        elif primary_need == 'market' and s.code == 'eNAM':
            match_score += 90
            reasons.append("Connects you to nationwide buyers across 1,360+ mandis.")

        # Farm Type Matching
        if farm_type == 'organic' and s.code == 'PKVY':
            match_score += 90
            reasons.append("Directly tailored for organic farmers with ₹50,000/Ha financial aid.")
        elif farm_type == 'horticulture' and s.code == 'MIDH':
            match_score += 90
            reasons.append("Specialized subsidy for polyhouses, fruit orchards, and vegetable shade nets.")
        elif farm_type == 'dairy' and s.code == 'AHIDF':
            match_score += 90
            reasons.append("Specifically finances dairy cattle, feed units, and milk processing.")

        # Universal small/marginal farmer boost
        if land_size in ['marginal', 'small']:
            if s.code in ['PM-KISAN', 'PMKSY', 'SMAM', 'KCC', 'SHC']:
                match_score += 20
                reasons.append("Priority eligibility and maximum subsidy tier reserved for small/marginal farmers.")

        if match_score > 0:
            results.append({
                'scheme': s.to_dict(),
                'match_score': min(100, match_score),
                'reasons': reasons
            })

    results.sort(key=lambda x: x['match_score'], reverse=True)
    return results
