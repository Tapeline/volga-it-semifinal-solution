import requests

from timetable_service import settings


class AccountService:
    def __init__(self, base_url=settings.ACCOUNT_SERVICE):
        self.base = base_url

    def doctor_exists(self, uid):
        response = requests.get(f"{self.base}/api/Accounts/Exists/Doctor/{uid}/")
        return response.status_code == 200 and response.json()["exists"]

    def user_exists(self, uid):
        response = requests.get(f"{self.base}/api/Accounts/Exists/User/{uid}/")
        return response.status_code == 200 and response.json()["exists"]


class HospitalService:
    def __init__(self, base_url=settings.HOSPITAL_SERVICE):
        self.base = base_url

    def hospital_exists(self, uid):
        response = requests.get(f"{self.base}/api/Hospitals/Exists/{uid}/")
        return response.status_code == 200 and response.json()["exists"]

    def hospital_room_exists(self, uid, room_name):
        response = requests.get(f"{self.base}/api/Hospitals/RoomExists/{uid}/{room_name}/")
        return response.status_code == 200 and response.json()["exists"]
