from src.objectModels.api_data_objects import *

VACCINE_CODE_MAP = {
    "COVID19": [
        {
            "system": "http://snomed.info/sct",
            "code": "43111411000001101",
            "display": "Comirnaty JN.1 COVID-19 mRNA Vaccine 30micrograms/0.3ml dose dispersion for injection multidose vials (Pfizer Ltd)",
            "stringValue": "Comirnaty JN.1 COVID-19 mRNA Vaccine 30micrograms/0.3ml dose dispersion for injection multidose vials",
            "idValue": "4311141100001101",
            "manufacturer": "Pfizer Ltd"
        },
        {
            "system": "http://snomed.info/sct",
            "code": "43113211000001101",
            "display": "Comirnaty JN.1 Children 6 months - 4 years COVID-19 mRNA Vaccine 3micrograms/0.3ml dose concentrate for dispersion for injection multidose vials (Pfizer Ltd)",
            "stringValue": "Comirnaty JN.1 Children 6 months - 4 years COVID-19 mRNA Vaccine 3micrograms/0.3ml dose concentrate for dispersion for injection multidose vials",
            "idValue": "4311321100001101",
            "manufacturer": "Pfizer Ltd"
        },
        {
            "system": "http://snomed.info/sct",
            "code": "43112711000001100",
            "display": "Comirnaty JN.1 Children 5-11 years COVID-19 mRNA Vaccine 10micrograms/0.3ml dose dispersion for injection single dose vials (Pfizer Ltd)",
            "stringValue": "Comirnaty JN.1 Children 5-11 years COVID-19 mRNA Vaccine 10micrograms/0.3ml dose dispersion for injection single dose vials",
            "idValue": "431127110001100",
            "manufacturer": "Pfizer Ltd"
        },
        {
            "system": "http://snomed.info/sct",
            "code": "42985911000001104",
            "display": "Spikevax JN.1 COVID-19 mRNA Vaccine 0.1mg/ml dispersion for injection multidose vials (Moderna, Inc)",
            "stringValue": "Spikevax JN.1 COVID-19 mRNA Vaccine 0.1mg/ml dispersion for injection multidose vials",
            "idValue": "4298591100001104",
            "manufacturer": "Moderna, Inc"
        }
    ],
    "FLU": [
        {
            "system": "http://snomed.info/sct",
            "code": "34680411000001107",
            "display": "Quadrivalent influenza vaccine (split virion, inactivated) suspension for injection 0.5ml pre-filled syringes (Sanofi Pasteur)",
            "stringValue": "Quadrivalent influenza vaccine (split virion, inactivated) suspension for injection 0.5ml pre-filled syringes",
            "idValue": "3468041100001107",
            "manufacturer": "Sanofi Pasteur"
        }
    ],
    "RSV": [
        {
            "system": "http://snomed.info/sct",
            "code": "42223111000001107",
            "display": "Arexvy vaccine powder and suspension for suspension for injection 0.5ml vials (GlaxoSmithKline UK Ltd)",
            "stringValue": "Arexvy vaccine powder and suspension for suspension for injection 0.5ml vials",
            "idValue": "4222311100001107",
            "manufacturer": "GlaxoSmithKline UK Ltd"
        },
        {
            "system": "http://snomed.info/sct",
            "code": "42605811000001109",
            "display": "Abrysvo vaccine powder and solvent for solution for injection 0.5ml vials (Pfizer Ltd)",
            "stringValue": "Abrysvo vaccine powder and solvent for solution for injection 0.5ml vials",
            "idValue": "4260581100001109",
            "manufacturer": "Pfizer Ltd"
        }
    ],
    "HPV": [
        {
            "system": "http://snomed.info/sct",
            "code": "12238911000001100",
            "display": "Cervarix vaccine suspension for injection 0.5ml pre-filled syringes (GlaxoSmithKline) (product)",
            "stringValue": "Gardasil 9 suspension for injection 0.5ml pre-filled syringes",
            "idValue": "12238911000001100",  
            "manufacturer": "GlaxoSmithKline"    
        },
        {
            "system": "http://snomed.info/sct",
            "code": "33493111000001108",
            "display": "Gardasil 9 vaccine suspension for injection 0.5ml pre-filled syringes (Merck Sharp & Dohme (UK) Ltd) (product)",
            "stringValue": "Gardasil 9 suspension for injection 0.5ml pre-filled syringes",
            "idValue": "33493111000001108",  
            "manufacturer": "Merck Sharp & Dohme (UK) Ltd"    
        },
        {
            "system": "http://snomed.info/sct",
            "code": "10880211000001104",
            "display": "Gardasil vaccine suspension for injection 0.5ml pre-filled syringes (Merck Sharp & Dohme (UK) Ltd) (product)",
            "stringValue": "Gardasil 9 suspension for injection 0.5ml pre-filled syringes",
            "idValue": "10880211000001104",  
            "manufacturer": "Merck Sharp & Dohme (UK) Ltd"    
        }
    ] ,
    "MENACWY":[
        {
            "system": "http://snomed.info/sct",
            "code": "39779611000001104",    
            "display": "MenQuadfi vaccine solution for injection 0.5ml vials (Sanofi) (product)",
            "stringValue": "MenQuadfi vaccine solution for injection 0.5ml vials",
            "idValue": "3977961100001104",
            "manufacturer": "Sanofi"
        },
        {
            "system": "http://snomed.info/sct",
            "code": "20517811000001104",    
            "display": "Nimenrix vaccine powder and solvent for solution for injection 0.5ml pre-filled syringes (GlaxoSmithKline UK Ltd) (product)",
            "stringValue": "Nimenrix vaccine powder and solvent for solution for injection 0.5ml pre-filled syringes",
            "idValue": "20517811000001104",
            "manufacturer": "GlaxoSmithKline UK Ltd"
        }
        ,
        {
            "system": "http://snomed.info/sct",
            "code": "17188711000001105",    
            "display": "Menveo vaccine powder and solvent for solution for injection 0.5ml vials (Novartis Vaccines and Diagnostics Ltd) (product)",
            "stringValue": "Menveo vaccine powder and solvent for solution for injection 0.5ml vials",
            "idValue": "17188711000001105",
            "manufacturer": "Novartis Vaccines and Diagnostics Ltd"
        }
    ],
    "3IN1":[
        {   
            "system": "http://snomed.info/sct",
            "code": "7374511000001107",
            "display": "Revaxis vaccine suspension for injection 0.5ml pre-filled syringes (Sanofi) 1 pre-filled disposable injection (product)",
            "stringValue": "Revaxis vaccine suspension for injection 0.5ml pre-filled syringes ",
            "idValue": "7374511000001107",
            "manufacturer": "Sanofi"
        },
    ],
    "MMR":[
        {   
            "system": "http://snomed.info/sct",
            "code": "7374511000001107",
            "display": "Revaxis vaccine suspension for injection 0.5ml pre-filled syringes (Sanofi) 1 pre-filled disposable injection (product)",
            "stringValue": "Revaxis vaccine suspension for injection 0.5ml pre-filled syringes ",
            "idValue": "7374511000001107",
            "manufacturer": "Sanofi"
        },
    ],
    "MMRV":[
        {   
            "system": "http://snomed.info/sct",
            "code": "7374511000001107",
            "display": "Revaxis vaccine suspension for injection 0.5ml pre-filled syringes (Sanofi) 1 pre-filled disposable injection (product)",
            "stringValue": "Revaxis vaccine suspension for injection 0.5ml pre-filled syringes ",
            "idValue": "7374511000001107",
            "manufacturer": "Sanofi"
        },
    ],
    "PERTUSSIS":[
        {   
            "system": "http://snomed.info/sct",
            "code": "7374511000001107",
            "display": "Revaxis vaccine suspension for injection 0.5ml pre-filled syringes (Sanofi) 1 pre-filled disposable injection (product)",
            "stringValue": "Revaxis vaccine suspension for injection 0.5ml pre-filled syringes ",
            "idValue": "7374511000001107",
            "manufacturer": "Sanofi"
        },
    ]
}



