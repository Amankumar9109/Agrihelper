"""
AgriHelper - Modern Farming Techniques Catalog & Service
Provides curated agricultural technique profiles, ROI & subsidy calculations,
and integrations with Schemes and Agri Store products.
"""

TECHNIQUES_CATALOG = [
    {
        "id": 1,
        "slug": "drip-irrigation",
        "legacy_slug": "drip_irrigation",
        "title": "Precision Drip Irrigation",
        "legacy_title": "Drip Irrigation",
        "category": "Water Management",
        "badge": "Save 50-70% Water",
        "icon": "fa-faucet-drip",
        "tagline": "Direct root-zone micro-irrigation with fertigation capability for optimal crop yield and water conservation.",
        "overview": "Drip irrigation is a precision micro-irrigation system that delivers water and dissolved nutrients directly to the root zone of plants through an engineered network of valves, mainline pipes, lateral tubings, and calibrated drippers/emitters. By eliminating surface runoff and deep percolation, it dramatically reduces water consumption while keeping soil moisture continuously at field capacity.",
        "how_it_works": "Water from a tube-well or farm pond is pumped through a filtration unit (disc/screen filter) to prevent emitter clogging. Soluble fertilizers from a Venturi injector tank mix into the stream (fertigation). The pressured water flows through sub-mains into UV-stabilized inline or online lateral pipes laid along crop rows, slowly dripping water directly at plant roots at rates of 1.2 to 4.0 liters per hour.",
        "key_benefits": [
            "Reduces farm water consumption by 50% to 70% compared to traditional flood irrigation",
            "Increases crop yield by 25% to 60% due to consistent moisture and targeted aeration",
            "Saves 30% to 40% on fertilizers through precision fertigation with zero runoff",
            "Suppresses weed growth by keeping inter-row furrow areas completely dry",
            "Operates efficiently on undulating, hilly, or irregularly shaped terrain without land leveling"
        ],
        "implementation_steps": [
            "Conduct water quality and soil texture analysis to check salinity and filtration requirements.",
            "Design lateral spacing and dripper discharge rates based on crop row geometry (e.g. 1.2m x 0.6m for vegetables).",
            "Install head unit consisting of pump, hydrocyclone filter, disc filter, pressure gauge, and Venturi injector.",
            "Lay PVC main and sub-main trenches at 1.5 to 2.0 feet depth, connecting flush valves at terminal ends.",
            "Roll out 16mm or 12mm lateral tubes and install start connectors and end caps.",
            "Perform trial pressure test at 1.0 to 1.5 kg/cm² and flush lateral lines before first crop planting."
        ],
        "suitable_crops": ["Sugarcane", "Cotton", "Banana", "Pomegranate", "Grapes", "Tomato", "Chilli", "Capsicum", "Potato", "Citrus"],
        "estimated_cost_per_acre": "₹35,000 - ₹55,000",
        "base_cost_numeric": 45000,
        "subsidy_scheme": "PM Krishi Sinchayee Yojana (PMKSY - Per Drop More Crop)",
        "subsidy_code": "PMKSY",
        "subsidy_percentage": "45% - 55%",
        "subsidy_percent_numeric": 55,
        "water_savings": "50% - 70%",
        "yield_boost": "+30% to +50%",
        "roi_payback": "12 to 18 months",
        "image_url": "https://images.unsplash.com/photo-1563514227147-6d2ff665a6a0?w=1200&auto=format&fit=crop&q=80",
        "related_products": ["irri-001", "fert-002", "tool-002"],
        "related_schemes": ["PMKSY", "SHC"]
    },
    {
        "id": 2,
        "slug": "soil-health",
        "legacy_slug": "soil_health",
        "title": "Soil Health & Precision Testing",
        "legacy_title": "Soil Health",
        "category": "Soil & Nutrition",
        "badge": "Cut Fertilizer Waste by 25%",
        "icon": "fa-vial-virus",
        "tagline": "Smart digital sensing, pH calibration, and scientific NPK nutrient balancing to rejuvenate soil ecology.",
        "overview": "Soil Health Monitoring integrates digital IoT probes, rapid colorimetric testing, and the Government Soil Health Card portal to assess the exact chemical, biological, and physical parameters of farm soil. Rather than applying uniform blanket fertilizer doses, farmers supply tailored macronutrients (N, P, K) and critical micronutrients (Zinc, Boron, Iron) tailored to specific crop demands.",
        "how_it_works": "Soil samples are collected across a zig-zag grid from 0-15 cm plow depth. Portable 4-in-1 digital meters assess soil pH, electro-conductivity (EC), moisture, and temperature on-site. Detailed lab or mobile assay measures available Nitrogen, Phosphorus, Potassium, Organic Carbon (SOC), and micronutrients. The resulting data generates crop-specific nutrient replenishment charts.",
        "key_benefits": [
            "Prevents soil acidification, sodicity, and salinity buildup from indiscriminate chemical use",
            "Reduces unnecessary fertilizer expenditure by up to ₹2,500 - ₹4,000 per acre per season",
            "Prevents micronutrient deficiency diseases like Khaira in rice and hollow heart in vegetables",
            "Improves Soil Organic Carbon (SOC) and beneficial microbial biomass when paired with compost",
            "Enhances root depth penetration and drought resilience during dry spells"
        ],
        "implementation_steps": [
            "Collect 8-10 composite soil cores from a representative 1-acre field avoiding bunds and manure pits.",
            "Dry soil in shade, pulverize with wooden mallet, and pass through 2mm brass sieve.",
            "Use digital tester or submit sample to nearest Krishi Vigyan Kendra (KVK) or testing lab.",
            "Calibrate soil pH: apply agricultural lime (calcium carbonate) if pH < 6.0; apply gypsum if pH > 8.0.",
            "Incorporate 4-5 tonnes of decomposed farmyard manure or vermicompost to elevate SOC above 0.75%.",
            "Apply basal fertilizers as recommended by the Soil Health Card before sowing or transplanting."
        ],
        "suitable_crops": ["Wheat", "Paddy / Rice", "Maize", "Pulses (Chickpea, Arhar)", "Oilseeds (Mustard, Groundnut)", "Vegetables"],
        "estimated_cost_per_acre": "₹500 - ₹1,500",
        "base_cost_numeric": 1200,
        "subsidy_scheme": "Soil Health Card Scheme (SHC)",
        "subsidy_code": "SHC",
        "subsidy_percentage": "100% Free Soil Card",
        "subsidy_percent_numeric": 100,
        "water_savings": "15% - 20%",
        "yield_boost": "+15% to +25%",
        "roi_payback": "Immediate (First Season)",
        "image_url": "https://images.unsplash.com/photo-1585314062340-f1a5a7c9328d?w=1200&auto=format&fit=crop&q=80",
        "related_products": ["tool-002", "fert-001", "fert-003"],
        "related_schemes": ["SHC", "PKVY"]
    },
    {
        "id": 3,
        "slug": "vertical-farming",
        "legacy_slug": "vertical_farming",
        "title": "Vertical Farming & Controlled Environments",
        "legacy_title": "Vertical Farming",
        "category": "Protected Cultivation",
        "badge": "10x Yield / sq.m",
        "icon": "fa-layer-group",
        "tagline": "Multi-tier stacked indoor cultivation using artificial LED spectra and climate automation.",
        "overview": "Vertical farming is the practice of producing food in vertically stacked layers, integrated structures, or vertical inclined surfaces in climate-controlled indoor facilities. By utilizing controlled environment agriculture (CEA) technology, crops are shielded from adverse climate shocks, pests, and droughts, yielding 10 to 20 times more produce per square foot than traditional horizontal farms.",
        "how_it_works": "Plants are supported in modular food-grade vertical towers or tiered A-frame racks using recirculating hydroponic or aeroponic nutrient feeds. Specialized full-spectrum LED fixtures supply Photosynthetically Active Radiation (PAR) with tuned red (660nm) and blue (450nm) wavelengths. Automated HVAC systems regulate indoor temperature (20-24°C), humidity (60-70%), and elevated CO₂ levels (800-1200 ppm).",
        "key_benefits": [
            "Maximizes space efficiency with 90% less land requirement compared to conventional farming",
            "Conserves up to 95% water via closed-loop moisture condensation and nutrient recycling",
            "Enables 365-day continuous harvesting unaffected by monsoon delays, hail, or heatwaves",
            "Completely eliminates the need for chemical pesticides and synthetic soil fumigants",
            "Enables hyper-local urban farming, cutting food miles, transit spoilage, and carbon emissions"
        ],
        "implementation_steps": [
            "Select an insulated shed, warehouse, or greenhouse facility with reliable 3-phase power supply.",
            "Install multi-tiered galvanized racking systems with food-grade PVC/food-safe gutters.",
            "Mount horticultural LED grow lights providing 250-300 µmol/m²/s Photosynthetic Photon Flux Density.",
            "Connect automated nutrient dosing system with continuous EC and pH monitoring probes.",
            "Install dehumidifier, evaporative cooling pads, and exhaust ventilation for vapor deficit management.",
            "Sow certified disease-free microgreen, lettuce, or herb seeds in sterile rockwool or coco plugs."
        ],
        "suitable_crops": ["Butterhead Lettuce", "Spinach", "Kale", "Arugula", "Exotic Basil", "Strawberries", "Rosemary", "Microgreens"],
        "estimated_cost_per_acre": "₹15,00,000 - ₹35,00,000 (Facility Setup)",
        "base_cost_numeric": 1500000,
        "subsidy_scheme": "Mission for Integrated Development of Horticulture (MIDH)",
        "subsidy_code": "MIDH",
        "subsidy_percentage": "35% - 50%",
        "subsidy_percent_numeric": 40,
        "water_savings": "90% - 95%",
        "yield_boost": "+500% to +1000% (per area)",
        "roi_payback": "2.5 to 3.5 years",
        "image_url": "https://images.unsplash.com/photo-1586771107445-d3ca888129ff?w=1200&auto=format&fit=crop&q=80",
        "related_products": ["seed-003", "fert-002", "tool-002"],
        "related_schemes": ["MIDH", "PMKSY"]
    },
    {
        "id": 4,
        "slug": "drones-agriculture",
        "legacy_slug": "drones_agriculture",
        "title": "Agricultural Drones & Precision Spraying",
        "legacy_title": "Drones Agriculture",
        "category": "Precision Tech",
        "badge": "10x Faster Spraying",
        "icon": "fa-plane-up",
        "tagline": "Aerial UAV crop monitoring, multispectral NDVI stress mapping, and ultra-low-volume chemical spraying.",
        "overview": "Agricultural drones (Kisan Drones) combine unmanned aerial vehicles with RTK precision GPS, multispectral imaging cameras, and intelligent centrifugal spray nozzles. Drones can cover an entire acre in just 6 to 10 minutes with surgical precision, reducing farmer chemical exposure while delivering deep canopy droplet penetration through downward rotor downdraft.",
        "how_it_works": "The pilot creates an autonomous flight boundary via mission planner app on an Android controller. The drone takes off autonomously with a 10L to 20L tank, flying 2 to 3 meters above the crop canopy. Micron-sized droplets (120-250 microns) are driven deep into both upper and lower leaf surfaces by propeller vortex winds, providing superior coverage with 90% less water.",
        "key_benefits": [
            "Sprays 1 acre in only 7-10 minutes versus 4-5 hours required by manual knapsack sprayers",
            "Cuts water carrier volume from 200 liters/acre down to just 10-15 liters/acre (90% water saving)",
            "Reduces agrochemical wastage and drift by 25% through calibrated droplet spectrums",
            "Eliminates direct human inhalation and dermal contact with hazardous chemical sprays",
            "Multispectral cameras detect pest attacks, fungal rust, and moisture stress days before visible to eye"
        ],
        "implementation_steps": [
            "Obtain DGCA Remote Pilot Certificate (RPC) and register drone with Unique Identification Number (UIN).",
            "Survey field perimeter, noting trees, high-tension electrical cables, and wind barriers.",
            "Dilute bio-pesticide or micronutrient foliar spray according to recommended Ultra-Low Volume (ULV) ratios.",
            "Calibrate flow sensor, radar terrain-following sensor, and obstacle avoidance LIDAR.",
            "Execute automated waypoint route in calm wind conditions (<12 km/h), preferably early morning or late evening.",
            "Rinse tank and atomizers with clean water immediately after flight completion."
        ],
        "suitable_crops": ["Paddy / Rice", "Wheat", "Cotton", "Sugarcane", "Soybean", "Groundnut", "Mustard", "Apple & Mango Orchards"],
        "estimated_cost_per_acre": "₹350 - ₹500 / acre (Custom Hiring) or ₹4.5L - ₹7.5L (Purchase)",
        "base_cost_numeric": 450000,
        "subsidy_scheme": "Sub-Mission on Agricultural Mechanization (SMAM Kisan Drone)",
        "subsidy_code": "SMAM",
        "subsidy_percentage": "40% to 100% (FPOs & Custom Hiring)",
        "subsidy_percent_numeric": 50,
        "water_savings": "85% - 90%",
        "yield_boost": "+15% to +25%",
        "roi_payback": "12 to 14 months (Custom Hiring Service)",
        "image_url": "https://images.unsplash.com/photo-1508614589041-895b88991e3e?w=1200&auto=format&fit=crop&q=80",
        "related_products": ["tool-001", "prot-001", "prot-002"],
        "related_schemes": ["SMAM", "PMFBY"]
    },
    {
        "id": 5,
        "slug": "hydroponics",
        "legacy_slug": "hydroponics",
        "title": "Hydroponics & Soilless Cultivation",
        "legacy_title": "Hydroponics",
        "category": "Protected Cultivation",
        "badge": "Zero Soil Diseases",
        "icon": "fa-flask-vial",
        "tagline": "Growing nutrient-dense vegetables in recirculating water solutions without soil.",
        "overview": "Hydroponics is the science of cultivating plants without natural soil, using mineral nutrient solutions dissolved in water. Plant roots are either suspended directly in an oxygenated nutrient bath or supported by an inert substrate such as coco peat, perlite, expanded clay pebbles, or rockwool. Because plants do not expend energy searching for nutrients in compact dirt, vegetative growth is 30% to 50% faster.",
        "how_it_works": "In a closed-loop Nutrient Film Technique (NFT) or Dutch Bucket channel, nutrient-rich water flows over plant roots around the clock. Submersible aeration pumps inject dissolved oxygen (>6 mg/L). Electronic sensors monitor Electrical Conductivity (1.4 - 2.4 mS/cm) and pH (5.6 - 6.4), automatically replenishing pure mineral salts when readings drop.",
        "key_benefits": [
            "Complete exemption from soil-borne pathogens like nematodes, Fusarium wilt, and damping-off",
            "Saves up to 90% water by constantly filtering and recirculating nutrient drainage",
            "Accelerates crop turnaround time by 30-40%, allowing 8 to 12 harvests per year",
            "Produces cleaner, pesticide-free vegetables that fetch 2x-3x price premiums in urban markets",
            "Can be set up on non-arable lands, rooftops, barren rocky patches, or degraded plots"
        ],
        "implementation_steps": [
            "Construct a polyhouse structure with 40-mesh insect-proof netting and UV-stabilized polythene.",
            "Assemble food-grade PVC NFT gullies with slope gradient of 1:30 to 1:40 for gravity drain.",
            "Fill master sump reservoir with RO or filtered water (<150 ppm TDS) and add hydroponic stock solutions (A & B).",
            "Insert germinated seedlings from rockwool plug trays into 2-inch net cups with clay pebbles.",
            "Maintain circulation pump timer: 15 minutes ON / 15 minutes OFF during daylight hours.",
            "Perform daily checks on water EC and pH; dump and refresh nutrient water every 14 to 21 days."
        ],
        "suitable_crops": ["Cherry Tomatoes", "English Cucumber", "Bell Peppers (Colored Capsicum)", "Lettuce", "Bok Choy", "Celery", "Mint", "Strawberries"],
        "estimated_cost_per_acre": "₹12,00,000 - ₹22,00,000 (Commercial Polyhouse Unit)",
        "base_cost_numeric": 1200000,
        "subsidy_scheme": "National Horticulture Mission (NHM) & State Polyhouse Subsidy",
        "subsidy_code": "NHM",
        "subsidy_percentage": "50% of capital project cost",
        "subsidy_percent_numeric": 50,
        "water_savings": "85% - 90%",
        "yield_boost": "+40% to +80%",
        "roi_payback": "2.0 to 3.0 years",
        "image_url": "https://images.unsplash.com/photo-1558449028-b53a39d100fc?w=1200&auto=format&fit=crop&q=80",
        "related_products": ["fert-002", "seed-003", "tool-002"],
        "related_schemes": ["MIDH", "PMKSY"]
    },
    {
        "id": 6,
        "slug": "ai-data-analytics",
        "legacy_slug": "ai_data_analytics",
        "title": "AI & Crop Data Analytics",
        "legacy_title": "AI & Data Analytics",
        "category": "AI & Automation",
        "badge": "Predictive Smart Farming",
        "icon": "fa-robot",
        "tagline": "Machine learning, satellite NDVI telemetry, and automated pest identification for precision decisions.",
        "overview": "AI and Agricultural Big Data transform farming from subjective guesswork into an exact, data-driven science. By fusing hyper-local weather models, multispectral satellite observations (Sentinel-2, Landsat), and on-field IoT moisture probes, AI algorithms forecast pest outbreaks, pinpoint optimum irrigation schedules, and model expected crop yields with high confidence.",
        "how_it_works": "A deep convolutional neural network (CNN) trained on millions of crop disease images identifies foliar pathology from a standard smartphone camera photograph in under 2 seconds. Simultaneously, satellite Normalized Difference Vegetation Index (NDVI) time-series data tracks chlorophyll vigor across individual survey plots, alerting farmers to emerging stress hotspots days before foliage yellows.",
        "key_benefits": [
            "Early warning systems detect pest attacks and fungal infections before widespread contagion",
            "Eliminates excessive prophylactic spraying, saving up to 35% on chemical bills",
            "Optimizes sowing calendar by matching real-time soil temperature and monsoon onset dates",
            "Accurate yield tonnage modeling empowers farmers to negotiate better forward APMC mandi rates",
            "Integrates directly with RAG agricultural advisors (like KisanMitra) for personalized regional recommendations"
        ],
        "implementation_steps": [
            "Register farm geographic coordinates (latitude, longitude, survey number) on AgriHelper.",
            "Install smartphone diagnostic app or use AgriHelper's built-in KisanMitra AI assistant.",
            "Deploy solar-powered soil moisture and microclimate weather IoT nodes in representative plots.",
            "Upload weekly smartphone photos of crops during critical vegetative and flowering phases.",
            "Review automated NDVI vitality alerts and apply recommended biological interventions immediately.",
            "Track local mandi price forecasts to choose the highest-profit liquidation window."
        ],
        "suitable_crops": ["Cotton", "Paddy / Rice", "Wheat", "Soybean", "Maize", "Chilli", "Tomato", "Onion", "Potato"],
        "estimated_cost_per_acre": "₹0 - ₹2,500 / year (Software & IoT)",
        "base_cost_numeric": 1500,
        "subsidy_scheme": "Digital Agriculture Mission (AgriStack / IDEA)",
        "subsidy_code": "AGRISTACK",
        "subsidy_percentage": "Free Public Digital Infrastructure",
        "subsidy_percent_numeric": 100,
        "water_savings": "20% - 30%",
        "yield_boost": "+20% to +35%",
        "roi_payback": "Immediate (First Season)",
        "image_url": "https://images.unsplash.com/photo-1581092160607-ee22621dd758?w=1200&auto=format&fit=crop&q=80",
        "related_products": ["tool-002", "prot-002"],
        "related_schemes": ["eNAM", "PMFBY"]
    },
    {
        "id": 7,
        "slug": "solar-smart-farming",
        "legacy_slug": "solar_smart_farming",
        "title": "Solar-Powered Smart Agriculture",
        "legacy_title": "Solar Farming",
        "category": "Clean Energy",
        "badge": "Zero Diesel Bills",
        "icon": "fa-solar-panel",
        "tagline": "Clean off-grid solar water pumping, agri-photovoltaics, and automatic solenoid valve irrigation.",
        "overview": "Solar-powered smart agriculture liberates farmers from unpredictable rural electricity blackouts and surging diesel generator expenses. Utilizing high-efficiency monocrystalline solar arrays and smart Variable Frequency Drives (VFD), solar pump sets draw clean water whenever daylight is available. Dual-use Agri-PV systems even allow shade-tolerant crops to thrive directly underneath solar panels.",
        "how_it_works": "A 3HP, 5HP, or 7.5HP DC/AC submersible solar pump is connected to an array of photovoltaic modules through an intelligent inverter. When sunlight hits the panels, the VFD softly ramps pump speed to match solar irradiance. Automated timer valves distribute water through drip networks systematically without requiring manual field visits.",
        "key_benefits": [
            "Eliminates 100% of recurring diesel fuel costs (saving ₹30,000 - ₹70,000 per year)",
            "Guarantees reliable irrigation during daytime hours, ending dangerous night-time farm visits",
            "Enables surplus electricity sales back to the state power grid under the PM-KUSUM feeder solarization",
            "Cuts carbon emissions and prevents groundwater contamination from oil leaks",
            "Low maintenance lifespan exceeding 25 years with minimal moving components"
        ],
        "implementation_steps": [
            "Assess water depth, required daily discharge volume, and pump horsepower needed.",
            "Verify shadow-free land footprint (approx. 100 sq.ft per kW of solar capacity).",
            "Submit application online via state DISCOM portal under PM-KUSUM Component-B or C.",
            "Install galvanized steel ground mounting structure with manual seasonal tilt tracking.",
            "Install certified BIS-compliant solar modules, VFD solar controller, and DC disconnect switch.",
            "Connect automated float switch in overhead farm pond to automatically prevent dry runs."
        ],
        "suitable_crops": ["All field crops", "Orchards", "Pulses", "Sugarcane", "Wheat", "Mustard", "Fodder crops"],
        "estimated_cost_per_acre": "₹1,80,000 - ₹3,50,000 (Complete 3HP-5HP Solar Pump)",
        "base_cost_numeric": 220000,
        "subsidy_scheme": "PM-KUSUM Scheme (Component B & C)",
        "subsidy_code": "PM-KUSUM",
        "subsidy_percentage": "60% to 90% (Central + State Subsidy)",
        "subsidy_percent_numeric": 70,
        "water_savings": "30% - 40% (When paired with drip)",
        "yield_boost": "+25% to +35%",
        "roi_payback": "12 to 18 months",
        "image_url": "https://images.unsplash.com/photo-1509391365360-2e959784a276?w=1200&auto=format&fit=crop&q=80",
        "related_products": ["irri-001", "tool-002", "prot-002"],
        "related_schemes": ["PM-KUSUM", "PMKSY"]
    },
    {
        "id": 8,
        "slug": "greenhouse-polyhouse",
        "legacy_slug": "greenhouse_polyhouse",
        "title": "Protected Cultivation & Polyhouse",
        "legacy_title": "Polyhouse Farming",
        "category": "Protected Cultivation",
        "badge": "Off-Season Premium Prices",
        "icon": "fa-wheat-awn-circle-exclamation",
        "tagline": "Naturally ventilated polyhouses with shade nets and climate screening for high-value horticulture.",
        "overview": "Protected cultivation shields delicate horticultural crops from scorching summer sun, unseasonal hail, heavy monsoons, and pest swarms. UV-stabilized 200-micron polyethylene film creates a controlled microclimate, increasing humidity and maintaining ideal temperatures, allowing farmers to produce off-season vegetables and export-quality flowers at 3x market rates.",
        "how_it_works": "A curved galvanized steel structure is enveloped with UV-stabilized anti-fog, anti-drip plastic film. Top ridge vents and side rollup curtains provide natural thermo-siphon air exchange. Retractable aluminized thermal screens reflect excessive heat during midday, and motorized misting micro-foggers drop internal temperature by 4-6°C through evaporative cooling.",
        "key_benefits": [
            "Enables profitable off-season vegetable production when market prices are 200-300% higher",
            "Yields 4x to 8x higher volume per acre compared to open-field cultivation",
            "Protects completely from catastrophic hail storms, unseasonal rain, and blistering heatwaves",
            "Reduces chemical insecticide usage by 70% thanks to insect-proof perimeter mesh",
            "Produces uniform grade-A fruit and vegetable sizes demanded by retail chains and export buyers"
        ],
        "implementation_steps": [
            "Select well-drained fertile land with orientation keeping length in North-South direction.",
            "Erect GI pipe trellis framework (Class B pipes, minimum 4.5m center height).",
            "Fix 200-micron UV-stabilized polyethylene cladding using aluminum profile and spring wire.",
            "Install 40-mesh nylon insect nets on all side ventilation curtains.",
            "Lay internal drip irrigation with micro-mister foggers for relative humidity regulation.",
            "Prepare raised soil beds (1m width, 30cm height) enriched with sterilized coco peat and compost."
        ],
        "suitable_crops": ["Dutch Roses", "Carnations", "Gerbera", "Color Capsicum (Red & Yellow)", "Parthenocarpic Cucumber", "Cherry Tomatoes", "Muskmelon"],
        "estimated_cost_per_acre": "₹35,00,000 - ₹45,00,000 / acre (Naturally Ventilated)",
        "base_cost_numeric": 3800000,
        "subsidy_scheme": "Mission for Integrated Development of Horticulture (MIDH)",
        "subsidy_code": "MIDH",
        "subsidy_percentage": "50% of project cost (up to ₹40L)",
        "subsidy_percent_numeric": 50,
        "water_savings": "50% - 60%",
        "yield_boost": "+200% to +400%",
        "roi_payback": "2.0 to 3.0 years",
        "image_url": "https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=1200&auto=format&fit=crop&q=80",
        "related_products": ["seed-003", "irri-001", "fert-002"],
        "related_schemes": ["MIDH", "PMKSY"]
    },
    {
        "id": 9,
        "slug": "integrated-pest-management",
        "legacy_slug": "integrated_pest_management",
        "title": "Integrated Pest Management (IPM)",
        "legacy_title": "Integrated Pest Management",
        "category": "Soil & Nutrition",
        "badge": "Zero Chemical Residue",
        "icon": "fa-shield-halved",
        "tagline": "Combining bio-agents, pheromone lures, sticky traps, and neem extracts to control pests sustainably.",
        "overview": "Integrated Pest Management (IPM) is an environmentally sound strategy that manages agricultural pests, diseases, and weeds by combining biological control, crop rotation, pheromone monitoring, and botanical extracts. Rather than attempting total chemical eradication, IPM suppresses pest populations below the Economic Injury Level (EIL) while protecting pollinators and beneficial predatory insects.",
        "how_it_works": "Farmers deploy yellow and blue sticky traps (10-15 per acre) to monitor whiteflies, aphids, and thrips. Pheromone delta traps catch male bollworms and stem borers to disrupt reproductive cycles. Biological predators (Trichogramma wasps, Chrysoperla) and bio-fungicides (Trichoderma viride, Pseudomonas fluorescens) neutralize pathogens naturally. Botanical sprays like cold-pressed neem oil (10,000 ppm) repel caterpillars without harming honeybees.",
        "key_benefits": [
            "Prevents pests from developing chemical resistance and eliminates pest resurgence",
            "Ensures zero synthetic pesticide residue, meeting organic and export clearance standards",
            "Protects native pollinators (honeybees) and natural beneficial predators (ladybird beetles)",
            "Reduces farmer plant protection expenditure by 40% compared to chemical cocktails",
            "Guarantees safe working environment for farm families and farm laborers"
        ],
        "implementation_steps": [
            "Install 5-8 pheromone traps per acre to calculate daily insect trap count.",
            "Hang yellow sticky traps for sucking pests (aphids, whiteflies) and blue traps for thrips.",
            "Release Trichogramma egg parasitoid cards @ 50,000 eggs/acre at initial pest detection.",
            "Spray cold-pressed neem oil (5ml per liter) with mild soap emulsifier as preventive defense.",
            "Apply bio-agents like Beauveria bassiana or Bacillus thuringiensis (Bt) for chewing larvae.",
            "Reserve targeted low-toxicity synthetic chemicals only when pest count crosses Economic Threshold Level (ETL)."
        ],
        "suitable_crops": ["Cotton", "Paddy / Rice", "Tomato", "Brinjal", "Okra", "Pomegranate", "Mango", "Pulses"],
        "estimated_cost_per_acre": "₹1,200 - ₹2,500 / acre per season",
        "base_cost_numeric": 1800,
        "subsidy_scheme": "Paramparagat Krishi Vikas Yojana (PKVY)",
        "subsidy_code": "PKVY",
        "subsidy_percentage": "Financial aid up to ₹50,000 / hectare for 3 years",
        "subsidy_percent_numeric": 75,
        "water_savings": "10% - 15%",
        "yield_boost": "+15% to +20%",
        "roi_payback": "Immediate (First Season)",
        "image_url": "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=1200&auto=format&fit=crop&q=80",
        "related_products": ["prot-001", "prot-002", "fert-003"],
        "related_schemes": ["PKVY", "SHC"]
    }
]

