from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import ModelForm
from django import forms
from ckeditor.fields import RichTextField 

# Create your models here.
class Amenity(models.Model):
    name = models.CharField(max_length=50)
    description = RichTextField(blank=True)
    active = models.BooleanField()
    image = models.ImageField(blank=True, null=True, upload_to='images/amenity/')

    def __str__(self):
        return self.name

    def serialize(self):
        url = ''
        if (self.image):
            url = self.image.url
        return {
            'pk': self.pk,
            'name': self.name,
            'description': self.description,
            'active' :self.active,
            'image' : url,
        }

class AmenityForm(ModelForm):
    class Meta:
        model = Amenity
        fields = '__all__'

class Room_Type(models.Model):
    title = models.CharField(max_length=50)
    short_code = models.CharField(max_length=25)
    description = RichTextField(blank=True)
    base_occupancy = models.IntegerField()
    max_occupancy = models.IntegerField()
    extra_bed = models.IntegerField()
    kids_occupancy = models.IntegerField()
    amenities = models.ManyToManyField(Amenity, blank=True)
    base_price = models.IntegerField()
    additional_person_price = models.IntegerField()
    extra_bed_price = models.IntegerField()
    image = models.ImageField(blank=True, null=True, upload_to='images/room_types/')

    def __str__(self):
        return self.title

    def serialize(self):
        url = ''
        if (self.image):
            url = self.image.url
        amenities = []
        if self.amenities.count() != 0:
            for x in self.amenities.all():
                if x.active:
                    amenities.append(x.pk)
        return {
            'pk': self.pk,
            'title': self.title, 
            'short_code': self.short_code,
            'description': self.description,
            'base_occupancy': self.base_occupancy,
            'max_occupancy': self.max_occupancy,
            'extra_bed' : self.extra_bed,
            'kids_occupancy': self.kids_occupancy,
            'amenities': amenities,
            'base_price': self.base_price,
            'additional_person_price': self.additional_person_price,
            'extra_bed_price': self.extra_bed_price,
            'image': url,
        }

def get_my_choices():
    available_choices = []
    for x in Amenity.objects.filter(active=True).all():
        available_choices.append((x.pk,x.name))
    return available_choices

class Room_TypeForm(ModelForm):

    amenities = forms.MultipleChoiceField(
        widget= forms.CheckboxSelectMultiple,
        choices= get_my_choices
    )
        
    class Meta:
        model = Room_Type
        fields = '__all__'

class Floor(models.Model):
    name = models.CharField(max_length=50)
    number = models.IntegerField(unique=True)
    description = RichTextField(blank=True)
    active = models.BooleanField()

    def __str__(self):
        return f'{self.number} - {self.name}'

    def serialize(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'number': self.number,
            'description': self.description,
            'active' :self.active,
        }

class FloorForm(ModelForm):
    class Meta:
        model = Floor
        fields = '__all__'

