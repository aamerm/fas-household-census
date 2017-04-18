import functools
from django.forms import formset_factory, BaseFormSet, modelformset_factory
from django.shortcuts import get_object_or_404, render, redirect
from . import household as household
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..forms.page21 import *
from .common import *


@login_required(login_url='login')
def init(request):
    if request.session.get('household') is None:
        return new(request)
    else:
        asset_ownership_result_set = AssetOwnership.objects.filter(household=request.session.get('household'))
        if len(asset_ownership_result_set) == 0:
            return new(request)
        return edit(request, request.session['household'])


@login_required(login_url='login')
def new(request):
    immovables_form_set = formset_factory(ImmovableForm, formset=BaseFormSet, extra=5)
    meansOfTransport_form_set = formset_factory(MeansOfTransportForm, formset=BaseFormSet, extra=5)
    electricEquipments_form_set = formset_factory(ElectricEquipmentsForm, formset=BaseFormSet, extra=5)
    otherDomesticDurableGoods_form_set = formset_factory(OtherDomesticDurableGoodsForm, formset=BaseFormSet, extra=5)
    furniture_form_set = formset_factory(FurnitureForm, formset=BaseFormSet, extra=5)
    inventories_form_set = formset_factory(InventoriesForm, formset=BaseFormSet, extra=5)
    miscellaneous_form_set = formset_factory(MiscellaneousForm, formset=BaseFormSet, extra=5)

    if request.method == "POST":
        immovablesForms = immovables_form_set(request.POST, prefix='Immovables')
        meansOfTransportForms = meansOfTransport_form_set(request.POST, prefix='MeansOfTransport')
        furnitureForms = furniture_form_set(request.POST, prefix='Furniture')
        electricEquipmentsForms = electricEquipments_form_set(request.POST, prefix='ElectricEquipments')
        otherDomesticDurableGoodsForms = otherDomesticDurableGoods_form_set(request.POST,
                                                                            prefix='OtherDomesticDurableGoods')
        inventoriesForms = inventories_form_set(request.POST, prefix='Inventories')
        miscellaneousForms = miscellaneous_form_set(request.POST, prefix='Miscellaneous')

        assetOwnership_save = False
        if immovablesForms.is_valid() and meansOfTransportForms.is_valid() and \
                furnitureForms.is_valid() and \
                electricEquipmentsForms.is_valid() and \
                otherDomesticDurableGoodsForms.is_valid() and \
                inventoriesForms.is_valid() and \
                miscellaneousForms.is_valid():

            assetOwnership_save = save_forms(request, immovablesForms)
            assetOwnership_save = save_forms(request,meansOfTransportForms) or assetOwnership_save
            assetOwnership_save = save_forms(request, furnitureForms) or assetOwnership_save
            assetOwnership_save = save_forms(request, electricEquipmentsForms) or assetOwnership_save
            assetOwnership_save = save_forms(request,otherDomesticDurableGoodsForms) or assetOwnership_save
            assetOwnership_save = save_forms(request, inventoriesForms) or assetOwnership_save
            assetOwnership_save = save_forms(request, miscellaneousForms) or assetOwnership_save

            if assetOwnership_save:
                messages.success(request, 'Data saved successfully')
                return redirect('page21_edit', pk=request.session['household'])

    return render(request, 'page21.html',
                  {'immovables_form_set': immovables_form_set(prefix='Immovables'),
                   'meansoftransport_form_set':meansOfTransport_form_set(prefix='MeansOfTransport'),
                   'furniture_form_set':furniture_form_set(prefix='Furniture'),
                   'electricEquipments_form_set':electricEquipments_form_set(prefix='ElectricEquipments'),
                   'otherDomesticDurableGoods_form_set':otherDomesticDurableGoods_form_set(prefix='OtherDomesticDurableGoods'),
                   'inventories_form_set':inventories_form_set(prefix='Inventories'),
                   'miscellaneous_form_set':miscellaneous_form_set(prefix='Miscellaneous')})


def are_all_assetForms_valid(asset_forms_array):
    def add(x, y):
        return x and y
    return functools.reduce(add, list(map(lambda x:x.is_valid(),asset_forms_array)))

@login_required(login_url='login')
def edit(request, pk):
    try:
        request.session['household'] = pk  # TODO: temporary, remove when search functionality is implemented
        asset_array = {'ImmovablesForm':ImmovableForm, 'MeansOfTransportForm':MeansOfTransportForm, 'FurnitureForm':FurnitureForm,
                       'ElectricEquipmentsForm':ElectricEquipmentsForm,
                       'OtherDomesticDurableGoodsForm':OtherDomesticDurableGoodsForm,
                       'InventoriesForm':InventoriesForm,
                       'MiscellaneousForm':MiscellaneousForm}
        if request.method == "POST":
            asset_forms_array=[]
            assetOwnership_save=False
            for asset_prefix,asset_form in asset_array.items():
                asset_form_set = formset_factory(asset_form ,formset=BaseFormSet, extra=5)
                asset_forms_array.append(asset_form_set(request.POST, prefix=asset_prefix.rstrip('Form')))
            if are_all_assetForms_valid(asset_forms_array):
                for asset_form in asset_forms_array:
                    if asset_form.is_valid():
                        AssetOwnership.objects.filter(household=pk).delete()
                        assetOwnership_save=save_forms(request,asset_form) or assetOwnership_save
            if assetOwnership_save:
                messages.success(request, 'Data saved successfully')

        assetsetArray={}
        for asset_key,asset_value in asset_array.items():
            asset_model_form = modelformset_factory(AssetOwnership, form=asset_value, extra=5)
            # asset_result_set = AssetOwnership.objects.filter(household=pk,type_of_asset__in=[ x.id for x in AssetType.objects.filter(asset_category_id=AssetCategory.objects.get(asset_category=asset_key.rstrip('Form')).id) ])
            asset_result_set = AssetOwnership.objects.filter(household=pk,type_of_asset__in=[x.id for x in AssetType.objects.filter(asset_category_id=AssetCategory.objects.get(asset_category=asset_key.rstrip('Form')).id)])
            # asset_result_set=asset_category_id=AssetCategory.objects.get(asset_category="Miscellaneous").id)
            assetsetArray['_'.join(asset_key.split("Form")).lower()+"form_set"]=asset_model_form(queryset=asset_result_set,prefix=asset_key.rstrip('Form'))
        # self.fields['type_of_asset'].queryset =


        return render(request, 'page21.html',assetsetArray)
    except Exception:
        return new(request)


def get(household):
    try:
        assetOwnership = AssetOwnership.objects.get(household=household)

    except AssetOwnership.DoesNotExist:
        assetOwnership = None
    return assetOwnership