CATEGORIES = [
    "All",
    "Water Management",
    "Precision Tech",
    "Protected Cultivation",
    "Soil & Nutrition",
    "AI & Automation",
    "Clean Energy"
]

def get_all_techniques(category="All", search=""):
    """Returns filtered techniques list based on category and search keyword."""
    results = TECHNIQUES_CATALOG
    if category and category != "All":
        results = [t for t in results if t.get("category") == category]
    if search:
        q = search.lower().strip()
        results = [
            t for t in results
            if q in t["title"].lower()
            or q in t["tagline"].lower()
            or q in t["overview"].lower()
            or any(q in crop.lower() for crop in t.get("suitable_crops", []))
            or q in t.get("category", "").lower()
        ]
    return results

def get_technique_by_slug(slug):
    """Fetches a technique by its canonical slug or legacy slug."""
    slug = slug.strip().lower()
    for t in TECHNIQUES_CATALOG:
        if t["slug"] == slug or t.get("legacy_slug") == slug:
            return t
        # Match normalized slug with hyphens or underscores
        if t["slug"].replace("-", "_") == slug.replace("-", "_"):
            return t
    return None

def get_technique_by_id(tech_id):
    """Fetches a technique by integer ID."""
    for t in TECHNIQUES_CATALOG:
        if t["id"] == tech_id:
            return t
    return None

