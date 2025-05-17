from src.objectModels.dataObjects import *

VACCINE_CODE_MAP = {
    "COVID": [
        Vaccine_code(system="http://snomed.info/sct", code="43111411000001101", display="Comirnaty JN.1 COVID-19 mRNA Vaccine 30micrograms/0.3ml dose dispersion for injection multidose vials (Pfizer Ltd)", manufacturer="Pfizer Ltd"),
        Vaccine_code(system="http://snomed.info/sct", code="43113211000001101", display="Comirnaty JN.1 Children 6 months - 4 years COVID-19 mRNA Vaccine 3micrograms/0.3ml dose concentrate for dispersion for injection multidose vials (Pfizer Ltd)", manufacturer="Pfizer Ltd"),
        Vaccine_code(system="http://snomed.info/sct", code="43112711000001100", display="Comirnaty JN.1 Children 5-11 years COVID-19 mRNA Vaccine 10micrograms/0.3ml dose dispersion for injection single dose vials (Pfizer Ltd)", manufacturer="Pfizer Ltd"),
        Vaccine_code(system="http://snomed.info/sct", code="42985911000001104", display="Spikevax JN.1 COVID-19 mRNA Vaccine 0.1mg/ml dispersion for injection multidose vials (Moderna, Inc)", manufacturer="Moderna, Inc")
    
    ],
    "FLU": [
        Vaccine_code(system="http://snomed.info/sct", code="34680411000001107", display= "Quadrivalent influenza vaccine (split virion, inactivated) suspension for injection 0.5ml pre-filled syringes (Sanofi Pasteur)", manufacturer="Sanofi Pasteur"),
       
    ],
    "RSV": [
        Vaccine_code(system="http://snomed.info/sct", code="42223111000001107", display="Arexvy vaccine powder and suspension for suspension for injection 0.5ml vials (GlaxoSmithKline UK Ltd)", manufacturer="GlaxoSmithKline UK Ltd"),
        Vaccine_code(system="http://snomed.info/sct", code="42605811000001109", display="Abrysvo vaccine powder and solvent for solution for injection 0.5ml vials (Pfizer Ltd)", manufacturer="Pfizer Ltd")
    ]
}


VACCINATION_PROCEDURE_MAP = {
    "COVID": [
        Coding(system="http://snomed.info/sct", code="1362591000000103" , display= "Immunisation course to maintain protection against SARS-CoV-2 (severe acute respiratory syndrome coronavirus 2)")
    ],
    "FLU": [
        Coding(system="http://snomed.info/sct", code="884861000000100"  , display="Seasonal influenza vaccination (procedure)")
    ],
    "RSV": [
        Coding(system="http://snomed.info/sct", code="1303503001", display="Administration of RSV (respiratory syncytial virus) vaccine")
    ]
}

SITE_MAP = [
    Coding(system="http://snomed.info/sct", code="368208006", display="Left upper arm structure"),
    Coding(system="http://snomed.info/sct", code="368209003", display="Right upper arm structure ")
]


ROUTE_MAP = [
    Coding(system="http://snomed.info/sct", code="78421000", display="Intramuscular"),
    Coding(system="http://snomed.info/sct", code="34206005", display="Subcutaneous route (qualifier value)")
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
    Coding(system="http://snomed.info/sct", code="443684005", display="Disease outbreak (event)"),
    Coding(system="http://snomed.info/sct", code="310578008", display="Routine immunization schedule" )
]

PROTOCOL_DISEASE_MAP ={ 
    "COVID":[
        Coding( system="http://snomed.info/sct", code="840539006", display="Disease caused by severe acute respiratory syndrome coronavirus 2 (disorder)" ),
        Coding( system="http://snomed.info/sct", code="6142004", display="Influenza caused by Influenza virus (disorder)" )
    ],
    "FLU":[
        Coding( system="http://snomed.info/sct", code="840539006", display="Disease caused by severe acute respiratory syndrome coronavirus 2 (disorder)" ),
    ],
    "RSV":[
        Coding( system="http://snomed.info/sct", code="55735004", display="Respiratory syncytial virus infection (disorder)" ),
           ]
}





