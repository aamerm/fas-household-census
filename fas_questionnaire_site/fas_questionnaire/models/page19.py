from django.db import models


class PublicDistributionSystem(models.Model):
    id = models.AutoField(primary_key=True)
    type_of_card = models.ForeignKey('TypeOfRationCard', db_column='type_of_card',on_delete= models.CASCADE, blank=True, null=True)
    color_of_card = models.ForeignKey('ColorOfCard',on_delete=models.CASCADE, db_column='color_of_card', blank=True, null=True)
    does_family_hold_ration_card = models.NullBooleanField()
    no_of_adults_on_card = models.IntegerField(blank=True, null=True)
    no_of_children_on_card = models.IntegerField(blank=True, null=True)
    reasons_for_not_having_card = models.CharField(max_length=255, blank=True, null=True)
    household = models.ForeignKey('Household',on_delete=models.CASCADE, db_column='household', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'public_distribution_system'


class TypeOfRationCard(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = True
        db_table = 'type_of_ration_card'

    def __str__(self):
        return self.type


class ColorOfCard(models.Model):
    id = models.AutoField(primary_key=True)
    color = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = True
        db_table = 'color_of_card'

    def __str__(self):
        return self.color


class WaterForDomesticUse(models.Model):
    id = models.AutoField(primary_key=True)
    source_of_water = models.ForeignKey('SourceOfWater', models.CASCADE, db_column='source_of_water', blank=True, null=True)
    ownership = models.ForeignKey('SourceOfWaterOwnership', models.CASCADE, db_column='ownership', blank=True, null=True)
    distance = models.ForeignKey('WaterSourceDistanceFromHouse', models.CASCADE, db_column='distance', blank=True, null=True)
    time_to_source = models.IntegerField(blank=True, null=True)
    months_water_available = models.CharField(max_length=100, blank=True, null=True)
    drinking = models.ForeignKey('PurposeForWhichUsed', models.CASCADE, db_column='drinking', blank=True, null=True, related_name='%(class)s_drinking')
    cooking = models.ForeignKey('PurposeForWhichUsed', models.CASCADE, db_column='cooking', blank=True, null=True, related_name='%(class)s_cooking')
    bathing_or_cleaning = models.ForeignKey('PurposeForWhichUsed', models.CASCADE, db_column='bathing_or_cleaning', blank=True, null=True, related_name='%(class)s_bathing_or_cleaning')
    for_animals = models.ForeignKey('PurposeForWhichUsed', models.CASCADE, db_column='for_animals', blank=True, null=True, related_name='%(class)s_for_animals')
    cost_payment = models.CharField(max_length=20, blank=True, null=True)
    restrictions = models.CharField(max_length=150, blank=True, null=True)
    comments = models.CharField(max_length=150, blank=True, null=True)
    household = models.ForeignKey('Household', models.CASCADE, db_column='household', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'water_for_domestic_use'


class SourceOfWater(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = True
        db_table = 'source_of_water'

    def __str__(self):
        return self.source


class SourceOfWaterOwnership(models.Model):
    id = models.AutoField(primary_key=True)
    ownership = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = True
        db_table = 'source_of_water_ownership'

    def __str__(self):
        return self.ownership


class WaterSourceDistanceFromHouse(models.Model):
    id = models.AutoField(primary_key=True)
    distance = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = True
        db_table = 'water_source_distance_from_house'

    def __str__(self):
        return self.distance


class PurposeForWhichUsed(models.Model):
    id = models.AutoField(primary_key=True)
    purpose = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = True
        db_table = 'purpose_for_which_used'

    def __str__(self):
        return self.purpose


class Housing(models.Model):
    id = models.AutoField(primary_key=True)
    owned_or_rented = models.ForeignKey('WhetherOwnedOrRented', models.CASCADE, db_column='owned_or_rented', blank=True, null=True)
    year_of_original_construction = models.CharField(max_length=50, blank=True, null=True)
    year_of_recent_repair = models.CharField(max_length=50, blank=True, null=True)
    verandah_present = models.ForeignKey('YesOrNo', db_column='verandah_present', blank=True, null=True, related_name='%(class)s_verandah_present')
    separate_kitchen = models.ForeignKey('YesOrNo', db_column='separate_kitchen', blank=True, null=True, related_name='%(class)s_separate_kitchen')
    additional_rooms = models.IntegerField(blank=True, null=True)
    type_of_roof = models.ForeignKey('TypeOfRoof', models.CASCADE, db_column='type_of_roof', blank=True, null=True)
    type_of_wall = models.ForeignKey('TypeOfWall', models.CASCADE, db_column='type_of_wall', blank=True, null=True)
    type_of_floor = models.ForeignKey('TypeOfFloor', models.CASCADE, db_column='type_of_floor', blank=True, null=True)
    latrine = models.ForeignKey('Latrine', models.CASCADE, db_column='latrine', blank=True, null=True)
    electricity = models.ForeignKey('ElectricityConnection', models.CASCADE, db_column='electricity', blank=True, null=True)
    energy_for_cooking = models.ForeignKey('SourceOfEnergyForCooking', models.CASCADE, db_column='energy_for_cooking', blank=True, null=True)
    if_provided_by_govt = models.ForeignKey('YesOrNo', db_column='if_provided_by_govt', blank=True, null=True, related_name='%(class)s_if_provided_by_govt')
    year_when_provided = models.CharField(max_length=10, blank=True, null=True)
    nature_of_disbursement = models.ForeignKey('NatureOfDisbursement', models.CASCADE, db_column='nature_of_disbursement', blank=True, null=True)
    amount_provided_in_cash = models.CharField(max_length=20, blank=True, null=True)
    comments = models.CharField(max_length=50, blank=True, null=True)
    household = models.ForeignKey('Household', models.CASCADE, db_column='household', blank=True, null=True)


class WhetherOwnedOrRented(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = True
        db_table = 'whether_owned_or_rented'

    def __str__(self):
        return self.type

class TypeOfRoof(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = True
        db_table = 'type_of_roof'

    def __str__(self):
        return self.type


class TypeOfWall(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = True
        db_table = 'type_of_wall'

    def __str__(self):
        return self.type


class TypeOfFloor(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = True
        db_table = 'type_of_floor'

    def __str__(self):
        return self.type


class Latrine(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = True
        db_table = 'latrine'

    def __str__(self):
        return self.type


class ElectricityConnection(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = True
        db_table = 'electricity_connection'

    def __str__(self):
        return self.type


class SourceOfEnergyForCooking(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = True
        db_table = 'source_of_energy_for_cooking'

    def __str__(self):
        return self.source


class NatureOfDisbursement(models.Model):
    id = models.AutoField(primary_key=True)
    nature = models.CharField(max_length=50, unique=True)

    class Meta:
        managed = True
        db_table = 'nature_of_disbursement'

    def __str__(self):
        return self.nature


class HousingComments(models.Model):
    id = models.AutoField(primary_key=True)
    comments = models.TextField(blank=True, null=True)
    household = models.ForeignKey('Household', models.CASCADE, db_column='household', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'housing_comments'
