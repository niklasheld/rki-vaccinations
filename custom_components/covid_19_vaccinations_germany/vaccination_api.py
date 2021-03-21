from aiohttp import ClientSession
from dataclasses import dataclass
import csv


@dataclass
class VaccinationData:
    """Class for holding data about vaccinations"""

    vaccinated_one_shot_total: int
    vaccinated_one_shot_percentage: float
    vaccinated_two_shots_total: int
    vaccinated_two_shots_percentage: float
    doses_biontech: int
    doses_astrazeneca: int
    doses_moderna: int

    @staticmethod
    def from_timeseries(item):

        csv_file = csv.DictReader(
            item.splitlines(), delimiter="\t", lineterminator="\n"
        )

        new_data = list(csv_file)[-1]

        return VaccinationData(
            vaccinated_one_shot_total=new_data["personen_erst_kumulativ"],
            vaccinated_one_shot_percentage=float(new_data["impf_quote_erst"]) * 100,
            vaccinated_two_shots_total=new_data["personen_voll_kumulativ"],
            vaccinated_two_shots_percentage=float(new_data["impf_quote_voll"]) * 100,
            doses_biontech=new_data["dosen_biontech_kumulativ"],
            doses_astrazeneca=new_data["dosen_astrazeneca_kumulativ"],
            doses_moderna=new_data["dosen_moderna_kumulativ"],
        )


async def get_vaccination_stats(session: ClientSession):
    """Fetch vacination progress data"""

    url = (
        "https://impfdashboard.de/data/germany_vaccinations_timeseries_v2.9427d633.tsv"
    )

    async with session.get(url) as resp:
        return VaccinationData.from_timeseries(await resp.text())