def get_categories():
    """Returns all available technique categories."""
    return CATEGORIES

def calculate_technique_roi(technique_slug, farm_acres=1.0, crop_type="General"):
    """
    Computes real-time ROI, water savings, subsidy estimates, and net farmer profit
    based on farm land size, crop type, and selected technique.
    """
    technique = get_technique_by_slug(technique_slug)
    if not technique:
        technique = TECHNIQUES_CATALOG[0]

    acres = max(0.5, float(farm_acres))
    base_cost = technique["base_cost_numeric"] * acres
    subsidy_rate = technique["subsidy_percent_numeric"] / 100.0

    # Government subsidy capping logic
    estimated_subsidy = base_cost * subsidy_rate
    # Cap commercial polyhouse / vertical farming subsidy per scheme guidelines
    if technique["slug"] in ["vertical-farming", "greenhouse-polyhouse"]:
        estimated_subsidy = min(estimated_subsidy, 4000000.0)

    net_farmer_investment = max(0.0, base_cost - estimated_subsidy)

    # Water savings estimation (Litres per year)
    # Average baseline flood irrigation uses approx 4,000,000 L / acre / year
    baseline_water_use = 4000000 * acres
    if "drip" in technique["slug"]:
        water_saved_liters = baseline_water_use * 0.60
        annual_fertilizer_savings = 3500 * acres
        annual_electricity_savings = 4200 * acres
        yield_gain_percent = 35
    elif "hydroponic" in technique["slug"] or "vertical" in technique["slug"]:
        water_saved_liters = baseline_water_use * 0.88
        annual_fertilizer_savings = 5000 * acres
        annual_electricity_savings = 2000 * acres
        yield_gain_percent = 70
    elif "solar" in technique["slug"]:
        water_saved_liters = baseline_water_use * 0.35
        annual_fertilizer_savings = 1500 * acres
        annual_electricity_savings = 38000 * acres  # Eliminates diesel pump
        yield_gain_percent = 25
    elif "drone" in technique["slug"]:
        water_saved_liters = 180000 * acres
        annual_fertilizer_savings = 3200 * acres
        annual_electricity_savings = 1000 * acres
        yield_gain_percent = 20
    elif "soil" in technique["slug"] or "pest" in technique["slug"]:
        water_saved_liters = 400000 * acres
        annual_fertilizer_savings = 4500 * acres
        annual_electricity_savings = 1200 * acres
        yield_gain_percent = 22
    else:
        water_saved_liters = baseline_water_use * 0.25
        annual_fertilizer_savings = 2500 * acres
        annual_electricity_savings = 2000 * acres
        yield_gain_percent = 20

    # Estimated extra revenue based on crop
    crop_multipliers = {
        "Sugarcane": 45000,
        "Cotton": 32000,
        "Tomato": 65000,
        "Paddy / Rice": 28000,
        "Wheat": 24000,
        "Vegetables": 55000,
        "Fruits / Orchard": 75000
    }
    baseline_crop_revenue = crop_multipliers.get(crop_type, 40000) * acres
    estimated_extra_crop_revenue = baseline_crop_revenue * (yield_gain_percent / 100.0)

    total_annual_farmer_benefit = (
        annual_fertilizer_savings
        + annual_electricity_savings
        + estimated_extra_crop_revenue
    )

    if total_annual_farmer_benefit > 0:
        payback_years = round(net_farmer_investment / total_annual_farmer_benefit, 1)
        if payback_years < 0.2:
            payback_str = "Immediate (< 3 months)"
        elif payback_years <= 1.0:
            payback_str = f"~{int(payback_years * 12)} months (First Year)"
        else:
            payback_str = f"~{payback_years} years"
    else:
        payback_str = "12 - 18 months"

    return {
        "technique_title": technique["title"],
        "farm_acres": acres,
        "crop_type": crop_type,
        "base_setup_cost": round(base_cost, 2),
        "estimated_subsidy": round(estimated_subsidy, 2),
        "subsidy_percentage": technique["subsidy_percentage"],
        "net_farmer_cost": round(net_farmer_investment, 2),
        "water_saved_liters": int(water_saved_liters),
        "fertilizer_savings_inr": round(annual_fertilizer_savings, 2),
        "energy_savings_inr": round(annual_electricity_savings, 2),
        "extra_revenue_inr": round(estimated_extra_crop_revenue, 2),
        "total_annual_benefit": round(total_annual_farmer_benefit, 2),
        "yield_boost_percent": yield_gain_percent,
        "payback_period": payback_str
    }

