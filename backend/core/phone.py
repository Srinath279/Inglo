import phonenumbers
from fastapi import HTTPException

class  PhoneNumber:
    @staticmethod
    def validate_phone_number(potential_number: str, country_code: str) -> bool:
        try:
            phone_number_obj = phonenumbers.parse(f'+{country_code}{potential_number}')
            print(phone_number_obj)
        except phonenumbers.phonenumberutil.NumberParseException:
            return False
        if not phonenumbers.is_valid_number(phone_number_obj):
            raise HTTPException(status_code=404, detail="Invalid phone number")
        return f'+{country_code}{potential_number}'