class Room(models.Model):
    room_type = models.ForeignKey(Room_Type, on_delete=models.CASCADE)
    floor = models.ForeignKey(Floor,on_delete=models.CASCADE)
    room_number = models.IntegerField(unique=True)

    def __str__(self):
        return self.room_number

    def serialize(self):
        return {
            'pk': self.pk,
            'room_type': self.room_type.title,
            'room_type_pk': self.room_type.pk,
            'floor': f'{self.floor.number} - {self.floor.name}',
            'floor_pk': self.floor.pk,
            'room_number': self.room_number,
        }

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class Positions(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField(blank=True)

    def __str__(self):
        return self.name

    def serialize(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'description': self.description,
        }

class PositionsForm(ModelForm):
    class Meta:
        model = Positions
        fields = '__all__'

class Departments(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField(blank=True)
    
    def __str__(self):
        return self.name
    
    def serialize(self):
        return {
            'pk': self.pk,
            'name': self.name,
            'description': self.description,
        }

class DepartmentsForm(ModelForm):
    class Meta:
        model = Departments
        fields = '__all__'

class User_permission(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Employee(AbstractUser):
    TITLE_CHOICES = (
        ('Mr', 'Mr'),
        ('Mrs', 'Mrs'),
        ('Miss', 'Miss'),
        ('Ms', 'Ms'),
        ('Dr', 'Dr'),
    )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    CALLING_CODE_CHOICES = (
        (44, 'United Kingdom +44'),
        (93, 'Afghanistan +93'),
        (355, 'Albania +355'),
        (213, 'Algeria +213'),
        (1, 'American Samoa +1'),
        (376, 'Andorra +376'),
        (244, 'Angola +244'),
        (1, 'Anguilla +1'),
        (1, 'Antigua and Barbuda +1'),
        (54, 'Argentina +54'),
        (374, 'Armenia +374'),
        (297, 'Aruba +297'),
        (61, 'Australia +61'),
        (43, 'Austria +43'),
        (994, 'Azerbaijan +994'),
        (1, 'Bahamas +1'),
        (973, 'Bahrain +973'),
        (880, 'Bangladesh +880'),
        (1, 'Barbados +1'),
        (375, 'Belarus +375'),
        (32, 'Belgium +32'),
        (501, 'Belize +501'),
        (229, 'Benin +229'),
        (1, 'Bermuda +1'),
        (975, 'Bhutan +975'),
        (591, 'Bolivia +591'),
        (387, 'Bosnia and Herzegovina +387'),
        (267, 'Botswana +267'),
        (55, 'Brazil +55'),
        (673, 'Brunei Darussalam +673'),
        (359, 'Bulgaria +359'),
        (226, 'Burkina Faso +226'),
        (257, 'Burundi +257'),
        (855, 'Cambodia +855'),
        (237, 'Cameroon +237'),
        (1, 'Canada +1'),
        (238, 'Cape Verde +238'),
        (236, 'Central African Republic +236'),
        (235, 'Chad +235'),
        (56, 'Chile +56'),
        (86, 'China +86'),
        (57, 'Colombia +57'),
        (269, 'Comoros +269'),
        (242, 'Congo (Brazzaville) +242'),
        (243, 'Congo (Kinshasa) +243'),
        (506, 'Costa Rica +506'),
        (385, 'Croatia (Hrvatska) +385'),
        (53, 'Cuba +53'),
        (357, 'Cyprus +357'),
        (420, 'Czech Republic +420'),
        (45, 'Denmark +45'),
        (253, 'Djibouti +253'),
        (1, 'Dominica +1'),
        (1, 'Dominican Republic +1'),
        (593, 'Ecuador +593'),
        (20, 'Egypt +20'),
        (503, 'El Salvador +503'),
        (240, 'Equatorial Guinea +240'),
        (291, 'Eritrea +291'),
        (372, 'Estonia +372'),
        (251, 'Ethiopia +251'),
        (298, 'Faroe Islands +298'),
        (679, 'Fiji +679'),
        (358, 'Finland +358'),
        (33, 'France +33'),
        (594, 'French Guiana +594'),
        (689, 'French Polynesia +689'),
        (241, 'Gabon +241'),
        (220, 'Gambia +220'),
        (995, 'Georgia +995'),
        (49, 'Germany +49'),
        (233, 'Ghana +233'),
        (30, 'Greece +30'),
        (299, 'Greenland +299'),
        (1, 'Grenada +1'),
        (590, 'Guadeloupe +590'),
        (1, 'Guam +1'),
        (502, 'Guatemala +502'),
        (224, 'Guinea +224'),
        (245, 'Guinea-Bissau +245'),
        (592, 'Guyana +592'),
        (509, 'Haiti +509'),
        (379, 'Holy See (Vatican City State) +379'),
        (504, 'Honduras +504'),
        (852, 'Hong Kong, SAR +852'),
        (36, 'Hungary +36'),
        (354, 'Iceland +354'),
        (91, 'India +91'),
        (62, 'Indonesia +62'),
        (98, 'Iran, Islamic Republic of +98'),
        (964, 'Iraq +964'),
        (353, 'Ireland +353'),
        (972, 'Israel +972'),
        (39, 'Italy +39'),
        (1, 'Jamaica +1'),
        (81, 'Japan +81'),
        (962, 'Jordan +962'),
        (7, 'Kazakhstan +7'),
        (254, 'Kenya +254'),
        (686, 'Kiribati +686'),
        (850, "Korea, Democratic People's Republic of (North) +850"),
        (82, 'Korea, Republic of (South) +82'),
        (965, 'Kuwait +965'),
        (996, 'Kyrgyzstan +996'),
        (856, 'Laos (Lao PDR) +856'),
        (371, 'Latvia +371'),
        (961, 'Lebanon +961'),
        (266, 'Lesotho +266'),
        (231, 'Liberia +231'),
        (218, 'Libya +218'),
        (423, 'Liechtenstein +423'),
        (370, 'Lithuania +370'),
        (352, 'Luxembourg +352'),
        (853, 'Macao (SAR China) +853'),
        (389, 'Macedonia, Republic of +389'),
        (261, 'Madagascar +261'),
        (265, 'Malawi +265'),
        (60, 'Malaysia +60'),
        (960, 'Maldives +960'),
        (223, 'Mali +223'),
        (356, 'Malta +356'),
        (692, 'Marshall Islands +692'),
        (596, 'Martinique +596'),
        (222, 'Mauritania +222'),
        (230, 'Mauritius +230'),
        (52, 'Mexico +52'),
        (691, 'Micronesia, Federated States of +691'),
        (373, 'Moldova +373'),
        (377, 'Monaco +377'),
        (976, 'Mongolia +976'),
        (382, 'Montenegro +382'),
        (1, 'Montserrat +1'),
        (212, 'Morocco and Western Sahara +212'),
        (258, 'Mozambique +258'),
        (95, 'Myanmar +95'),
        (264, 'Namibia +264'),
        (674, 'Nauru +674'),
        (977, 'Nepal +977'),
        (31, 'Netherlands +31'),
        (599, 'Netherlands Antilles +599'),
        (687, 'New Caledonia +687'),
        (64, 'New Zealand +64'),
        (505, 'Nicaragua +505'),
        (227, 'Niger +227'),
        (234, 'Nigeria +234'),
        (1, 'Northern Mariana Islands +1'),
        (47, 'Norway +47'),
        (968, 'Oman +968'),
        (92, 'Pakistan +92'),
        (680, 'Palau +680'),
        (970, 'Palestinian Territory, Occupied +970'),
        (507, 'Panama +507'),
        (675, 'Papua New Guinea +675'),
        (595, 'Paraguay +595'),
        (51, 'Peru +51'),
        (63, 'Philippines +63'),
        (870, 'Pitcairn +870'),
        (48, 'Poland +48'),
        (351, 'Portugal +351'),
        (1, 'Puerto Rico +1'),
        (974, 'Qatar +974'),
        (262, 'Réunion and Mayotte +262'),
        (40, 'Romania +40'),
        (7, 'Russian Federation +7'),
        (250, 'Rwanda +250'),
        (1, 'Saint Kitts and Nevis +1'),
        (1, 'Saint Lucia +1'),
        (1, 'Saint Vincent and the Grenadines +1'),
        (685, 'Samoa +685'),
        (378, 'San Marino +378'),
        (239, 'São Tomé and Principe +239'),
        (966, 'Saudi Arabia +966'),
        (221, 'Senegal +221'),
        (381, 'Serbia +381'),
        (248, 'Seychelles +248'),
        (232, 'Sierra Leone +232'),
        (65, 'Singapore +65'),
        (421, 'Slovakia +421'),
        (386, 'Slovenia +386'),
        (677, 'Solomon Islands +677'),
        (252, 'Somalia +252'),
        (27, 'South Africa +27'),
        (34, 'Spain +34'),
        (94, 'Sri Lanka +94'),
        (249, 'Sudan +249'),
        (597, 'Suriname +597'),
        (268, 'Swaziland +268'),
        (46, 'Sweden +46'),
        (41, 'Switzerland +41'),
        (963, 'Syrian Arab Republic (Syria) +963'),
        (886, 'Taiwan, Republic of China +886'),
        (992, 'Tajikistan +992'),
        (255, 'Tanzania, United Republic of +255'),
        (66, 'Thailand +66'),
        (670, 'Timor-Leste +670'),
        (228, 'Togo +228'),
        (676, 'Tonga +676'),
        (1, 'Trinidad and Tobago +1'),
        (216, 'Tunisia +216'),
        (90, 'Turkey +90'),
        (993, 'Turkmenistan +993'),
        (688, 'Tuvalu +688'),
        (256, 'Uganda +256'),
        (380, 'Ukraine +380'),
        (971, 'United Arab Emirates +971'),
        (44, 'United Kingdom +44'),
        (1, 'United States of America +1'),
        (598, 'Uruguay +598'),
        (998, 'Uzbekistan +998'),
        (678, 'Vanuatu +678'),
        (58, 'Venezuela (Bolivarian Republic of) +58'),
        (84, 'Viet Nam +84'),
        (1, 'Virgin Islands, British +1'),
        (1, 'Virgin Islands, US +1'),
        (967, 'Yemen +967'),
        (260, 'Zambia +260'),
        (263, 'Zimbabwe +263'),
    )
    COUNTRY_CHOICES = (
        ('AF', 'Afghanistan'),
        ('AX', 'Åland Islands'),
        ('AL', 'Albania'),
        ('DZ', 'Algeria'),
        ('AS', 'American Samoa'),
        ('AD', 'Andorra'),
        ('AO', 'Angola'),
        ('AI', 'Anguilla'),
        ('AQ', 'Antarctica'),
        ('AG', 'Antigua and Barbuda'),
        ('AR', 'Argentina'),
        ('AM', 'Armenia'),
        ('AW', 'Aruba'),
        ('AU', 'Australia'),
        ('AT', 'Austria'),
        ('AZ', 'Azerbaijan'),
        ('BS', 'Bahamas (the)'),
        ('BH', 'Bahrain'),
        ('BD', 'Bangladesh'),
        ('BB', 'Barbados'),
        ('BY', 'Belarus'),
        ('BE', 'Belgium'),
        ('BZ', 'Belize'),
        ('BJ', 'Benin'),
        ('BM', 'Bermuda'),
        ('BT', 'Bhutan'),
        ('BO', 'Bolivia (Plurinational State of)'),
        ('BQ', 'Bonaire, Sint Eustatius and Saba'),
        ('BA', 'Bosnia and Herzegovina'),
        ('BW', 'Botswana'),
        ('BV', 'Bouvet Island'),
        ('BR', 'Brazil'),
        ('IO', 'British Indian Ocean Territory (the)'),
        ('BN', 'Brunei Darussalam'),
        ('BG', 'Bulgaria'),
        ('BF', 'Burkina Faso'),
        ('BI', 'Burundi'),
        ('CV', 'Cabo Verde'),
        ('KH', 'Cambodia'),
        ('CM', 'Cameroon'),
        ('CA', 'Canada'),
        ('KY', 'Cayman Islands (the)'),
        ('CF', 'Central African Republic (the)'),
        ('TD', 'Chad'),
        ('CL', 'Chile'),
        ('CN', 'China'),
        ('CX', 'Christmas Island'),
        ('CC', 'Cocos (Keeling) Islands (the)'),
        ('CO', 'Colombia'),
        ('KM', 'Comoros (the)'),
        ('CD', 'Congo (the Democratic Republic of the)'),
        ('CG', 'Congo (the)'),
        ('CK', 'Cook Islands (the)'),
        ('CR', 'Costa Rica'),
        ('CI', "Côte d'Ivoire"),
        ('HR', 'Croatia'),
        ('CU', 'Cuba'),
        ('CW', 'Curaçao'),
        ('CY', 'Cyprus'),
        ('CZ', 'Czechia'),
        ('DK', 'Denmark'),
        ('DJ', 'Djibouti'),
        ('DM', 'Dominica'),
        ('DO', 'Dominican Republic (the)'),
        ('EC', 'Ecuador'),
        ('EG', 'Egypt'),
        ('SV', 'El Salvador'),
        ('GQ', 'Equatorial Guinea'),
        ('ER', 'Eritrea'),
        ('EE', 'Estonia'),
        ('SZ', 'Eswatini'),
        ('ET', 'Ethiopia'),
        ('FK', 'Falkland Islands (the) [Malvinas]'),
        ('FO', 'Faroe Islands (the)'),
        ('FJ', 'Fiji'),
        ('FI', 'Finland'),
        ('FR', 'France'),
        ('GF', 'French Guiana'),
        ('PF', 'French Polynesia'),
        ('TF', 'French Southern Territories (the)'),
        ('GA', 'Gabon'),
        ('GM', 'Gambia (the)'),
        ('GE', 'Georgia'),
        ('DE', 'Germany'),
        ('GH', 'Ghana'),
        ('GI', 'Gibraltar'),
        ('GR', 'Greece'),
        ('GL', 'Greenland'),
        ('GD', 'Grenada'),
        ('GP', 'Guadeloupe'),
        ('GU', 'Guam'),
        ('GT', 'Guatemala'),
        ('GG', 'Guernsey'),
        ('GN', 'Guinea'),
        ('GW', 'Guinea-Bissau'),
        ('GY', 'Guyana'),
        ('HT', 'Haiti'),
        ('HM', 'Heard Island and McDonald Islands'),
        ('VA', 'Holy See (the)'),
        ('HN', 'Honduras'),
        ('HK', 'Hong Kong'),
        ('HU', 'Hungary'),
        ('IS', 'Iceland'),
        ('IN', 'India'),
        ('ID', 'Indonesia'),
        ('IR', 'Iran (Islamic Republic of)'),
        ('IQ', 'Iraq'),
        ('IE', 'Ireland'),
        ('IM', 'Isle of Man'),
        ('IL', 'Israel'),
        ('IT', 'Italy'),
        ('JM', 'Jamaica'),
        ('JP', 'Japan'),
        ('JE', 'Jersey'),
        ('JO', 'Jordan'),
        ('KZ', 'Kazakhstan'),
        ('KE', 'Kenya'),
        ('KI', 'Kiribati'),
        ('KP', "Korea (the Democratic People's Republic of)"),
        ('KR', 'Korea (the Republic of)'),
        ('KW', 'Kuwait'),
        ('KG', 'Kyrgyzstan'),
        ('LV', 'Latvia'),
        ('LB', 'Lebanon'),
        ('LS', 'Lesotho'),
        ('LR', 'Liberia'),
        ('LY', 'Libya'),
        ('LI', 'Liechtenstein'),
        ('LT', 'Lithuania'),
        ('LU', 'Luxembourg'),
        ('MO', 'Macao'),
        ('MK', 'Republic of North Macedonia'),
        ('MG', 'Madagascar'),
        ('MW', 'Malawi'),
        ('MY', 'Malaysia'),
        ('MV', 'Maldives'),
        ('ML', 'Mali'),
        ('MT', 'Malta'),
        ('MH', 'Marshall Islands (the)'),
        ('MQ', 'Martinique'),
        ('MR', 'Mauritania'),
        ('MU', 'Mauritius'),
        ('YT', 'Mayotte'),
        ('MX', 'Mexico'),
        ('FM', 'Micronesia (Federated States of)'),
        ('MD', 'Moldova (the Republic of)'),
        ('MC', 'Monaco'),
        ('MN', 'Mongolia'),
        ('ME', 'Montenegro'),
        ('MS', 'Montserrat'),
        ('MA', 'Morocco'),
        ('MZ', 'Mozambique'),
        ('MM', 'Myanmar'),
        ('NA', 'Namibia'),
        ('NR', 'Nauru'),
        ('NP', 'Nepal'),
        ('NL', 'Netherlands (the)'),
        ('NC', 'New Caledonia'),
        ('NZ', 'New Zealand'),
        ('NI', 'Nicaragua'),
        ('NE', 'Niger (the)'),
        ('NG', 'Nigeria'),
        ('NU', 'Niue'),
        ('NF', 'Norfolk Island'),
        ('MP', 'Northern Mariana Islands (the)'),
        ('NO', 'Norway'),
        ('OM', 'Oman'),
        ('PK', 'Pakistan'),
        ('PW', 'Palau'),
        ('PS', 'Palestine, State of'),
        ('PA', 'Panama'),
        ('PG', 'Papua New Guinea'),
        ('PY', 'Paraguay'),
        ('PE', 'Peru'),
        ('PH', 'Philippines (the)'),
        ('PN', 'Pitcairn'),
        ('PL', 'Poland'),
        ('PT', 'Portugal'),
        ('PR', 'Puerto Rico'),
        ('QA', 'Qatar'),
        ('RE', 'Réunion'),
        ('RO', 'Romania'),
        ('RU', 'Russian Federation (the)'),
        ('RW', 'Rwanda'),
        ('BL', 'Saint Barthélemy'),
        ('SH', 'Saint Helena, Ascension and Tristan da Cunha'),
        ('KN', 'Saint Kitts and Nevis'),
        ('LC', 'Saint Lucia'),
        ('MF', 'Saint Martin (French part)'),
        ('PM', 'Saint Pierre and Miquelon'),
        ('VC', 'Saint Vincent and the Grenadines'),
        ('WS', 'Samoa'),
        ('SM', 'San Marino'),
        ('ST', 'Sao Tome and Principe'),
        ('SA', 'Saudi Arabia'),
        ('SN', 'Senegal'),
        ('RS', 'Serbia'),
        ('SC', 'Seychelles'),
        ('SL', 'Sierra Leone'),
        ('SG', 'Singapore'),
        ('SX', 'Sint Maarten (Dutch part)'),
        ('SK', 'Slovakia'),
        ('SI', 'Slovenia'),
        ('SB', 'Solomon Islands'),
        ('SO', 'Somalia'),
        ('ZA', 'South Africa'),
        ('GS', 'South Georgia and the South Sandwich Islands'),
        ('SS', 'South Sudan'),
        ('ES', 'Spain'),
        ('LK', 'Sri Lanka'),
        ('SD', 'Sudan (the)'),
        ('SR', 'Suriname'),
        ('SJ', 'Svalbard and Jan Mayen'),
        ('SE', 'Sweden'),
        ('CH', 'Switzerland'),
        ('SY', 'Syrian Arab Republic'),
        ('TW', 'Taiwan (Province of China)'),
        ('TJ', 'Tajikistan'),
        ('TZ', 'Tanzania, United Republic of'),
        ('TH', 'Thailand'),
        ('TL', 'Timor-Leste'),
        ('TG', 'Togo'),
        ('TK', 'Tokelau'),
        ('TO', 'Tonga'),
        ('TT', 'Trinidad and Tobago'),
        ('TN', 'Tunisia'),
        ('TR', 'Turkey'),
        ('TM', 'Turkmenistan'),
        ('TC', 'Turks and Caicos Islands (the)'),
        ('TV', 'Tuvalu'),
        ('UG', 'Uganda'),
        ('UA', 'Ukraine'),
        ('AE', 'United Arab Emirates (the)'),
        ('GB', 'United Kingdom of Great Britain and Northern Ireland (the)'),
        ('UM', 'United States Minor Outlying Islands (the)'),
        ('US', 'United States of America (the)'),
        ('UY', 'Uruguay'),
        ('UZ', 'Uzbekistan'),
        ('VU', 'Vanuatu'),
        ('VE', 'Venezuela (Bolivarian Republic of)'),
        ('VN', 'Viet Nam'),
        ('VG', 'Virgin Islands (British)'),
        ('VI', 'Virgin Islands (U.S.)'),
        ('WF', 'Wallis and Futuna'),
        ('EH', 'Western Sahara'),
        ('YE', 'Yemen'),
        ('ZM', 'Zambia'),
        ('ZW', 'Zimbabwe'),
    )

    title = models.CharField(max_length=4, choices=TITLE_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    confirm_password = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=10)
    country_calling_code = models.IntegerField(choices=CALLING_CODE_CHOICES)
    department = models.ForeignKey(Departments, on_delete=models.SET_NULL,null=True, blank=True)
    position = models.ForeignKey(Positions, on_delete=models.SET_DEFAULT, default=1)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    city = models.CharField(max_length=255)
    address = models.TextField()
    image = models.ImageField(blank=True, null=True, upload_to='images/Employee/')
    user_permission = models.ManyToManyField(User_permission,blank=True)

    def __str__(self):
        return self.username

    def serialize(self):
        url = ''
        if (self.image):
            url = self.image.url
        department = ''
        if self.department:
            department = {'pk' :self.department.pk,'name' :self.department.name,}
        user_permission = []
        for x in self.user_permission.all():
            user_permission.append({'pk': x.pk, 'name': x.name})

        return {
            'pk': self.pk,
            'title': self.title,
            'gender': self.gender,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'username': self.username,
            'email': self.email,
            'date_of_birth': self.date_of_birth,
            'country_calling_code': self.country_calling_code,
            'phone_number': self.phone_number,
            'department': department,
            'position': {'pk' :self.position.pk,'name' :self.position.name,},
            'country': self.country,
            'city': self.city,
            'address': self.address,
            'image' : url,
            'user_permission': user_permission,
        }

class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = ['title','gender','first_name','last_name','username','email','password','confirm_password','date_of_birth','country_calling_code','phone_number', 'department', 'position', 'country', 'city', 'address', 'image']
