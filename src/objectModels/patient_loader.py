import csv
from src.objectModels.dataObjects import Identifier, HumanName, Address, Patient

csv_path = "input/testData.csv"

def load_patient_by_id(id: str) -> Patient:
    """
    Load a patient's details from a CSV file by NHS number.
    """
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["id"] == id:
                nhs_number = row.get("nhs_number", "").strip()
                nhs_number = None if not nhs_number or nhs_number.lower() in ["null", "none"] else nhs_number

                identifier = Identifier(
                    system="https://fhir.nhs.uk/Id/nhs-number",
                    value=nhs_number
                )

                name = HumanName(
                    family=row["family_name"],
                    given=[row["given_name"]]
                )

                address = Address(
                    use="Home",
                    type="Postal",
                    text="Validate Obf",
                    line=[row["address_line"]],
                    city=row["city"],
                    district=row["district"],
                    state=row["state"],
                    postalCode=row["postal_code"],
                    country=row["country"],
                    period={"start": "2000-01-01", "end": "2030-01-01"}
                )

                return Patient(
                    identifier=[identifier],
                    name=[name],
                    gender=row["gender"],
                    birthDate=row["birth_date"],
                    address=[address]
                )

    raise ValueError(f"NHS number {id} not found in {csv_path}")
