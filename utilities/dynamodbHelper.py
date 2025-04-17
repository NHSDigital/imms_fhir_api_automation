import logging
logging.basicConfig(filename='debugLog.log', level=logging.INFO)
logger = logging.getLogger(__name__)

def diseaseTypeMapping(inputJSON):
    diseaseTypeCode = inputJSON['protocolApplied'][0]['targetDisease'][0]['coding'][0]['code']

    switch = {
        840539006: "COVID19",
        6142004: "FLU",
        55735004: "RSV",
    }

    return switch.get(int(diseaseTypeCode), "Invalid option")

    # COVID19 = "840539006"
    # flu: str = "6142004"
    # hpv: str = "240532009"
    # measles: str = "14189004"
    # mumps: str = "36989005"
    # rubella: str = "36653000"
    # rsv: str = "55735004"

# def switch_case(option):
#     switch = {
#         840539006: "COVID19",
#         6142004: "FLU",
#         55735004: "RSV",
#     }
#     return switch.get(option, "Invalid option")
