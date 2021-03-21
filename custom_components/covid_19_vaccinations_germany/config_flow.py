"""Config flow for COVID-19 Vaccinations Germany integration."""

from homeassistant import config_entries

from .const import DOMAIN


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Coronavirus."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    _options = None

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""

        await self.async_set_unique_id("covid19_vaccinations_germany")
        self._abort_if_unique_id_configured()
        return self.async_create_entry(
            title="COVID-19 Vaccinations in Germany", data={}
        )
