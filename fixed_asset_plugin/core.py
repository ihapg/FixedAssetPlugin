"""Add Fixed Asset Parameter to every new Part created"""

import logging
from typing import Optional

from django.contrib.contenttypes.models import ContentType

from plugin import InvenTreePlugin
from plugin.mixins import EventMixin

from common.models import Parameter, ParameterTemplate
from part.models import Part

from . import PLUGIN_VERSION

logger = logging.getLogger(__name__)


class FixedAssetPlugin(EventMixin, InvenTreePlugin):

    """FixedAssetPlugin - custom InvenTree plugin."""

    # Plugin metadata
    TITLE = "Fixed Asset Plugin"
    NAME = "FixedAssetPlugin"
    SLUG = "fixed-asset-plugin"
    DESCRIPTION = "Add Fixed Asset Parameter to every new Part created"
    VERSION = PLUGIN_VERSION
    AUTHOR = "Adrian Piney Gutierrez"
    LICENSE = "MIT"

    # Variables
    TEMPLATE_NAME = "Fixed Asset"

    # InvenTree 1.2.0 replaced PartParameter / PartParameterTemplate
    # with the generic common.models.Parameter / ParameterTemplate
    MIN_VERSION = '1.2.0'

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(f"plugin.{self.SLUG}")

    def _get_template(self) -> Optional[ParameterTemplate]:
        """Look up the parameter template (lazily, so it is never stale)."""
        template = ParameterTemplate.objects.filter(name=self.TEMPLATE_NAME).first()

        if template is None:
            self.logger.error(f"Template '{self.TEMPLATE_NAME}' not found")

        return template

    def _get_part_from_event(self, *, args, kwargs) -> Optional[Part]:
        if kwargs.get('model') != 'Part':
            return None

        pid = kwargs.get('id')
        if pid is not None:
            return Part.objects.filter(pk=pid).first()
        return None

    # Respond to InvenTree events (from EventMixin)
    # Ref: https://docs.inventree.org/en/stable/extend/plugins/event/
    def wants_process_event(self, event: str) -> bool:
        """Return True if the plugin wants to process the given event."""
        return event == 'part_part.created'

    def process_event(self, event: str, *args, **kwargs) -> None:

        # Check de los args para comprobar datos
        self.logger.debug(f"fixed-asset-plugin args={args}, kwargs={kwargs}")

        part = self._get_part_from_event(args=args, kwargs=kwargs)

        if not part:
            self.logger.debug("Ignoring event: not a Part or not ID")
            return

        template = self._get_template()

        if not template:
            return

        if part.parameters_list.filter(template=template).exists():
            self.logger.debug(f"Part {part.pk} ya tiene '{template.name}'")
            return

        try:
            Parameter.objects.create(
                model_type=ContentType.objects.get_for_model(Part),
                model_id=part.pk,
                template=template,
                data="False",
            )
            self.logger.info(f"Added '{template.name}' parameter to Part {part.pk}")

        except Exception as e:
            self.logger.error(f"Error adding parameter: {e}")
