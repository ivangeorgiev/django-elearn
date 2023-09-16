from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class UniqueKeyRelatedField(serializers.RelatedField):
    default_error_messages = {
        "required": _("This field is required."),
        "does_not_exist": _('Invalid value "{key_value}" for key "{key_name}" - object does not exist.'),
        "key_not_unique": _('Invalid value "{key_value}" for key "{key_name}" - value is not unique.'),
        "incorrect_type": _("Incorrect type. Expected pk value, received {data_type}."),
    }

    def __init__(self, *, lookup_field_name=None, key_field=None, **kwargs):
        self.lookup_field_name = lookup_field_name or "pk"
        self.key_field = key_field
        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False

    def to_internal_value(self, data):
        if self.key_field is not None:
            data = self.key_field.to_internal_value(data)
        queryset = self.get_queryset()
        try:
            if isinstance(data, bool):
                raise TypeError
            query_args = { self.lookup_field_name: data}
            return queryset.get(**query_args)
        except ObjectDoesNotExist:
            self.fail("does_not_exist", key_name=self.lookup_field_name, key_value=data)
        except MultipleObjectsReturned:
            self.fail("key_not_unique", key_name=self.lookup_field_name, key_value=data)
        except (TypeError, ValueError):
            self.fail("incorrect_type", data_type=type(data).__name__)

    def to_representation(self, value):
        raw_key_value = getattr(value, self.lookup_field_name)
        if self.key_field is not None:
            return self.key_field.to_representation(raw_key_value)
        return raw_key_value
