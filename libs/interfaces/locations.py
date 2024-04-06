from enum import Enum


class IsraelRegions(Enum):
    JERUSALEM = "מחוז ירושלים"
    NORTH = "מחוז הצפון"
    SOUTH = "מחוז הדרום"
    HAIFA = "מחוז חיפה"
    TEL_AVIV = "מחוז תל אביב"
    NATIONAL = "ארצי - מרחוק"
    CENTER = "מחוז המרכז"

    def __str__(self):
        return self.value

    @staticmethod
    def get_regions():
        return [region.value for region in IsraelRegions]

    def center_city(self):
        city_to_region = {
            IsraelRegions.JERUSALEM: "ירושלים",
            IsraelRegions.NORTH: "טבריה",
            IsraelRegions.SOUTH: "באר שבע",
            IsraelRegions.HAIFA: "חיפה",
            IsraelRegions.TEL_AVIV: "תל אביב - יפו",
            IsraelRegions.CENTER: "ראשון לציון",
        }

        return city_to_region.get(self, "")
