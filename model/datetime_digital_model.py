import time


class DateTimeDigitalModel:
    def get_current_date_time(self) -> list[str]:
        return [time.strftime("%H%M"), time.strftime("%m/%d"), time.strftime("%a")]
