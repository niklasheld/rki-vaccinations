from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import PERCENTAGE

from . import get_coordinator

SENSORS = {
    "vaccinated_one_shot_total": "mdi:shield-outline",
    "vaccinated_two_shots_total": "mdi:shield",
    "vaccinated_one_shot_percentage": "mdi:shield-outline",
    "vaccinated_two_shots_percentage": "mdi:shield",
    "doses_biontech": "mdi:needle",
    "doses_astrazeneca": "mdi:needle",
    "doses_moderna": "mdi:needle",
}


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Defer sensor setup to the shared sensor module."""
    coordinator = await get_coordinator(hass)

    async_add_entities(
        VaccinationSensor(coordinator, info_type) for info_type in SENSORS
    )


class VaccinationSensor(CoordinatorEntity):
    """Sensor representing corona virus data."""

    name = None
    unique_id = None

    def __init__(self, coordinator, info_type):
        """Initialize coronavirus sensor."""
        super().__init__(coordinator)
        self.name = f"Germany COVID {info_type}"
        self.unique_id = f"germany_covid_{info_type}"
        self.info_type = info_type

    @property
    def available(self):
        """Return if sensor is available."""
        return self.coordinator.last_update_success

    @property
    def state(self):
        """Return the state"""
        return getattr(self.coordinator.data, self.info_type)

    @property
    def icon(self):
        """Return the icon."""
        return SENSORS[self.info_type]

    @property
    def unit_of_measurement(self):
        """Return unit of measurement."""
        if "percent" in self.info_type:
            return PERCENTAGE
        return "people"
