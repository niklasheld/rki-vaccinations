import csv
from dataclasses import dataclass
from aiohttp import ClientSession


@dataclass
class VaccinationData:
    """Class for holding data about vaccinations"""

    vaccinated_one_shot_total: int = None
    vaccinated_one_shot_percentage: float = None
    vaccinated_two_shots_total: int = None
    vaccinated_two_shots_percentage: float = None
    doses_biontech: int = None
    doses_astrazeneca: int = None
    doses_moderna: int = None
    delivered_biontech: int = None
    delivered_astrazeneca: int = None
    delivered_moderna: int = None
    delivered_total: int = None
    stock_total: int = None
    stock_biontech: int = None
    stock_astrazeneca: int = None
    stock_moderna: int = None

    @staticmethod
    def from_timeseries(tsv_vaccinations, tsv_deliveries):

        vaccinations = csv.DictReader(
            tsv_vaccinations.splitlines(), delimiter="\t", lineterminator="\n"
        )
        vaccinations = list(vaccinations)[-1]

        deliveries = csv.DictReader(
            tsv_deliveries.splitlines(), delimiter="\t", lineterminator="\n"
        )
        deliveries = list(deliveries)

        def delivered_vaccinations_sum(deliveries, vaccination_type: str):
            return sum(
                int(delivery["dosen"])
                for delivery in deliveries
                if delivery["impfstoff"] == vaccination_type
            )

        result = VaccinationData()

        result.vaccinated_one_shot_total = int(vaccinations["personen_erst_kumulativ"])
        result.vaccinated_one_shot_percentage = (
            float(vaccinations["impf_quote_erst"]) * 100
        )
        result.vaccinated_two_shots_total = int(vaccinations["personen_voll_kumulativ"])
        result.vaccinated_two_shots_percentage = (
            float(vaccinations["impf_quote_voll"]) * 100
        )

        result.doses_biontech = int(vaccinations["dosen_biontech_kumulativ"])
        result.doses_astrazeneca = int(vaccinations["dosen_astrazeneca_kumulativ"])
        result.doses_moderna = int(vaccinations["dosen_moderna_kumulativ"])

        result.delivered_biontech = delivered_vaccinations_sum(deliveries, "comirnaty")
        result.delivered_astrazeneca = delivered_vaccinations_sum(deliveries, "astra")
        result.delivered_moderna = delivered_vaccinations_sum(deliveries, "moderna")
        result.delivered_total = (
            result.delivered_biontech
            + result.delivered_astrazeneca
            + result.delivered_moderna
        )

        result.stock_total = (
            result.delivered_total
            - result.vaccinated_one_shot_total
            - result.vaccinated_two_shots_total
        )
        result.stock_biontech = result.delivered_biontech - result.doses_biontech
        result.stock_astrazeneca = (
            result.delivered_astrazeneca - result.doses_astrazeneca
        )
        result.stock_moderna = result.delivered_moderna - result.doses_moderna

        return result


async def get_vaccination_stats(session: ClientSession):
    """Fetch vacination progress data"""

    url_vaccinations = (
        "https://impfdashboard.de/data/germany_vaccinations_timeseries_v2.9427d633.tsv"
    )

    url_deliveries = (
        "https://impfdashboard.de/data/germany_deliveries_timeseries_v2.5aef0f71.tsv"
    )

    async with session.get(url_vaccinations) as resp_vaccination:
        vaccinations = await resp_vaccination.text()

    async with session.get(url_deliveries) as resp_deliveries:
        deliveries = await resp_deliveries.text()

    return VaccinationData.from_timeseries(vaccinations, deliveries)
