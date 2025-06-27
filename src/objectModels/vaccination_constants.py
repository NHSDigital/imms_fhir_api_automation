from src.objectModels.dataObjects import *

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
            "display": "Disease caused by severe acute respiratory syndrome coronavirus 2 (disorder)"
        }
    ],
    "FLU": [
        {
            "system": "http://snomed.info/sct",
            "code": "6142004",
            "display": "Influenza caused by Influenza virus (disorder)"
        }
    ],
    "RSV": [
        {
            "system": "http://snomed.info/sct",
            "code": "55735004",
            "display": "Respiratory syncytial virus infection (disorder)"
        }
    ]
}

ERROR_MAP = {
    "Common_field": {
        "resourceType": "OperationOutcome",
        "profile": "https://simplifier.net/guide/UKCoreDevelopment2/ProfileUKCore-OperationOutcome",
        "system": "https://fhir.nhs.uk/Codesystem/http-error-codes",
    },
    "invalid_NHSNumber": {
        "issue_code": "invariant",
        "severity": "error",
        "code": "INVARIANT",
        "diagnostics": "Validation errors: contained[?(@.resourceType=='Patient')].identifier[0].value does not exists."
    },
    "invalid_DiseaseType": {
        "issue_code": "invalid",
        "severity": "error",
        "code": "INVALID",
        "diagnostics": "immunization-target must be one or more of the following: COVID19,FLU,HPV,MMR,RSV"
    },
    "invalid_DateFrom": {
        "issue_code": "invalid",
        "severity": "error",
        "code": "INVALID",
        "diagnostics": "Search parameter -date.from must be in format: YYYY-MM-DD"
    }, 
    "invalid_DateTo": {
        "issue_code": "invalid",
        "severity": "error",
        "code": "INVALID",
        "diagnostics": "Search parameter -date.to must be in format: YYYY-MM-DD"
    },        
}

