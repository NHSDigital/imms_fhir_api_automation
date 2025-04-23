from datetime import datetime
import re

def dateToCSV(date_input):
    try:

        if ('T' in date_input) and (re.search(r'[+-]\d{2}:\d{2}$', date_input)):
            normalized_datetime = re.sub(r'([+-]\d{2}):(\d{2})', r'\1\2', date_input)

            if '.' in normalized_datetime:
                dt_obj = datetime.strptime(normalized_datetime, "%Y-%m-%dT%H:%M:%S.%f%z")
            else:    
                dt_obj = datetime.strptime(normalized_datetime, "%Y-%m-%dT%H:%M:%S%z")

            csvDate = dt_obj.strftime("%Y%m%dT%H%M%S%z")
            csvDate = re.sub(r'[+-]', '', csvDate)
            csvDate = re.sub(r'(\d{2})\d{2}$', r'\1', csvDate)
           
            return csvDate
                
        elif 'T' in date_input:
            if '.' in date_input:
                dt_obj = datetime.strptime(date_input, "%Y-%m-%dT%H:%M:%S.%f")
            else:
                dt_obj = datetime.strptime(date_input, "%Y-%m-%dT%H:%M:%S")

            csvDate = dt_obj.strftime("%Y%m%dT%H%M%S")

            return csvDate
        
        elif re.search(r'[+-]\d{2}:\d{2}$', date_input):
            dt_obj = datetime.strptime(date_input, "%Y-%m-%d%z")
            csvDate = dt_obj.strftime("%Y%m%d%z")
            csvDate = re.sub(r'[+-]', '', csvDate)
            csvDate = re.sub(r'(\d{2})\d{2}$', r'\1', csvDate)            

            return csvDate
        
        else:
            dt_obj = datetime.strptime(date_input, "%Y-%m-%d")
            csvDate = dt_obj.strftime("%Y%m%d")

            return csvDate
    except ValueError as e:
        return f"Error: Invalid date or datetime format ({e})"
    

def dateFieldCheck(dtInput, fieldName):
    if dtInput[:5] == "Error":
        return dtInput
    
    if fieldName.lower() == "recorded":
        csvDate = dtInput.strftime("%Y%m%d")
        return csvDate