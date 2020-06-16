# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Info(models.Model):
    name = models.CharField(max_length=128)
    region = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    vlan1 = models.CharField(db_column='Vlan1', max_length=128)  # Field name made lowercase.
    vlan10 = models.CharField(db_column='Vlan10', max_length=128)  # Field name made lowercase.
    model = models.CharField(max_length=128)
    opendate = models.CharField(db_column='OpenDate', max_length=128)  # Field name made lowercase.
    monidate = models.CharField(db_column='moniDate', max_length=128)  # Field name made lowercase.
    internet = models.CharField(max_length=128)
    adslusername = models.CharField(db_column='ADSLUsername', max_length=128)  # Field name made lowercase.
    adslpassword = models.CharField(db_column='ADSLPassword', max_length=128)  # Field name made lowercase.
    storenumber = models.CharField(db_column='storeNumber', max_length=128)  # Field name made lowercase.
    loopback = models.CharField(db_column='Loopback', max_length=128)  # Field name made lowercase.
    tunnelip = models.CharField(db_column='tunnelIP', max_length=128)  # Field name made lowercase.
    sn = models.CharField(db_column='SN', max_length=128)  # Field name made lowercase.
    mark = models.CharField(max_length=128)
    adslip = models.CharField(db_column='ADSLIP', max_length=128)  # Field name made lowercase.
    adslgateway = models.CharField(db_column='ADSLGateway', max_length=128)  # Field name made lowercase.
    tc51 = models.CharField(db_column='TC51', max_length=128)  # Field name made lowercase.
    dialupno = models.CharField(db_column='dialupNO', max_length=128)  # Field name made lowercase.
    modify_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'info'


class Devices(models.Model):
    storeno = models.IntegerField(db_column='storeNO', primary_key=True)  # Field name made lowercase.
    router = models.CharField(max_length=128)
    router_ip = models.CharField(max_length=128)
    is_aruba = models.CharField(max_length=128)
    ap_1 = models.CharField(max_length=128)
    ap_1_model = models.CharField(max_length=128)
    ap_1_version = models.CharField(max_length=128)
    ap_1_ip = models.CharField(max_length=128)
    ap_1_serial = models.CharField(max_length=128)
    ap_2 = models.CharField(max_length=128)
    ap_2_model = models.CharField(max_length=128)
    ap_2_version = models.CharField(max_length=128)
    ap_2_ip = models.CharField(max_length=128)
    ap_2_serial = models.CharField(max_length=128)
    ap_3 = models.CharField(max_length=128)
    ap_3_model = models.CharField(max_length=128)
    ap_3_version = models.CharField(max_length=128)
    ap_3_ip = models.CharField(max_length=128)
    ap_3_serial = models.CharField(max_length=128)
    ap_4 = models.CharField(max_length=128)
    ap_4_model = models.CharField(max_length=128)
    ap_4_version = models.CharField(max_length=128)
    ap_4_ip = models.CharField(max_length=128)
    ap_4_serial = models.CharField(max_length=128)
    ap_5 = models.CharField(max_length=128)
    ap_5_model = models.CharField(max_length=128)
    ap_5_version = models.CharField(max_length=128)
    ap_5_ip = models.CharField(max_length=128)
    ap_5_serial = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'devices'


class Contacts(models.Model):
    storeno = models.IntegerField(db_column='storeNO', primary_key=True)  # Field name made lowercase.
    region = models.CharField(max_length=128)
    telephone = models.CharField(max_length=128)
    regional_manager = models.CharField(max_length=128)
    regional_manager_phone = models.CharField(max_length=128)
    regional_it = models.CharField(max_length=128)
    regional_it_phone = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'contacts'