VACCINATION_PROCEDURE_MAP = {
    "COVID19": [
        {
            "system": "http://snomed.info/sct",
            "code": "1362591000000103",
            "display": "Immunisation course to maintain protection against SARS-CoV-2 (severe acute respiratory syndrome coronavirus 2)",
            "stringValue": "Immunisation course to maintain protection against severe acute respiratory syndrome coronavirus 2 (regime/therapy)",
            "idValue": "1362591000000103"
        },
        {
            "system": "http://snomed.info/sct",
            "code": "1362591000000103",
            "display": "Immunisation course to maintain protection against severe acute respiratory syndrome coronavirus 2 (regime/therapy)",
            "stringValue": "Immunisation course to maintain protection against severe acute respiratory syndrome coronavirus 2",
            "idValue": "1362591000000103"
        }
    ],
    "FLU": [
        {
            "system": "http://snomed.info/sct",
            "code": "884861000000100",
            "display": "Seasonal influenza vaccination (procedure)",
            "stringValue": "Administration of first intranasal seasonal influenza vaccination (procedure)",
            "idValue": "884861000000100"
        },
        {
            "system": "http://snomed.info/sct",
            "code": "884861000000100",
            "display": "Administration of first intranasal seasonal influenza vaccination (procedure)",
            "stringValue": "Seasonal influenza vaccination",
            "idValue": "884861000000100"
        }
    ],
    "RSV": [
        {
            "system": "http://snomed.info/sct",
            "code": "1303503001",
            "display": "Administration of RSV (respiratory syncytial virus) vaccine",
            "stringValue": "Administration of respiratory syncytial virus vaccine",
            "idValue": "1303503001"
        },
        {
            "system": "http://snomed.info/sct",
            "code": "1303503001",
            "display": "Administration of respiratory syncytial virus vaccine",
            "stringValue": "Administration of vaccine product containing only Human orthopneumovirus antigen",
            "idValue": "1303503001"
        }
    ],
    "HPV": [
        {
            "system": "http://snomed.info/sct",
            "code": "761841000",
            "display": "Administration of vaccine product containing only Human papillomavirus antigen (procedure)",
            "stringValue": "Administration of vaccine product containing only Human papillomavirus antigen",
            "idValue": "761841000"
        },
        {
            "system": "http://snomed.info/sct",
            "code": "761841000",
            "display": "Administration of vaccine product containing only Human papillomavirus antigen (procedure)",
            "stringValue": "Administration of vaccine product containing only Human papillomavirus antigen",
            "idValue": "761841000"
        }
    ],
    "MENACWY": [ 
        {
            "system": "http://snomed.info/sct",
            "code": "871874000",
            "display": "Administration of vaccine product containing only Neisseria meningitidis serogroup A, C, W135 and Y antigens (procedure)",
            "stringValue": "Administration of vaccine product containing only Neisseria meningitidis serogroup ",
            "idValue": "871874000"
        },
        {
            "system": "http://snomed.info/sct",
            "code": "871874000",
            "display": "Administration of vaccine product containing only Neisseria meningitidis serogroup A, C, W135 and Y antigens (procedure)",
            "stringValue": "Administration of vaccine product containing only Neisseria meningitidis serogroup ",
            "idValue": "871874000"
        }
    ],
    "MMR": [
        {
            "system": "http://snomed.info/sct",
            "code": "170433008",
            "display": "Administration of second dose of vaccine product containing only Measles morbillivirus and Mumps orthorubulavirus and Rubella virus antigens",
            "stringValue": "Administration of vaccine product containing only Measles virus and Mumps virus and Rubella virus antigens",
            "idValue": "866186002"
        },
         {
            "system": "http://snomed.info/sct",
            "code": "38598009",
            "display": "Administration of vaccine product containing only Measles morbillivirus and Mumps orthorubulavirus and Rubella virus antigens",
            "stringValue": "Administration of vaccine product containing only Measles virus and Mumps virus and Rubella virus antigens",
            "idValue": "8666002"
        }
    ],
    "MMRV": [
        {
            "system": "http://snomed.info/sct",
            "code": "432636005",
            "display": "Administration of vaccine product containing only Human alphaherpesvirus 3 and Measles morbillivirus and Mumps orthorubulavirus and Rubella virus antigens",
            "stringValue": "Administration of second dose of vaccine product containing only Human alphaherpesvirus 3 and Measles morbillivirus and Mumps orthorubulavirus and Rubella virus antigens",
            "idValue": "866182"
        },
        {
            "system": "http://snomed.info/sct",
            "code": "433733003",
            "display": "Administration of second dose of vaccine product containing only Human alphaherpesvirus 3 and Measles morbillivirus and Mumps orthorubulavirus and Rubella virus antigens",
            "stringValue": "Administration of vaccine product containing only Human alphaherpesvirus 3 and Measles morbillivirus and Mumps orthorubulavirus and Rubella virus antigens",
            "idValue": "86602"
        }
    ],
    "SHINGLES": [
        {   
            "system": "http://snomed.info/sct",
            "code": "722215002",
            "display": "Administration of vaccine product containing only Human alphaherpesvirus 3 antigen for shingles (procedure)",
            "stringValue": "Administration of vaccine product containing only Human alphaherpesvirus 3 antigen for shingles",
            "idValue": "4326365"
        },
    ],
    "3IN1": [
        {
            "system": "http://snomed.info/sct",
            "code": "414619005",
            "display": "Administration of vaccine product containing only Clostridium tetani and low dose Corynebacterium diphtheriae and inactivated Human poliovirus antigens",
            "stringValue": "Administration of vaccine product containing only Clostridium tetani and Corynebacterium diphtheriae and inactivated Human poliovirus antigens",
            "idValue": "866182"
        },
        {
            "system": "http://snomed.info/sct",
            "code": "866227002",
            "display": "Administration of booster dose of vaccine product containing only Clostridium tetani and Corynebacterium diphtheriae and Human poliovirus antigens",
            "stringValue": "Administration of vaccine product containing only Clostridium tetani and low dose Corynebacterium diphtheriae and inactivated Human poliovirus antigens",
            "idValue": "8662002"
        }
    ],
     "PERTUSSIS": [
        {   
            "system": "http://snomed.info/sct",
            "code": "722215002",
            "display": "Administration of vaccine product containing only Human alphaherpesvirus 3 antigen for shingles (procedure)",
            "stringValue": "Administration of vaccine product containing only Human alphaherpesvirus 3 antigen for shingles",
            "idValue": "4326365"
        },
    ]
    
}

