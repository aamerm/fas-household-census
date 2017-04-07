from django import forms
from ..models.ownership_wells_section9 import *


class OwnershipTypeForm(forms.ModelForm):

    class Meta:
        model = OwnershipType
        fields = ['type']
        exclude = []
        widgets = None
        localized_fields = None
        labels = {}
        help_texts = {}
        error_messages = {}


class WellTypeForm(forms.ModelForm):

    class Meta:
        model = WellType
        fields = ['type']
        exclude = []
        widgets = None
        localized_fields = None
        labels = {}
        help_texts = {}
        error_messages = {}


class PowerSourceForm(forms.ModelForm):

    class Meta:
        model = PowerSource
        fields = ['source']
        exclude = []
        widgets = None
        localized_fields = None
        labels = {}
        help_texts = {}
        error_messages = {}


class ExchangeNatureForm(forms.ModelForm):

    class Meta:
        model = ExchangeNature
        fields = ['exchange']
        exclude = []
        widgets = None
        localized_fields = None
        labels = {}
        help_texts = {}
        error_messages = {}


class OwnershipWellsTubewellsForm(forms.ModelForm):

    class Meta:
        model = OwnershipWellsTubewells
        fields = ['household', 'ownership_type', 'year_when_installed', 'present_depth', 'original_depth', 'type', 'power_source', 'installation_cost', 'finance_source', 'expenses_last_year', 'irrigation_crop', 'irrigation_sale_area', 'irrigation_revenue', 'exchange_nature', 'irrigation_land_extent', 'comments']
        exclude = ['household']
        widgets = None
        localized_fields = None
        labels = {}
        help_texts = {}
        error_messages = {}
