class TravelMindError(Exception):
    pass


class CityNotSupportedError(TravelMindError):
    pass


class InvalidTripDataError(TravelMindError):
    pass