SITE_MAP = [
    {
        "system": "http://snomed.info/sct",
        "code": "368208006",
        "display": "Left upper arm structure",
        "idValue": "36820006",
        "stringValue": "Left upper arm structure (body structure)"
    },
    {
        "system": "http://snomed.info/sct",
        "code": "368209003",
        "display": "Right upper arm structure",
        "idValue": "36820903",
        "stringValue": "Right upper arm structure (body structure)"
    }
]


ROUTE_MAP = [
    {
        "system": "http://snomed.info/sct",
        "code": "78421000",
        "display": "Intramuscular",
        "idValue": "7842100",
        "stringValue": "Intramuscular route (qualifier value)"
    },
    {
        "system": "http://snomed.info/sct",
        "code": "34206005",
        "display": "Subcutaneous route (qualifier value)",
        "idValue": "3420605",
        "stringValue": "Subcutaneous route (qualifier value)"
    }
]


DOSE_QUANTITY_MAP = [
    {
    "value": 0.3,
    "unit": "Inhalation - unit of product usage",
    "system": "http://snomed.info/sct",
    "code": "2622896019"
    }
]

REASON_CODE_MAP = [
    {
        "system": "http://snomed.info/sct",
        "code": "443684005",
        "display": "Disease outbreak (event)"
    },
    {
        "system": "http://snomed.info/sct",
        "code": "310578008",
        "display": "Routine immunization schedule"
    }
]

