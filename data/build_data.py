# build_data.py
import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent
DATA_DIR.mkdir(parents=True, exist_ok=True)


products = [
    {
        "product_id": "FW-001",
        "name": "Gentle Skin Cleanser",
        "brand": "Cetaphil",
        "price_inr": 349,
        "skin_types": ["dry", "normal", "sensitive"],
        "concerns_addressed": ["dryness", "sensitivity"],
        "key_ingredients": ["glycerin", "niacinamide", "panthenol"],
        "full_ingredient_list": [
            "Water", "Glycerin", "Cetearyl Alcohol", "Sodium Cocoyl Isethionate", 
            "Niacinamide", "Panthenol", "Citric Acid", "Sodium Benzoate"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-002",
        "name": "Oily Skin Cleanser",
        "brand": "Cetaphil",
        "price_inr": 599,
        "skin_types": ["oily", "combination"],
        "concerns_addressed": ["excess_oil", "acne", "clogged_pores"],
        "key_ingredients": ["niacinamide", "panthenol", "glycerin"],
        "full_ingredient_list": [
            "Water", "Glycerin", "PEG-200 Hydrogenated Glyceryl Palmate", "Sodium Lauroyl Sarcosinate",
            "Niacinamide", "Panthenol", "Citric Acid", "Sodium Benzoate", "Fragrance"
        ],
        "flags": ["sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-003",
        "name": "Hydrating Facial Cleanser",
        "brand": "CeraVe",
        "price_inr": 490,
        "skin_types": ["dry", "normal", "sensitive"],
        "concerns_addressed": ["dryness", "barrier_repair", "sensitivity"],
        "key_ingredients": ["ceramides", "hyaluronic_acid", "glycerin"],
        "full_ingredient_list": [
            "Aqua/Water", "Glycerin", "Cetearyl Alcohol", "PEG-40 Stearate", "Stearyl Alcohol",
            "Potassium Phosphate", "Ceramide NP", "Ceramide AP", "Ceramide EOP", "Carbomer",
            "Glyceryl Stearate", "Behentrimonium Methosulfate", "Sodium Lauroyl Lactylate",
            "Sodium Hyaluronate", "Cholesterol", "Phenoxyethanol", "Disodium EDTA", "Dipotassium Phosphate",
            "Tocopherol", "Phytosphingosine", "Xanthan Gum", "Ethylhexylglycerin"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-004",
        "name": "Foaming Facial Cleanser",
        "brand": "CeraVe",
        "price_inr": 490,
        "skin_types": ["oily", "combination", "normal"],
        "concerns_addressed": ["excess_oil", "clogged_pores", "barrier_repair"],
        "key_ingredients": ["ceramides", "niacinamide", "hyaluronic_acid"],
        "full_ingredient_list": [
            "Aqua/Water", "Cocamidopropyl Hydroxysultaine", "Sodium Lauroyl Sarcosinate",
            "Propanediol", "PEG-150 Pentaerythrityl Tetrastearate", "PEG-6 Caprylic/Capric Glycerides",
            "Niacinamide", "Ceramide NP", "Ceramide AP", "Ceramide EOP", "Carbomer",
            "Sodium Methyl Cocoyl Taurate", "Sodium Hyaluronate", "Cholesterol", "Phenoxyethanol",
            "Disodium EDTA", "Citric Acid", "Phytosphingosine", "Xanthan Gum", "Ethylhexylglycerin"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-005",
        "name": "SA Smoothing Cleanser",
        "brand": "CeraVe",
        "price_inr": 699,
        "skin_types": ["oily", "combination", "normal"],
        "concerns_addressed": ["rough_texture", "acne", "clogged_pores"],
        "key_ingredients": ["salicylic_acid", "ceramides", "hyaluronic_acid", "niacinamide"],
        "full_ingredient_list": [
            "Aqua/Water", "Sodium Lauroyl Sarcosinate", "Cocamidopropyl Hydroxysultaine",
            "Glycerin", "Niacinamide", "Gluconolactone", "Sodium Methyl Cocoyl Taurate",
            "PEG-150 Pentaerythrityl Tetrastearate", "Ceramide NP", "Ceramide AP", "Ceramide EOP",
            "Carbomer", "Calcium Gluconate", "Salicylic Acid", "Sodium Benzoate", "Sodium Lauroyl Lactylate",
            "Cholesterol", "Tetrasodium EDTA", "Sodium Hyaluronate", "Phytosphingosine", "Benzoic Acid"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-006",
        "name": "Salicylic Acid 2% + LHA Cleanser",
        "brand": "Minimalist",
        "price_inr": 299,
        "skin_types": ["oily", "combination"],
        "concerns_addressed": ["acne", "excess_oil", "blackheads"],
        "key_ingredients": ["salicylic_acid", "capryloyl_salicylic_acid", "zinc_pca"],
        "full_ingredient_list": [
            "Aqua", "Glycerin", "Cocamidopropyl Betaine", "Propanediol", "Sodium Lauroyl Methyl Isethionate",
            "Salicylic Acid", "Capryloyl Salicylic Acid", "Zinc PCA", "Phenoxyethanol",
            "Ethylhexylglycerin", "Sodium Hydroxide", "Trisodium Ethylenediamine Disuccinate"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-007",
        "name": "Aquaporin Booster 5% Cleanser",
        "brand": "Minimalist",
        "price_inr": 299,
        "skin_types": ["dry", "normal", "sensitive"],
        "concerns_addressed": ["dryness", "dehydration"],
        "key_ingredients": ["glycerin", "glyceryl_glucoside", "hyaluronic_acid"],
        "full_ingredient_list": [
            "Aqua", "Glycerin", "Glyceryl Glucoside", "Diglycerin", "Cocamidopropyl Betaine",
            "Sodium Lauroyl Methyl Isethionate", "Sodium Hyaluronate", "Betaine", "Phenoxyethanol",
            "Sodium Hydroxide", "Ethylhexylglycerin", "Trisodium Ethylenediamine Disuccinate"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-008",
        "name": "Oat Extract 6% Gentle Cleanser",
        "brand": "Minimalist",
        "price_inr": 299,
        "skin_types": ["sensitive", "dry", "normal"],
        "concerns_addressed": ["sensitivity", "redness", "dryness"],
        "key_ingredients": ["oat_extract", "colloidal_oatmeal", "hyaluronic_acid"],
        "full_ingredient_list": [
            "Aqua", "Avena Sativa (Oat) Kernel Extract", "Glycerin", "Dicaprylyl Carbonate",
            "Sodium Lauroyl Methyl Isethionate", "Colloidal Oatmeal", "Sodium Hyaluronate",
            "Phenoxyethanol", "Ethylhexylglycerin", "Carbomer", "Sodium Hydroxide"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-009",
        "name": "1% Salicylic Acid Gel Face Wash",
        "brand": "The Derma Co",
        "price_inr": 249,
        "skin_types": ["oily", "combination"],
        "concerns_addressed": ["acne", "excess_oil", "blackheads"],
        "key_ingredients": ["salicylic_acid", "witch_hazel", "willow_bark"],
        "full_ingredient_list": [
            "Aqua", "Sodium Alpha Olefin Sulfonate", "Cocamidopropyl Betaine", "Glycerin",
            "Salicylic Acid", "Hamamelis Virginiana (Witch Hazel) Extract", "Salix Alba (Willow) Bark Extract",
            "Phenoxyethanol", "Disodium EDTA", "Sodium Hydroxide"
        ],
        "flags": ["fragrance_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-010",
        "name": "2% Niacinamide Gentle Skin Cleanser",
        "brand": "The Derma Co",
        "price_inr": 299,
        "skin_types": ["sensitive", "dry", "normal"],
        "concerns_addressed": ["sensitivity", "dullness", "barrier_repair"],
        "key_ingredients": ["niacinamide", "ceramides", "cica_extract"],
        "full_ingredient_list": [
            "Aqua", "Cetyl Alcohol", "Stearyl Alcohol", "Niacinamide", "Ceramide NP",
            "Centella Asiatica Extract", "Propylene Glycol", "Sodium Cocoyl Isethionate",
            "Phenoxyethanol", "Ethylhexylglycerin"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-011",
        "name": "Sensibio Gel Moussant",
        "brand": "Bioderma",
        "price_inr": 890,
        "skin_types": ["sensitive", "dry", "normal"],
        "concerns_addressed": ["sensitivity", "redness", "dryness"],
        "key_ingredients": ["coco_glucoside", "glyceryl_oleate", "mannitol", "xylitol"],
        "full_ingredient_list": [
            "Aqua/Water/Eau", "Sodium Cocoamphoacetate", "Propanediol", "Sodium Lauroyl Sarcosinate",
            "Citric Acid", "Coco-Glucoside", "Glyceryl Oleate", "Sodium Citrate", "PEG-90 Glyceryl Isostearate",
            "Mannitol", "Xylitol", "Rhamnose", "Fructooligosaccharides", "Tocopherol", "Hydrogenated Palm Glycerides Citrate",
            "Lecithin", "Ascorbyl Palmitate"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-012",
        "name": "Sebium Gel Moussant",
        "brand": "Bioderma",
        "price_inr": 890,
        "skin_types": ["oily", "combination"],
        "concerns_addressed": ["excess_oil", "acne", "clogged_pores"],
        "key_ingredients": ["zinc_sulfate", "copper_sulfate", "ginkgo_biloba"],
        "full_ingredient_list": [
            "Aqua/Water/Eau", "Sodium Cocoamphoacetate", "Sodium Laureth Sulfate", "Methylpropanediol",
            "Disodium EDTA", "Mannitol", "Xylitol", "Rhamnose", "Fructooligosaccharides", "Zinc Sulfate",
            "Copper Sulfate", "Ginkgo Biloba Leaf Extract", "PEG-90 Glyceryl Isostearate", "Laureth-2",
            "Potassium Sorbate", "Sodium Chloride", "Citric Acid", "Sodium Hydroxide", "Fragrance"
        ],
        "flags": ["alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-013",
        "name": "Clear Face Cleansing Foam",
        "brand": "Sebamed",
        "price_inr": 580,
        "skin_types": ["oily", "combination", "sensitive"],
        "concerns_addressed": ["acne", "excess_oil", "sensitivity"],
        "key_ingredients": ["montaline_c40", "panthenol"],
        "full_ingredient_list": [
            "Aqua", "Cocamidopropyl Betainamide MEA Chloride", "Cocotrimonium Methosulfate",
            "Sodium Lactate", "Panthenol", "Parfum", "Phenoxyethanol"
        ],
        "flags": ["sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-014",
        "name": "Kind to Skin Refreshing Facial Wash",
        "brand": "Simple",
        "price_inr": 349,
        "skin_types": ["sensitive", "normal", "combination", "dry", "oily"],
        "concerns_addressed": ["sensitivity", "dryness"],
        "key_ingredients": ["panthenol", "allantoin", "vitamin_e"],
        "full_ingredient_list": [
            "Aqua", "Cocamidopropyl Betaine", "Propylene Glycol", "Hydroxypropyl Methylcellulose",
            "Panthenol", "Tocopheryl Acetate", "Pantolactone", "Sodium Hydroxide", "Disodium EDTA",
            "Sodium Hydroxymethylglycinate"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-015",
        "name": "Daily Skin Detox Purifying Gel Wash",
        "brand": "Simple",
        "price_inr": 375,
        "skin_types": ["oily", "combination"],
        "concerns_addressed": ["excess_oil", "clogged_pores", "acne"],
        "key_ingredients": ["witch_hazel", "zinc_pca", "thyme_extract"],
        "full_ingredient_list": [
            "Aqua", "Hamamelis Virginiana Leaf Water", "Cocamidopropyl Betaine", "Propylene Glycol",
            "Glycerin", "Sodium Laureth Sulfate", "PEG-7 Glyceryl Cocoate", "Acrylates/C10-30 Alkyl Acrylate Crosspolymer",
            "Zinc PCA", "Thymus Vulgaris Flower/Leaf Extract", "Sodium Hydroxide", "Panthenol",
            "Dipotassium Glycyrrhizate", "Citric Acid"
        ],
        "flags": ["fragrance_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-016",
        "name": "Cica Calming Blemish Clearing Face Wash",
        "brand": "Dot & Key",
        "price_inr": 295,
        "skin_types": ["oily", "combination", "sensitive"],
        "concerns_addressed": ["acne", "redness", "excess_oil"],
        "key_ingredients": ["cica_extract", "salicylic_acid", "tea_tree_oil", "green_tea"],
        "full_ingredient_list": [
            "Aqua", "Sodium Lauroyl Sarcosinate", "Cocamidopropyl Betaine", "Glycerin",
            "Centella Asiatica (Cica) Extract", "Salicylic Acid", "Melaleuca Alternifolia (Tea Tree) Leaf Oil",
            "Camellia Sinensis (Green Tea) Leaf Extract", "Allantoin", "Phenoxyethanol"
        ],
        "flags": ["sulfate_free", "alcohol_free", "paraben_free"]
    },
    {
        "product_id": "FW-017",
        "name": "Barrier Repair Hydrating Gentle Face Wash",
        "brand": "Dot & Key",
        "price_inr": 345,
        "skin_types": ["dry", "sensitive", "normal"],
        "concerns_addressed": ["dryness", "barrier_repair", "sensitivity"],
        "key_ingredients": ["ceramides", "hyaluronic_acid", "probiotics"],
        "full_ingredient_list": [
            "Aqua", "Sodium Cocoyl Isethionate", "Glycerin", "Cocamidopropyl Betaine",
            "Ceramide NP", "Ceramide AP", "Ceramide EOP", "Phytosphingosine", "Cholesterol",
            "Sodium Hyaluronate", "Lactobacillus Ferment Lysate", "Phenoxyethanol", "Ethylhexylglycerin"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-018",
        "name": "Deep Clean Facial Cleanser",
        "brand": "Neutrogena",
        "price_inr": 440,
        "skin_types": ["oily", "normal"],
        "concerns_addressed": ["clogged_pores", "dullness", "excess_oil"],
        "key_ingredients": ["salicylic_acid", "glycerin"],
        "full_ingredient_list": [
            "Water", "Sodium Laureth Sulfate", "Glycerin", "Lauryl Glucoside",
            "Cocamidopropyl Betaine", "PEG-120 Methyl Glucose Dioleate", "Salicylic Acid",
            "Citric Acid", "Sodium Hydroxide", "Fragrance"
        ],
        "flags": ["alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-019",
        "name": "Hydro Boost Cleanser Water Gel",
        "brand": "Neutrogena",
        "price_inr": 850,
        "skin_types": ["dry", "combination", "normal"],
        "concerns_addressed": ["dehydration", "dryness"],
        "key_ingredients": ["hyaluronic_acid", "glycerin"],
        "full_ingredient_list": [
            "Water", "Glycerin", "Cocamidopropyl Hydroxysultaine", "Sodium Cocoyl Isethionate",
            "Sodium Methyl Cocoyl Taurate", "Sodium Hydrolyzed Potato Starch Dodecenylsuccinate",
            "Hydrolyzed Hyaluronic Acid", "Ethylhexylglycerin", "Linoleamidopropyl PG-Dimonium Chloride Phosphate",
            "Polyquaternium-10", "Disodium EDTA", "Citric Acid", "Fragrance"
        ],
        "flags": ["sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-020",
        "name": "Green Tea Pore Cleansing Face Wash",
        "brand": "Plum",
        "price_inr": 345,
        "skin_types": ["oily", "combination"],
        "concerns_addressed": ["acne", "excess_oil"],
        "key_ingredients": ["green_tea", "glycolic_acid", "cellulose_beads"],
        "full_ingredient_list": [
            "Aqua", "Sodium Laureth Sulfate", "Cocamidopropyl Betaine", "Glycerin",
            "Camellia Sinensis (Green Tea) Leaf Extract", "Glycolic Acid", "Cellulose Beads",
            "Phenoxyethanol", "Fragrance"
        ],
        "flags": ["alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-021",
        "name": "1% Oat & Allantoin Gentle Cleanser",
        "brand": "Plum",
        "price_inr": 299,
        "skin_types": ["sensitive", "dry"],
        "concerns_addressed": ["sensitivity", "redness", "dryness"],
        "key_ingredients": ["oat_extract", "allantoin", "glycerin"],
        "full_ingredient_list": [
            "Aqua", "Sodium Lauroyl Sarcosinate", "Glycerin", "Cocamidopropyl Betaine",
            "Avena Sativa (Oat) Kernel Flour", "Allantoin", "Xanthan Gum", "Phenoxyethanol",
            "Ethylhexylglycerin", "Disodium EDTA"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-022",
        "name": "The Daily Duet Gentle Hydrating Cleanser",
        "brand": "Foxtale",
        "price_inr": 349,
        "skin_types": ["dry", "normal", "sensitive", "combination"],
        "concerns_addressed": ["dryness", "sensitivity"],
        "key_ingredients": ["sodium_hyaluronate", "red_algae_extract", "vitamin_b5"],
        "full_ingredient_list": [
            "Aqua", "Sodium Lauroyl Sarcosinate", "Cocamidopropyl Betaine", "Glycerin",
            "Sodium Hyaluronate", "Chondrus Crispus (Red Algae) Extract", "Panthenol",
            "Phenoxyethanol", "Disodium EDTA"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-023",
        "name": "Acne Fighting Cleanser with Salicylic Acid",
        "brand": "Foxtale",
        "price_inr": 349,
        "skin_types": ["oily", "combination"],
        "concerns_addressed": ["acne", "excess_oil", "blackheads"],
        "key_ingredients": ["salicylic_acid", "niacinamide", "hyaluronic_acid"],
        "full_ingredient_list": [
            "Aqua", "Sodium Lauroyl Sarcosinate", "Cocamidopropyl Betaine", "Salicylic Acid",
            "Niacinamide", "Sodium Hyaluronate", "Glycerin", "Phenoxyethanol", "Disodium EDTA"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-024",
        "name": "Fruit AHA Face Wash for Pigmentation",
        "brand": "Re'equil",
        "price_inr": 450,
        "skin_types": ["oily", "combination", "normal"],
        "concerns_addressed": ["dullness", "pigmentation", "rough_texture"],
        "key_ingredients": ["glycolic_acid", "lactic_acid", "bilberry_extract"],
        "full_ingredient_list": [
            "Aqua", "Cocamidopropyl Betaine", "Sodium Lauroyl Sarcosinate", "Vaccinium Myrtillus Fruit Extract",
            "Saccharum Officinarum (Sugar Cane) Extract", "Citrus Aurantium Dulcis (Orange) Fruit Extract",
            "Citrus Limon (Lemon) Fruit Extract", "Acer Saccharum (Sugar Maple) Extract", "Citric Acid",
            "Glycolic Acid", "Lactic Acid", "Phenoxyethanol", "Fragrance"
        ],
        "flags": ["sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-025",
        "name": "Oil Regulating Cleanser with Zinc PCA",
        "brand": "Re'equil",
        "price_inr": 490,
        "skin_types": ["oily", "combination"],
        "concerns_addressed": ["excess_oil", "acne", "clogged_pores"],
        "key_ingredients": ["zinc_pca", "citric_acid", "glycerin"],
        "full_ingredient_list": [
            "Aqua", "Cocamidopropyl Betaine", "Sodium Cocoyl Isethionate", "Zinc PCA",
            "Glycerin", "Citric Acid", "Phenoxyethanol", "Ethylhexylglycerin"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-026",
        "name": "Ceramide & Hyaluronic Acid Moisturising Face Wash",
        "brand": "Re'equil",
        "price_inr": 450,
        "skin_types": ["dry", "sensitive", "normal"],
        "concerns_addressed": ["dryness", "barrier_repair", "sensitivity"],
        "key_ingredients": ["ceramides", "hyaluronic_acid", "mango_butter"],
        "full_ingredient_list": [
            "Aqua", "Cetearyl Alcohol", "Sodium Cocoyl Isethionate", "Ceramide III",
            "Sodium Hyaluronate", "Mangifera Indica (Mango) Seed Butter", "Glycerin",
            "Phenoxyethanol", "Disodium EDTA"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-027",
        "name": "Salicylic Acid Oil Control Cleanser 0.5%",
        "brand": "Deconstruct",
        "price_inr": 299,
        "skin_types": ["oily", "combination", "sensitive"],
        "concerns_addressed": ["acne", "excess_oil"],
        "key_ingredients": ["salicylic_acid", "niacinamide"],
        "full_ingredient_list": [
            "Aqua", "Cocamidopropyl Betaine", "Sodium Lauroyl Sarcosinate", "Salicylic Acid",
            "Niacinamide", "Glycerin", "Xanthan Gum", "Phenoxyethanol", "Disodium EDTA"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-028",
        "name": "Hydrating Face Wash with Amino Acids",
        "brand": "Deconstruct",
        "price_inr": 299,
        "skin_types": ["dry", "normal", "sensitive"],
        "concerns_addressed": ["dryness", "dehydration"],
        "key_ingredients": ["amino_acids", "hyaluronic_acid", "panthenol"],
        "full_ingredient_list": [
            "Aqua", "Sodium Cocoyl Glycinate", "Glycerin", "Sodium Hyaluronate",
            "Sodium PCA", "Panthenol", "Proline", "Serine", "Phenoxyethanol"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-029",
        "name": "Flashfade Niacinamide Gel Cleanser",
        "brand": "Conscious Chemist",
        "price_inr": 349,
        "skin_types": ["all", "combination", "normal", "oily"],
        "concerns_addressed": ["dullness", "pigmentation", "excess_oil"],
        "key_ingredients": ["niacinamide", "licorice_root", "ceramides"],
        "full_ingredient_list": [
            "Aqua", "Sodium Lauroyl Sarcosinate", "Cocamidopropyl Betaine", "Niacinamide",
            "Glycyrrhiza Glabra (Licorice) Root Extract", "Ceramide NP", "Glycerin",
            "Phenoxyethanol", "Ethylhexylglycerin"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-030",
        "name": "Cleansing Lotion for Sensitive and Dry Skin",
        "brand": "Episoft",
        "price_inr": 480,
        "skin_types": ["sensitive", "dry"],
        "concerns_addressed": ["sensitivity", "dryness", "redness"],
        "key_ingredients": ["cetearyl_alcohol", "glycerin"],
        "full_ingredient_list": [
            "Purified Water", "Cetearyl Alcohol", "1,3-Butylene Glycol", "Sodium Cocoyl Glycinate",
            "Glycerin", "Phenoxyethanol", "Disodium EDTA", "Citric Acid"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-031",
        "name": "pH 5.5 Moisture Balancing Face Wash",
        "brand": "Joy",
        "price_inr": 195,
        "skin_types": ["all", "normal", "sensitive", "dry"],
        "concerns_addressed": ["barrier_repair", "dryness", "sensitivity"],
        "key_ingredients": ["panthenol", "ceramides", "calendula_extract"],
        "full_ingredient_list": [
            "Aqua", "Cocamidopropyl Betaine", "Sodium Lauroyl Sarcosinate", "Glycerin",
            "Panthenol", "Ceramide Complex", "Calendula Officinalis Flower Extract",
            "Citric Acid", "Phenoxyethanol"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-032",
        "name": "Purifying Neem Face Wash",
        "brand": "Himalaya",
        "price_inr": 140,
        "skin_types": ["oily", "combination"],
        "concerns_addressed": ["acne", "excess_oil"],
        "key_ingredients": ["neem_extract", "turmeric_extract"],
        "full_ingredient_list": [
            "Aqua", "Ammonium Lauryl Sulfate", "Melia Azadirachta Leaf Extract",
            "Cocamidopropyl Betaine", "Sodium Cocoyl Glutamate", "Glycerin",
            "Curcuma Longa (Turmeric) Rhizome Extract", "Phenoxyethanol", "Fragrance", "CI 19140", "CI 42090"
        ],
        "flags": ["alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-033",
        "name": "Moisturizing Aloe Vera Face Wash",
        "brand": "Himalaya",
        "price_inr": 140,
        "skin_types": ["dry", "normal"],
        "concerns_addressed": ["dryness"],
        "key_ingredients": ["aloe_vera", "cucumber_extract"],
        "full_ingredient_list": [
            "Aqua", "Ammonium Lauryl Sulfate", "Cocamidopropyl Betaine", "Aloe Barbadensis Leaf Extract",
            "Cucumis Sativus (Cucumber) Fruit Extract", "Glycerin", "Phenoxyethanol", "Fragrance"
        ],
        "flags": ["alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-034",
        "name": "Acne Control Face Wash with 1% Salicylic Acid + 5% Niacinamide",
        "brand": "Chemist at Play",
        "price_inr": 349,
        "skin_types": ["oily", "combination"],
        "concerns_addressed": ["acne", "blackheads", "excess_oil"],
        "key_ingredients": ["salicylic_acid", "niacinamide", "ceramides"],
        "full_ingredient_list": [
            "Aqua", "Sodium Lauroyl Sarcosinate", "Cocamidopropyl Betaine", "Niacinamide",
            "Salicylic Acid", "Ceramide NP", "Ceramide AP", "Phytosphingosine", "Glycerin",
            "Phenoxyethanol", "Disodium EDTA"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-035",
        "name": "Hydrating Face Wash with Ceramides",
        "brand": "Chemist at Play",
        "price_inr": 349,
        "skin_types": ["dry", "normal", "sensitive"],
        "concerns_addressed": ["dryness", "barrier_repair"],
        "key_ingredients": ["ceramides", "hyaluronic_acid", "colloidal_oatmeal"],
        "full_ingredient_list": [
            "Aqua", "Sodium Cocoyl Isethionate", "Glycerin", "Ceramide NP",
            "Ceramide AP", "Sodium Hyaluronate", "Colloidal Oatmeal", "Phenoxyethanol",
            "Ethylhexylglycerin"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-036",
        "name": "Low pH Good Morning Gel Cleanser",
        "brand": "COSRX",
        "price_inr": 750,
        "skin_types": ["oily", "combination", "sensitive"],
        "concerns_addressed": ["acne", "excess_oil", "sensitivity"],
        "key_ingredients": ["betaine_salicylate", "tea_tree_oil"],
        "full_ingredient_list": [
            "Water", "Cocamidopropyl Betaine", "Sodium Lauroyl Methyl Isethionate", "Polysorbate 20",
            "Styrax Japonicus Branch/Fruit/Leaf Extract", "Butylene Glycol", "Saccharomyces Ferment",
            "Cryptomeria Japonica Leaf Extract", "Nelumbo Nucifera Leaf Extract", "Pinus Palustris Leaf Extract",
            "Ulmus Davidiana Root Extract", "Oenothera Biennis (Evening Primrose) Flower Extract",
            "Pueraria Lobata Root Extract", "Melaleuca Alternifolia (Tea Tree) Leaf Oil", "Allantoin",
            "Caprylyl Glycol", "Ethylhexylglycerin", "Betaine Salicylate", "Citric Acid", "Ethyl Hexanediol",
            "1,2-Hexanediol", "Trisodium Ethylenediamine Disuccinate", "Sodium Benzoate", "Disodium EDTA"
        ],
        "flags": ["sulfate_free", "alcohol_free", "paraben_free"]
    },
    {
        "product_id": "FW-037",
        "name": "Salicylic Acid Daily Gentle Cleanser",
        "brand": "COSRX",
        "price_inr": 850,
        "skin_types": ["oily", "combination"],
        "concerns_addressed": ["acne", "clogged_pores", "excess_oil"],
        "key_ingredients": ["salicylic_acid", "tea_tree_oil"],
        "full_ingredient_list": [
            "Water", "Glycerin", "Myristic Acid", "Stearic Acid", "Potassium Hydroxide",
            "Lauric Acid", "Butylene Glycol", "Glycol Distearate", "Polysorbate 80",
            "Sodium Methyl Cocoyl Taurate", "Salicylic Acid", "Cocamidopropyl Betaine",
            "PEG-60 Hydrogenated Castor Oil", "Fragrance", "Sodium Chloride", "Melaleuca Alternifolia (Tea Tree) Leaf Oil",
            "Caprylyl Glycol", "Ethylhexylglycerin", "Salix Alba (Willow) Bark Water", "Disodium EDTA"
        ],
        "flags": ["sulfate_free", "alcohol_free", "paraben_free"]
    },
    {
        "product_id": "FW-038",
        "name": "Toleriane Hydrating Gentle Cleanser",
        "brand": "La Roche-Posay",
        "price_inr": 1390,
        "skin_types": ["dry", "sensitive", "normal"],
        "concerns_addressed": ["dryness", "sensitivity", "barrier_repair"],
        "key_ingredients": ["ceramide_3", "niacinamide", "glycerin", "thermal_spring_water"],
        "full_ingredient_list": [
            "Aqua/Water", "Glycerin", "Pentaerythrityl Tetraethylhexanoate", "Propylene Glycol",
            "Ammonium Polyacryloyldimethyl Taurate", "Polysorbate 60", "Ceramide NP",
            "Niacinamide", "Sodium Chloride", "Coco-Betaine", "Disodium EDTA", "Caprylyl Glycol",
            "Panthenol", "Tocopherol"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-039",
        "name": "Effaclar Purifying Foaming Gel Cleanser",
        "brand": "La Roche-Posay",
        "price_inr": 1150,
        "skin_types": ["oily", "sensitive"],
        "concerns_addressed": ["acne", "excess_oil", "clogged_pores"],
        "key_ingredients": ["zinc_pca", "thermal_spring_water"],
        "full_ingredient_list": [
            "Aqua/Water", "Sodium Laureth Sulfate", "PEG-8", "Coco-Betaine", "Hexylene Glycol",
            "Sodium Chloride", "PEG-120 Methyl Glucose Dioleate", "Zinc PCA", "Sodium Hydroxide",
            "Citric Acid", "Sodium Benzoate", "Phenoxyethanol", "Caprylyl Glycol", "Parfum/Fragrance"
        ],
        "flags": ["alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-040",
        "name": "Green Tea Hydrating Amino Acid Cleansing Foam",
        "brand": "Innisfree",
        "price_inr": 700,
        "skin_types": ["combination", "normal", "oily"],
        "concerns_addressed": ["dryness", "excess_oil"],
        "key_ingredients": ["green_tea_extract", "amino_acids", "glycerin"],
        "full_ingredient_list": [
            "Water/Aqua/Eau", "Glycerin", "Myristic Acid", "Stearic Acid", "PEG-32",
            "Potassium Hydroxide", "Palmitic Acid", "Lauric Acid", "Lauryl Glucoside",
            "Camellia Sinensis Leaf Extract", "Arginine", "Aspartic Acid", "Glutamic Acid",
            "Disodium EDTA", "Fragrance/Parfum"
        ],
        "flags": ["sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-041",
        "name": "Volcanic BHA Pore Cleansing Foam",
        "brand": "Innisfree",
        "price_inr": 750,
        "skin_types": ["oily", "combination"],
        "concerns_addressed": ["blackheads", "clogged_pores", "excess_oil"],
        "key_ingredients": ["volcanic_ash", "salicylic_acid", "lactic_acid"],
        "full_ingredient_list": [
            "Water/Aqua/Eau", "Glycerin", "Myristic Acid", "Stearic Acid", "PEG-32",
            "Potassium Hydroxide", "Lauric Acid", "Volcanic Ash", "Salicylic Acid",
            "Lactic Acid", "Silica", "Disodium EDTA", "Fragrance/Parfum"
        ],
        "flags": ["sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-042",
        "name": "CLEAR Pore Normalizing Cleanser",
        "brand": "Paula's Choice",
        "price_inr": 1390,
        "skin_types": ["oily", "combination", "sensitive"],
        "concerns_addressed": ["acne", "clogged_pores", "redness"],
        "key_ingredients": ["salicylic_acid", "arginine", "glycerin"],
        "full_ingredient_list": [
            "Water", "Sodium Lauroyl Sarcosinate", "Acrylates/Steareth-20 Methacrylate Copolymer",
            "Glycerin", "PEG-200 Hydrogenated Glyceryl Palmate", "Sodium Laureth Sulfate",
            "Salicylic Acid", "Arginine", "Butylene Glycol", "PEG-7 Glyceryl Cocoate",
            "Panthenol", "Disodium EDTA", "Phenoxyethanol", "Caprylyl Glycol"
        ],
        "flags": ["fragrance_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-043",
        "name": "Glow+ Smoothie Face Wash",
        "brand": "Aqualogica",
        "price_inr": 249,
        "skin_types": ["all", "normal", "combination"],
        "concerns_addressed": ["dullness", "dehydration"],
        "key_ingredients": ["vitamin_c", "papaya_extract", "hyaluronic_acid"],
        "full_ingredient_list": [
            "Aqua", "Sodium Lauroyl Sarcosinate", "Cocamidopropyl Betaine", "Glycerin",
            "Carica Papaya (Papaya) Fruit Extract", "Ascorbyl Glucoside", "Sodium Hyaluronate",
            "Phenoxyethanol", "Fragrance"
        ],
        "flags": ["sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-044",
        "name": "Hydrate+ Gel Face Wash",
        "brand": "Aqualogica",
        "price_inr": 249,
        "skin_types": ["dry", "normal", "sensitive"],
        "concerns_addressed": ["dryness", "dehydration"],
        "key_ingredients": ["coconut_water", "hyaluronic_acid", "glycerin"],
        "full_ingredient_list": [
            "Aqua", "Cocamidopropyl Betaine", "Sodium Cocoyl Isethionate", "Glycerin",
            "Cocos Nucifera (Coconut) Water", "Sodium Hyaluronate", "Phenoxyethanol", "Fragrance"
        ],
        "flags": ["sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-045",
        "name": "Tea Tree Face Wash with Neem",
        "brand": "Mamaearth",
        "price_inr": 259,
        "skin_types": ["oily", "combination"],
        "concerns_addressed": ["acne", "excess_oil"],
        "key_ingredients": ["tea_tree_oil", "neem_extract", "aloe_vera"],
        "full_ingredient_list": [
            "Aqua", "Sodium Lauroyl Sarcosinate", "Cocamidopropyl Betaine", "Melaleuca Alternifolia (Tea Tree) Leaf Oil",
            "Melia Azadirachta (Neem) Leaf Extract", "Aloe Barbadensis Leaf Juice", "Glycerin",
            "Phenoxyethanol", "Disodium EDTA"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free"]
    },
    {
        "product_id": "FW-046",
        "name": "Ubtan Face Wash with Turmeric & Saffron",
        "brand": "Mamaearth",
        "price_inr": 259,
        "skin_types": ["all", "combination", "normal"],
        "concerns_addressed": ["dullness", "pigmentation"],
        "key_ingredients": ["turmeric_extract", "saffron_extract", "walnut_beads"],
        "full_ingredient_list": [
            "Aqua", "Sodium Lauroyl Sarcosinate", "Cocamidopropyl Betaine", "Curcuma Longa (Turmeric) Extract",
            "Crocus Sativus (Saffron) Flower Extract", "Juglans Regia (Walnut) Shell Powder", "Glycerin",
            "Phenoxyethanol", "Fragrance"
        ],
        "flags": ["sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-047",
        "name": "Apple Cider Vinegar Foaming Face Wash",
        "brand": "WOW Skin Science",
        "price_inr": 349,
        "skin_types": ["oily", "combination"],
        "concerns_addressed": ["acne", "excess_oil", "blackheads"],
        "key_ingredients": ["apple_cider_vinegar", "aloe_vera", "vitamin_b5"],
        "full_ingredient_list": [
            "Purified Water", "Sodium Lauroyl Sarcosinate", "Disodium Cocoamphodiacetate", "Apple Cider Vinegar",
            "Aloe Barbadensis Leaf Juice", "D-Panthenol", "Tocopheryl Acetate", "Phenoxyethanol", "Fragrance"
        ],
        "flags": ["sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-048",
        "name": "Clean & Clear Foaming Face Wash",
        "brand": "Clean & Clear",
        "price_inr": 175,
        "skin_types": ["oily", "normal"],
        "concerns_addressed": ["excess_oil", "acne"],
        "key_ingredients": ["glycerin", "myristic_acid", "lauric_acid"],
        "full_ingredient_list": [
            "Water", "Triethanolamine", "Myristic Acid", "Lauric Acid", "Glycerin",
            "Cocamidopropyl Betaine", "Hydroxylpropyl Methylcellulose", "Fragrance", "BHT"
        ],
        "flags": ["sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-049",
        "name": "Bright Beauty Spot-less Glow Face Wash",
        "brand": "Pond's",
        "price_inr": 160,
        "skin_types": ["all", "normal", "oily"],
        "concerns_addressed": ["dullness", "pigmentation"],
        "key_ingredients": ["niacinamide", "glycerin"],
        "full_ingredient_list": [
            "Myristic Acid", "Glycerin", "Water", "Propylene Glycol", "Potassium Hydroxide",
            "Palmitic Acid & Stearic Acid", "Lauric Acid", "Glycol Distearate", "Decyl Glucoside",
            "Niacinamide", "Polyquaternium-7", "Fragrance", "Disodium EDTA"
        ],
        "flags": ["sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-050",
        "name": "Pure Detox Mineral Clay Anti-Pollution Face Wash",
        "brand": "Pond's",
        "price_inr": 199,
        "skin_types": ["oily", "combination"],
        "concerns_addressed": ["clogged_pores", "excess_oil", "dullness"],
        "key_ingredients": ["activated_charcoal", "moroccan_clay"],
        "full_ingredient_list": [
            "Myristic Acid", "Glycerin", "Water", "Potassium Hydroxide", "Stearic Acid",
            "Lauric Acid", "Kaolin (Moroccan Clay)", "Charcoal Powder", "Fragrance"
        ],
        "flags": ["sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-051",
        "name": "Bright Complete Vitamin C Face Wash",
        "brand": "Garnier",
        "price_inr": 175,
        "skin_types": ["all", "normal", "oily"],
        "concerns_addressed": ["dullness", "pigmentation"],
        "key_ingredients": ["ascorbyl_glucoside", "lemon_extract"],
        "full_ingredient_list": [
            "Aqua/Water", "Glycerin", "Myristic Acid", "Palmitic Acid", "Stearic Acid",
            "Potassium Hydroxide", "Lauric Acid", "Citrus Limon Fruit Extract/Lemon Fruit Extract",
            "Ascorbyl Glucoside", "Fragrance"
        ],
        "flags": ["sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-052",
        "name": "Blush & Glow Strawberry Gel Face Wash",
        "brand": "Lakme",
        "price_inr": 185,
        "skin_types": ["all", "normal", "dry"],
        "concerns_addressed": ["dullness", "dryness"],
        "key_ingredients": ["strawberry_extract", "glycerin"],
        "full_ingredient_list": [
            "Aqua", "Sodium Laureth Sulfate", "Glycerin", "Cocamidopropyl Betaine",
            "Fragaria Vesca (Strawberry) Fruit Extract", "Menthol", "Fragrance"
        ],
        "flags": ["alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-053",
        "name": "Purifying Cleanser for Acne Prone Skin",
        "brand": "Kaya",
        "price_inr": 380,
        "skin_types": ["oily", "combination"],
        "concerns_addressed": ["acne", "excess_oil", "blackheads"],
        "key_ingredients": ["salicylic_acid", "glycerin"],
        "full_ingredient_list": [
            "Aqua", "Sodium Laureth Sulfate", "Cocamidopropyl Betaine", "Salicylic Acid",
            "Glycerin", "Propylene Glycol", "Disodium EDTA", "Phenoxyethanol", "Fragrance"
        ],
        "flags": ["alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-054",
        "name": "Cleanance Cleansing Gel",
        "brand": "Avene",
        "price_inr": 1450,
        "skin_types": ["oily", "sensitive", "combination"],
        "concerns_addressed": ["acne", "excess_oil", "sensitivity"],
        "key_ingredients": ["avene_thermal_spring_water", "comedoclastin", "zinc_gluconate"],
        "full_ingredient_list": [
            "Avene Thermal Spring Water", "Water (Aqua)", "Zinc Coceth Sulfate", "Lauryl Betaine",
            "Decyl Glucoside", "Ceteareth-60 Myristyl Glycol", "PEG-7 Glyceryl Cocoate",
            "Silybum Marianum Fruit Extract (Comedoclastin)", "Zinc Gluconate", "Citric Acid",
            "Fragrance (Parfum)", "Sodium Benzoate", "Sodium Hydroxide"
        ],
        "flags": ["alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-055",
        "name": "Calendula Deep Cleansing Foaming Face Wash",
        "brand": "Kiehl's",
        "price_inr": 1550,
        "skin_types": ["normal", "oily", "sensitive"],
        "concerns_addressed": ["sensitivity", "redness", "excess_oil"],
        "key_ingredients": ["calendula_extract", "glycerin"],
        "full_ingredient_list": [
            "Aqua/Water", "Sodium Cocoyl Glycinate", "Coco-Betaine", "Glycerin",
            "Acrylates Copolymer", "Sodium Chloride", "Calendula Officinalis Flower Extract",
            "Phenoxyethanol", "Citrus Limon Peel Oil", "Limonene"
        ],
        "flags": ["sulfate_free", "alcohol_free", "paraben_free"]
    },
    {
        "product_id": "FW-056",
        "name": "Saslic DS 2% Salicylic Acid Foaming Face Wash",
        "brand": "Cipla",
        "price_inr": 420,
        "skin_types": ["oily", "combination"],
        "concerns_addressed": ["acne", "blackheads", "excess_oil"],
        "key_ingredients": ["salicylic_acid"],
        "full_ingredient_list": [
            "Purified Water", "Salicylic Acid", "Sodium Cocoamphoacetate", "Propylene Glycol",
            "Cocamidopropyl Betaine", "Sodium Hydroxide", "Phenoxyethanol"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-057",
        "name": "Saslic 1% Salicylic Acid Foaming Face Wash",
        "brand": "Cipla",
        "price_inr": 360,
        "skin_types": ["combination", "sensitive", "oily"],
        "concerns_addressed": ["acne", "excess_oil"],
        "key_ingredients": ["salicylic_acid"],
        "full_ingredient_list": [
            "Purified Water", "Salicylic Acid", "Sodium Cocoamphoacetate", "Propylene Glycol",
            "Cocamidopropyl Betaine", "Sodium Hydroxide", "Phenoxyethanol"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-058",
        "name": "Water Boost Micellar Facial Gel Wash",
        "brand": "Simple",
        "price_inr": 365,
        "skin_types": ["dry", "sensitive", "normal"],
        "concerns_addressed": ["dehydration", "dryness", "sensitivity"],
        "key_ingredients": ["plant_derived_penta_saccharide", "minerals"],
        "full_ingredient_list": [
            "Aqua", "Cocamidopropyl Betaine", "Propylene Glycol", "Hydroxypropyl Methylcellulose",
            "Panthenol", "Sodium Chloride", "Citric Acid", "Disodium EDTA", "Glycerin",
            "Sodium Hydroxymethylglycinate", "Potassium Chloride"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-059",
        "name": "Watermelon SuperGlow Gel Face Wash",
        "brand": "Dot & Key",
        "price_inr": 295,
        "skin_types": ["all", "combination", "oily"],
        "concerns_addressed": ["dullness", "excess_oil"],
        "key_ingredients": ["watermelon_extract", "glycolic_acid", "vitamin_c"],
        "full_ingredient_list": [
            "Aqua", "Cocamidopropyl Betaine", "Sodium Lauroyl Sarcosinate", "Glycerin",
            "Citrullus Lanatus (Watermelon) Fruit Extract", "Glycolic Acid", "3-O-Ethyl Ascorbic Acid",
            "Phenoxyethanol", "Fragrance"
        ],
        "flags": ["sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-060",
        "name": "Blemish Control Cleanser",
        "brand": "CeraVe",
        "price_inr": 720,
        "skin_types": ["oily", "combination"],
        "concerns_addressed": ["acne", "clogged_pores", "excess_oil"],
        "key_ingredients": ["salicylic_acid", "niacinamide", "ceramides", "hectorite_clay"],
        "full_ingredient_list": [
            "Aqua/Water", "Sodium Lauroyl Sarcosinate", "Cocamidopropyl Hydroxysultaine",
            "Glycerin", "Niacinamide", "Salicylic Acid", "Gluconolactone", "Sodium Methyl Cocoyl Taurate",
            "Ceramide NP", "Ceramide AP", "Ceramide EOP", "Carbomer", "Hectorite", "Phytosphingosine",
            "Cholesterol", "Sodium Hyaluronate", "Sodium Benzoate", "Disodium EDTA"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-061",
        "name": "Fruit AHA 2% Gentle Foaming Wash",
        "brand": "Conscious Chemist",
        "price_inr": 399,
        "skin_types": ["normal", "combination", "oily"],
        "concerns_addressed": ["dullness", "rough_texture", "pigmentation"],
        "key_ingredients": ["lactic_acid", "glycolic_acid", "malic_acid"],
        "full_ingredient_list": [
            "Aqua", "Sodium Cocoyl Glycinate", "Cocamidopropyl Betaine", "Lactic Acid",
            "Glycolic Acid", "Vaccinium Myrtillus Fruit Extract", "Glycerin", "Phenoxyethanol"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-062",
        "name": "1% Kojic Acid Daily Face Wash",
        "brand": "The Derma Co",
        "price_inr": 299,
        "skin_types": ["all", "combination", "normal"],
        "concerns_addressed": ["pigmentation", "dullness"],
        "key_ingredients": ["kojic_acid", "alpha_arbutin", "niacinamide"],
        "full_ingredient_list": [
            "Aqua", "Sodium Alpha Olefin Sulfonate", "Cocamidopropyl Betaine", "Glycerin",
            "Kojic Acid Dipalmitate", "Alpha Arbutin", "Niacinamide", "Phenoxyethanol", "Disodium EDTA"
        ],
        "flags": ["fragrance_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-063",
        "name": "Basic Cleanser",
        "brand": "FAE Beauty",
        "price_inr": 350,
        "skin_types": ["all", "sensitive", "dry", "normal"],
        "concerns_addressed": ["sensitivity", "dryness"],
        "key_ingredients": ["panthenol", "glycerin", "allantoin"],
        "full_ingredient_list": [
            "Aqua", "Sodium Cocoyl Isethionate", "Glycerin", "Panthenol",
            "Allantoin", "Phenoxyethanol", "Ethylhexylglycerin"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    },
    {
        "product_id": "FW-064",
        "name": "Acrofy Acne Cleanser",
        "brand": "Brinton",
        "price_inr": 499,
        "skin_types": ["oily", "combination"],
        "concerns_addressed": ["acne", "excess_oil"],
        "key_ingredients": ["salicylic_acid", "tea_tree_oil", "zinc_pca"],
        "full_ingredient_list": [
            "Aqua", "Sodium Lauroyl Sarcosinate", "Cocamidopropyl Betaine", "Salicylic Acid",
            "Zinc PCA", "Melaleuca Alternifolia (Tea Tree) Leaf Oil", "Glycerin", "Phenoxyethanol"
        ],
        "flags": ["sulfate_free", "alcohol_free", "paraben_free"]
    },
    {
        "product_id": "FW-065",
        "name": "Delicate Facial Cleanser Kashmiri Saffron & Neem",
        "brand": "Forest Essentials",
        "price_inr": 1475,
        "skin_types": ["all", "combination", "normal"],
        "concerns_addressed": ["dullness", "excess_oil"],
        "key_ingredients": ["saffron_extract", "neem_infusion", "rose_water"],
        "full_ingredient_list": [
            "Aqua", "Steam Distilled Rose Water", "Kashmiri Saffron Extract", "Neem Leaf Infusion",
            "Marigold Extract", "Anantmool Root Extract", "Sodium Cocoyl Apple Amino Acids",
            "Glycerin", "Potassium Sorbate"
        ],
        "flags": ["fragrance_free", "sulfate_free", "alcohol_free", "paraben_free", "essential_oil_free"]
    }
]

ingredient_kb = [
    {
        "ingredient_name": "Salicylic Acid",
        "aliases": ["bha", "beta hydroxy acid", "2-hydroxybenzoic acid"],
        "function": "Lipophilic beta-hydroxy acid (BHA) that penetrates sebum inside pores, dissolving keratin plugs and promoting cellular turnover.",
        "common_concerns": ["acne", "blackheads", "clogged_pores", "excess_oil"],
        "caution_notes": "Can cause mild dryness or peeling if overused. Increases skin sensitivity; pairing with daily broad-spectrum sunscreen is strongly advised.",
        "source": "Cosmetic Ingredient Review (CIR) Expert Panel & Journal of Clinical and Aesthetic Dermatology (2020)"
    },
    {
        "ingredient_name": "Niacinamide",
        "aliases": ["vitamin b3", "nicotinamide"],
        "function": "Water-soluble physiological vitamin that inhibits melanosome transfer, regulates sebum secretion, and upregulates ceramide biosynthesis in the lipid barrier.",
        "common_concerns": ["dullness", "pigmentation", "excess_oil", "barrier_repair", "sensitivity"],
        "caution_notes": "Well-tolerated across sensitive skin; high concentrations (>10%) may cause transient flushing in sensitive individuals.",
        "source": "British Journal of Dermatology (2018) & Paula's Choice Skincare Ingredient Dictionary"
    },
    {
        "ingredient_name": "Hyaluronic Acid",
        "aliases": ["sodium hyaluronate", "hydrolyzed hyaluronic acid", "ha"],
        "function": "High-potency humectant capable of binding up to 1000 times its molecular weight in water, drawing moisture into stratum corneum surface layers.",
        "common_concerns": ["dryness", "dehydration", "sensitivity"],
        "caution_notes": "Best combined with occlusives or barrier emollients in low-humidity environments to prevent trans-epidermal water loss.",
        "source": "International Journal of Biological Macromolecules (2019) & CIR Compendium"
    },
    {
        "ingredient_name": "Ceramides",
        "aliases": ["ceramide np", "ceramide ap", "ceramide eop", "ceramide 3", "phytosphingosine"],
        "function": "Essential physiological lipids (sphingolipids) comprising ~50% of the stratum corneum intercellular matrix, sealing moisture and protecting against external pathogens.",
        "common_concerns": ["barrier_repair", "dryness", "sensitivity", "redness"],
        "caution_notes": "Extremely safe, non-irritating biomimetic ingredient compatible with all skin types including compromised barriers.",
        "source": "American Journal of Clinical Dermatology (2021) & CIR Report on Ceramides"
    },
    {
        "ingredient_name": "Zinc PCA",
        "aliases": ["zinc pyrrolidone carboxylic acid"],
        "function": "Zinc salt of L-pyrrolidone carboxylic acid (L-PCA) that suppresses 5-alpha-reductase to diminish excess sebum while inhibiting cutibacterium acnes proliferation.",
        "common_concerns": ["excess_oil", "acne", "clogged_pores"],
        "caution_notes": "Gentle sebum-regulator; generally non-drying compared to harsh alcohol astringents.",
        "source": "International Journal of Cosmetic Science (2017)"
    },
    {
        "ingredient_name": "Centella Asiatica",
        "aliases": ["cica", "gotu kola", "madecassoside", "asiaticoside"],
        "function": "Botanical extract rich in triterpenoid saponins that accelerates cutaneous wound healing, stimulates collagen synthesis, and suppresses pro-inflammatory cytokines.",
        "common_concerns": ["sensitivity", "redness", "acne", "barrier_repair"],
        "caution_notes": "Exceptional safety profile for reactive, rosacea-prone, and sensitized skin barriers.",
        "source": "Indian Journal of Dermatology (2019) & Advances in Dermatology and Allergology"
    },
    {
        "ingredient_name": "Glycolic Acid",
        "aliases": ["aha", "alpha hydroxy acid"],
        "function": "Smallest molecular weight AHA that breaks calcium ion bonds between corneocytes on the skin surface, accelerating desquamation and brightening dull complexion.",
        "common_concerns": ["dullness", "pigmentation", "rough_texture"],
        "caution_notes": "Significantly heightens UV sensitivity (photosensitivity); mandatory sun protection recommended. Can irritate eczema or compromised barriers.",
        "source": "Dermatologic Surgery (2018) & FDA Guidance on Topical AHAs"
    },
    {
        "ingredient_name": "Glycerin",
        "aliases": ["glycerol"],
        "function": "Primary low-molecular-weight trihydroxy alcohol humectant that maintains stratum corneum hydration and stabilizes aquaporin channels.",
        "common_concerns": ["dryness", "dehydration", "sensitivity"],
        "caution_notes": "Virtually non-sensitizing and non-comedogenic across human patch studies.",
        "source": "CIR Expert Panel Safety Assessment & Journal of Investigative Dermatology"
    },
    {
        "ingredient_name": "Panthenol",
        "aliases": ["provitamin b5", "d-panthenol", "pantolactone"],
        "function": "Provitamin precursor to coenzyme A, functioning as both humectant and deep tissue repair agent that relieves pruritus and erythema.",
        "common_concerns": ["sensitivity", "dryness", "barrier_repair", "redness"],
        "caution_notes": "Hypoallergenic and non-irritating; recognized as a gold-standard skin-soothing agent.",
        "source": "Journal of Dermatological Treatment & CIR Expert Panel"
    },
    {
        "ingredient_name": "Colloidal Oatmeal",
        "aliases": ["avena sativa kernel flour", "oat extract"],
        "function": "FDA-recognized skin protectant packed with avenanthramides, beta-glucan, and lipids that neutralize histamine pathways and restore compromised moisture barriers.",
        "common_concerns": ["sensitivity", "redness", "dryness", "barrier_repair"],
        "caution_notes": "Safe for eczema-prone and pediatric skin, though individuals with celiac-adjacent oat contact dermatitis should test first.",
        "source": "Journal of Drugs in Dermatology (2020) & FDA OTC Monograph on Skin Protectants"
    },
    {
        "ingredient_name": "Allantoin",
        "aliases": ["5-ureidohydantoin"],
        "function": "Keratolytic compound that softens keratin structures, encourages cell proliferation, and provides anti-irritant soothing effects against cleansing surfactants.",
        "common_concerns": ["sensitivity", "redness", "dryness"],
        "caution_notes": "Well tolerated and classified as a safe, effective skin protectant.",
        "source": "International Journal of Toxicology & CIR Safety Assessment"
    },
    {
        "ingredient_name": "Lactic Acid",
        "aliases": ["alpha hydroxy propionic acid"],
        "function": "Larger molecular weight AHA derived naturally from microbial fermentation that provides surface exfoliation while concurrently boosting the skin's Natural Moisturizing Factor (NMF).",
        "common_concerns": ["dullness", "rough_texture", "dryness"],
        "caution_notes": "Milder than glycolic acid due to larger particle size; causes mild photosensitivity requiring sunscreen.",
        "source": "Cosmetic Dermatology & Paula's Choice Skincare Dictionary"
    },
    {
        "ingredient_name": "Tea Tree Oil",
        "aliases": ["melaleuca alternifolia leaf oil"],
        "function": "Essential volatile oil containing high concentrations of terpinen-4-ol displaying broad-spectrum antimicrobial and anti-inflammatory activity against Cutibacterium acnes.",
        "common_concerns": ["acne", "excess_oil"],
        "caution_notes": "Can trigger contact dermatitis or sensitized reactions if oxidised or used at high concentrations (>5%). Avoid if sensitive to essential oils.",
        "source": "Clinical Microbiology Reviews (2016) & Australasian Journal of Dermatology"
    },
    {
        "ingredient_name": "Green Tea Extract",
        "aliases": ["camellia sinensis leaf extract", "epigallocatechin gallate", "egcg"],
        "function": "Polyphenol powerhouse rich in EGCG that scavenges free radicals, downregulates sebum synthesis enzymes, and mitigates UV-induced oxidative stress.",
        "common_concerns": ["excess_oil", "acne", "dullness", "sensitivity"],
        "caution_notes": "Extremely safe, soothing topical antioxidant with no known contraindications.",
        "source": "Oxidative Medicine and Cellular Longevity & CIR Assessment"
    },
    {
        "ingredient_name": "Kojic Acid",
        "aliases": ["kojic acid dipalmitate"],
        "function": "Naturally derived chelation agent from fungal fermentation that chelates copper in tyrosinase enzymes to impede melanin synthesis.",
        "common_concerns": ["pigmentation", "dullness"],
        "caution_notes": "Can cause mild contact irritation or photosensitivity. Maximum topical concentration generally advised at 1-2%.",
        "source": "CIR Expert Panel Safety Report on Kojic Acid (2021)"
    },
    {
        "ingredient_name": "Alpha Arbutin",
        "aliases": ["4-hydroxyphenyl alpha-glucoside"],
        "function": "Bio-synthetic glycoside that gradually hydrolyzes to release minimal, sustained hydroquinone equivalents, inhibiting tyrosinase without cytotoxicity.",
        "common_concerns": ["pigmentation", "dullness"],
        "caution_notes": "Much safer and gentler than raw hydroquinone; safe up to 2% in facial cleansers and leave-ons.",
        "source": "Scientific Committee on Consumer Safety (SCCS) Opinion & CIR"
    },
    {
        "ingredient_name": "Sulfates (SLS/SLES)",
        "aliases": ["sodium lauryl sulfate", "sodium laureth sulfate", "ammonium lauryl sulfate"],
        "function": "Anionic surfactants engineered to create voluminous foam and emulsify heavy oils and particulate soil on skin surfaces.",
        "common_concerns": ["excess_oil"],
        "caution_notes": "High cleansing power can strip stratum corneum lipid bilayers, leading to dryness, barrier disruption, and irritation in sensitive and dry skin types.",
        "source": "Contact Dermatitis Journal & CIR Safety Assessment of Sodium Lauryl Sulfate"
    },
    {
        "ingredient_name": "Fragrance / Parfum",
        "aliases": ["parfum", "aroma", "fragrance"],
        "function": "Complex mixture of volatile synthetic or natural aromatic compounds added exclusively for product sensorial smell.",
        "common_concerns": ["none"],
        "caution_notes": "Ranked among the leading causes of cosmetic contact allergy and dermatitis globally. Strongly contraindicated for reactive or sensitized skin.",
        "source": "American Contact Dermatitis Society (ACDS) & European Commission SCCS"
    },
    {
        "ingredient_name": "Denatured Alcohol",
        "aliases": ["alcohol denat.", "ethanol", "sd alcohol 40"],
        "function": "Volatile solvent used to create quick-drying aesthetics, degrease excessive skin oiliness, and enhance penetration of active ingredients.",
        "common_concerns": ["excess_oil"],
        "caution_notes": "Repeated exposure can dissolve epidermal barrier lipids, exacerbating transepidermal water loss and causing rebound sebum production.",
        "source": "Dermatologic Therapy & CIR Report on Alcohol Denat."
    },
    {
        "ingredient_name": "Parabens",
        "aliases": ["methylparaben", "propylparaben", "ethylparaben", "butylparaben"],
        "function": "Broad-spectrum antimicrobial preservatives protecting water-based formulations from fungal and bacterial contamination.",
        "common_concerns": ["none"],
        "caution_notes": "Safe within regulatory thresholds per toxicology reviews, though frequently flagged or avoided due to consumer preference and clean-beauty standards.",
        "source": "CIR Expert Panel Safety Assessment & FDA Review of Parabens in Cosmetics"
    },
    {
        "ingredient_name": "Witch Hazel",
        "aliases": ["hamamelis virginiana leaf water", "witch hazel extract"],
        "function": "Botanical astringent containing tannins that temporarily constrict skin surface pores and diminish surface oiliness.",
        "common_concerns": ["excess_oil", "acne"],
        "caution_notes": "Naturally occurring tannins and alcohol distillation can cause drying or sensitization with frequent daily application.",
        "source": "Journal of Inflammation & Paula's Choice Skincare Dictionary"
    },
    {
        "ingredient_name": "Coco-Glucoside",
        "aliases": ["coco glucoside", "decyl glucoside", "lauryl glucoside"],
        "function": "Non-ionic biodegradable surfactant derived from coconut oil and fruit sugars, providing exceptionally mild cleansing without stripping barrier lipids.",
        "common_concerns": ["sensitivity", "dryness"],
        "caution_notes": "Extremely low irritation index; widely favored for sensitive, dry, and pediatric formulations.",
        "source": "CIR Safety Assessment of Alkyl Glucosides & Contact Dermatitis"
    },
    {
        "ingredient_name": "Sodium Lauroyl Sarcosinate",
        "aliases": ["lauroyl sarcosinate"],
        "function": "Mild amino-acid derived surfactant that offers gentle lather and effective dirt removal without the barrier disruption of traditional sulfates.",
        "common_concerns": ["sensitivity", "dryness"],
        "caution_notes": "Significantly gentler than SLS, non-comedogenic and well-tolerated by barrier-compromised skin.",
        "source": "International Journal of Toxicology & CIR Panel Assessment"
    },
    {
        "ingredient_name": "Sodium Cocoyl Isethionate",
        "aliases": ["sci", "baby foam"],
        "function": "Ultra-gentle hydrophilic fatty acid surfactant renowned for creating rich creamy foam with near-zero skin barrier disruption.",
        "common_concerns": ["dryness", "sensitivity", "barrier_repair"],
        "caution_notes": "Considered the gold standard for non-drying bar and liquid cleansers (syndet formulations).",
        "source": "Cosmetic Dermatology Review & CIR Compendium"
    },
    {
        "ingredient_name": "Gluconolactone",
        "aliases": ["pha", "polyhydroxy acid"],
        "function": "Next-generation polyhydroxy acid (PHA) featuring multiple hydroxyl groups that exfoliate gently while actively binding moisture and strengthening barrier integrity.",
        "common_concerns": ["dullness", "rough_texture", "sensitivity"],
        "caution_notes": "Much less irritating than AHAs; does not cause significant UV sensitivity, making it suitable for sensitive skin.",
        "source": "Dermatologic Surgery (2019) & CIR Safety Assessment"
    },
    {
        "ingredient_name": "Benzoyl Peroxide",
        "aliases": ["bpo", "dibenzoyl peroxide"],
        "function": "Topical antibacterial medication that introduces oxygen into the pilosebaceous unit, effectively neutralizing anaerobic Cutibacterium acnes without bacterial resistance.",
        "common_concerns": ["acne"],
        "caution_notes": "Can bleach fabrics and causes noticeable dryness, erythema, and flaking in initial weeks. Mandatory patch test advised.",
        "source": "American Academy of Dermatology (AAD) Acne Clinical Guidelines"
    },
    {
        "ingredient_name": "Aloe Vera",
        "aliases": ["aloe barbadensis leaf juice", "aloe extract"],
        "function": "Botanical mucilage containing acemannan, vitamins, and enzymes providing instant cooling, soothing, and anti-erythema relief.",
        "common_concerns": ["sensitivity", "dryness", "redness"],
        "caution_notes": "Generally very safe and soothing; rare contact allergy reported in allergic individuals.",
        "source": "Phytotherapy Research & CIR Safety Assessment"
    },
    {
        "ingredient_name": "Vitamin C (Ascorbyl Glucoside / 3-O-Ethyl)",
        "aliases": ["ascorbyl glucoside", "ethyl ascorbic acid", "l-ascorbic acid"],
        "function": "Stable antioxidant derivative that inhibits tyrosinase activity to fade hyperpigmentation while protecting cell membranes from free radical damage.",
        "common_concerns": ["pigmentation", "dullness"],
        "caution_notes": "In cleansers, contact time is brief; derivatives are gentler than pure acidic L-ascorbic acid, causing minimal tingling.",
        "source": "Journal of Clinical and Aesthetic Dermatology (2019)"
    },
    {
        "ingredient_name": "Activated Charcoal",
        "aliases": ["charcoal powder", "carbon"],
        "function": "Porous carbon matrix that physically adsorbs micro-pollutants, excess sebum, and surface particulate matter from the skin.",
        "common_concerns": ["excess_oil", "clogged_pores"],
        "caution_notes": "Can feel drying if formulated in high quantities; recommended primarily for oily or congested complexions.",
        "source": "Journal of Cosmetic Science & Paula's Choice Skincare Dictionary"
    },
    {
        "ingredient_name": "Squalane",
        "aliases": ["hydrogenated squalene", "plant squalane"],
        "function": "100% saturated biocompatible hydrocarbon mimicking natural human sebum; reinforces the lipid barrier without clogging pores.",
        "common_concerns": ["dryness", "barrier_repair", "sensitivity"],
        "caution_notes": "Non-comedogenic, stable against oxidation, and exceptionally well-tolerated by all skin types.",
        "source": "Advances in Food and Nutrition Research & CIR Safety Assessment"
    },
    {
        "ingredient_name": "Azelaic Acid",
        "aliases": ["azelaic acid", "nonanedioic acid"],
        "function": "Dicarboxylic acid that reduces Cutibacterium acnes, downregulates hyperactive melanocytes, and calms follicular hyperkeratinization.",
        "common_concerns": ["acne", "pigmentation", "redness", "sensitivity"],
        "caution_notes": "Initial tingling or mild itching common; suitable for rosacea-prone skin per dermatological guidelines.",
        "source": "Journal of Clinical and Aesthetic Dermatology (2018) & JAAD Guidelines"
    },
    {
        "ingredient_name": "Licorice Root Extract",
        "aliases": ["glycyrrhiza glabra root extract", "glabridin", "dipotassium glycyrrhizate"],
        "function": "Botanical soothing agent containing glabridin, which disperses melanin and suppresses tyrosinase while offering potent anti-inflammatory relief.",
        "common_concerns": ["pigmentation", "dullness", "sensitivity", "redness"],
        "caution_notes": "Safe, gentle brightening botanical with no photosensitivity risk.",
        "source": "Pigment Cell & Melanoma Research & CIR Safety Assessment"
    },
    {
        "ingredient_name": "Vitamin E (Tocopherol)",
        "aliases": ["tocopherol", "tocopheryl acetate"],
        "function": "Primary lipid-soluble physiological antioxidant protecting sebum and barrier cell membranes from lipid peroxidation.",
        "common_concerns": ["dryness", "barrier_repair"],
        "caution_notes": "High pure tocopherol concentrations can rarely cause contact dermatitis in reactive skin; esters like tocopheryl acetate are gentler.",
        "source": "Free Radical Biology and Medicine & CIR Expert Panel"
    },
    {
        "ingredient_name": "Mugwort (Artemisia)",
        "aliases": ["artemisia princeps leaf extract", "artemisia vulgaris extract"],
        "function": "Traditional medicinal herb rich in flavonoids and artemisinin that suppresses cutaneous mast cell degranulation and calms redness.",
        "common_concerns": ["sensitivity", "redness", "acne"],
        "caution_notes": "Very gentle and calming; individuals with Compositae/Asteraceae pollen allergies should patch test.",
        "source": "Journal of Ethnopharmacology & International Journal of Molecular Sciences"
    },
    {
        "ingredient_name": "Bakuchiol",
        "aliases": ["psoralea corylifolia seed extract"],
        "function": "Meroterpene phenol plant alternative to retinol that upregulates types I and IV collagen gene expression without triggering retinoic acid irritation.",
        "common_concerns": ["rough_texture", "dullness", "pigmentation"],
        "caution_notes": "Photostable and far gentler than prescription retinoids; safe for daytime use.",
        "source": "British Journal of Dermatology (2019)"
    },
    {
        "ingredient_name": "Capryloyl Salicylic Acid (LHA)",
        "aliases": ["lha", "lipohydroxy acid"],
        "function": "Lipophilic salicylic acid derivative with an 8-carbon fatty acid chain providing slower, cell-by-cell micro-exfoliation inside sebaceous follicles.",
        "common_concerns": ["acne", "clogged_pores", "blackheads", "excess_oil"],
        "caution_notes": "Significantly gentler with lower irritation index than standard free salicylic acid.",
        "source": "Dermatologic Surgery (2017) & L'Oréal Research Publications"
    },
    {
        "ingredient_name": "Probiotics (Lactobacillus Ferment Lysate)",
        "aliases": ["lactobacillus ferment", "bifida ferment lysate"],
        "function": "Non-viable postbiotic fractions that reinforce cutaneous microbiome defense, stimulate antimicrobial peptides, and reduce transepidermal water loss.",
        "common_concerns": ["barrier_repair", "sensitivity", "acne"],
        "caution_notes": "Safe, non-live postbiotic ingredients suitable for reactive or compromised barriers.",
        "source": "Frontiers in Microbiology (2020) & International Journal of Cosmetic Science"
    },
    {
        "ingredient_name": "Zinc Sulfate / Zinc Gluconate",
        "aliases": ["zinc sulfate", "zinc gluconate"],
        "function": "Bioavailable zinc salts functioning as astringent and antimicrobial agents that reduce surface bacterial colonization and soothe inflammatory blemishes.",
        "common_concerns": ["acne", "excess_oil", "sensitivity"],
        "caution_notes": "Well-tolerated in rinse-off formulations without systemic absorption.",
        "source": "Dermatology Research and Practice & CIR Safety Assessment"
    },
    {
        "ingredient_name": "Sodium Cocoyl Glycinate",
        "aliases": ["cocoyl glycinate"],
        "function": "Amino-acid based mild surfactant derived from glycine and coconut oil fatty acids producing a dense, creamy foam with minimal stratum corneum swelling.",
        "common_concerns": ["sensitivity", "dryness"],
        "caution_notes": "Significantly less drying than alkyl ether sulfates; excellent barrier preservation.",
        "source": "Journal of Oleo Science & CIR Expert Panel"
    }
]

with open(DATA_DIR / "products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, indent=2)

with open(DATA_DIR / "ingredient_kb.json", "w", encoding="utf-8") as f:
    json.dump(ingredient_kb, f, indent=2)

print(f"Successfully generated {len(products)} products and {len(ingredient_kb)} ingredient KB entries.")