PROTOCOL_DISEASE_MAP = {
    "COVID19": [
        {
            "system": "http://snomed.info/sct",
            "code": "840539006",
            "display": "Disease caused by severe acute respiratory syndrome coronavirus 2"
        }
    ],
    "FLU": [
        {
            "system": "http://snomed.info/sct",
            "code": "6142004",
            "display": "Influenza"
        }
    ],
    "RSV": [
        {
            "system": "http://snomed.info/sct",
            "code": "55735004",
            "display": "Respiratory syncytial virus infection"
        }
    ],
    "HPV": [
        {
            "system": "http://snomed.info/sct",
            "code": "240532009",
            "display": "Human papillomavirus infection"
        }
    ],
    "MMR": [
        {
            "system": "http://snomed.info/sct",
            "code": "14189004",
            "display": "Measles"
        },
        {
            "system": "http://snomed.info/sct",
            "code": "36989005",
            "display": "Mumps"
        },
        {
            "system": "http://snomed.info/sct",
            "code": "36653000",
            "display": "Rubella"
        }        
    ],
    "MMRV": [
      {
            "system": "http://snomed.info/sct",
            "code": "14189004",
            "display": "Measles"
      },
      {
           "system": "http://snomed.info/sct",
            "code": "36989005",
            "display": "Mumps"
      },
      {
            "system": "http://snomed.info/sct",
            "code": "36653000",
            "display": "Rubella"
      },
      {
            "system": "http://snomed.info/sct",
            "code": "38907003",
            "display": "Varicella"
      }
    ],
    "PERTUSSIS": [
      {
            "system": "http://snomed.info/sct",
            "code": "27836007",
            "display": "Pertussis"
      }
    ],
     "SHINGLES": [
      {
            "system": "http://snomed.info/sct",
            "code": "4740000",
            "display": "Herpes zoster"
      }
    ],  
    "PCV13": [
      {
        "system": "http://snomed.info/sct",
        "code": "16814004",
        "display": "Pneumococcal infectious disease"
      }
    ],
    "3IN1": [
      {
        "system": "http://snomed.info/sct",
        "code": "398102009",
        "display": "Acute poliomyelitis"
      },
      {
        "system": "http://snomed.info/sct",
        "code": "397430003",
        "display": "Diphtheria caused by Corynebacterium diphtheriae"
      },
      {
        "system": "http://snomed.info/sct",
        "code": "76902006",
        "display": "Tetanus"
      }
    ],
    "MENACWY": [
      {
        "system": "http://snomed.info/sct",
        "code": "23511006",
        "display": "Meningococcal infectious disease"
      }
    ]    
}