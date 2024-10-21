import random
import string
from datetime import timedelta

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.shortcuts import reverse
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext as _


from .managers import CustomUserManager


# --------------------------------- CUM ---------------------------------
class CustomUserModel(AbstractUser):
    INFO_STATUS_CHOICES = [
        ('cm', _('Content Maker')),
        ('bo', _('Business Owner')),
        ('du', _('Dual - Both')),
        ('nc', _('Not Completed')),
        ('ip', _('In Progress')),
    ]
    username = None
    phone_number = models.CharField(max_length=11, unique=True, verbose_name=_('Phone Number'))
    otp_code = models.PositiveIntegerField(blank=True, null=True)
    otp_code_datetime_created = models.DateTimeField(auto_now=True)
    info_status = models.CharField(max_length=3, choices=INFO_STATUS_CHOICES, blank=True, null=True, default='nc', verbose_name=_('User Status'))

    objects = CustomUserManager()
    backend = 'sponsorships.backends.CustomAuthBackend'
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []


# --------------------------------- CM & BO ---------------------------------
class ContentMaker(models.Model):
    # Choices
    STATUS_CHOICES = [
        ('ap', _('Approved')),
        ('rj', _('Rejected')),
        ('ip', _('In Progress')),
    ]
    PLATFORM_CHOICES = [
        ('pd', _('Podcaster')),
        ('in', _('Instagram')),
        ('yt', _('Youtube')),
        ('ap', _('Aparat')),
    ]
    FIELD_CHOICES = [
        ('art', _('Art')),
        ('b&s', _('Business & Startups')),
        ('c&t', _('Cinema & TV')),
        ('com', _('Comedy')),
        ('c&s', _('Culture & Social')),
        ('edu', _('Education')),
        ('e&s', _('Entertainment & Story')),
        ('hlf', _('Health, Life Style & Fashion')),
        ('his', _('History')),
        ('mus', _('Music')),
        ('pol', _('Politics')),
        ('rel', _('Religions')),
        ('sdv', _('Self Development')),
        ('spo', _('Sport')),
        ('t&s', _('Technology & Science')),
        ('trc', _('True Crime')),
    ]
    ACTIVITY_YEARS_CHOICES = [
        ('lt1', _('Less Than 1 Years')),
        ('1yrs', _('1 Year')),
        ('2yrs', _('2 Years')),
        ('3yrs', _('3 Years')),
        ('4yrs', _('4 Years')),
        ('5yrs', _('5 Years')),
        ('510', _('5 - 10 Years')),
        ('m10', _('More Than 10 Years')),
    ]
    SPONSOR_EXPERIENCE_CHOICES = [
        ('hve', _("Have")),
        ('dnt', _("Don't Have")),
    ]
    READY_CHOICES = [
        ('is', _("Is")),
        ('nt', _("Isn't")),
    ]
    # Fields
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='content_maker')
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Title'))
    creator = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Creator'))
    national_code = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('National Code'))
    description = models.CharField(max_length=500, verbose_name=_('Description'))
    cover = models.ImageField(upload_to='CM/covers/', verbose_name=_('CM Profile Cover'))
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True, allow_unicode=True)
    datetime_created = models.DateField(auto_now_add=True, verbose_name=_('Datetime of Creation'))
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, blank=True, null=True, default='ip', verbose_name=_('CM Status'))
    platform = models.CharField(max_length=3, choices=PLATFORM_CHOICES, blank=True, null=True, verbose_name=_('CM Platform'))
    field = models.CharField(max_length=3, choices=FIELD_CHOICES, blank=True, null=True, verbose_name=_('CM Field'))
    link1 = models.URLField(max_length=200, verbose_name=_('Link1'))
    link2 = models.URLField(max_length=200, blank=True, null=True, verbose_name=_('Link2'))
    link3 = models.URLField(max_length=200, blank=True, null=True, verbose_name=_('Link3'))
    link4 = models.URLField(max_length=200, blank=True, null=True, verbose_name=_('Link4'))
    id1 = models.CharField(max_length=200, verbose_name=_('ID1'))
    id2 = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('ID2'))
    id3 = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('ID3'))
    id4 = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('ID4'))
    email = models.CharField(max_length=300, blank=True, null=True, verbose_name=_('Email'))
    min_price = models.PositiveIntegerField(verbose_name=_('Min Price'))
    activity_years = models.CharField(max_length=4, choices=ACTIVITY_YEARS_CHOICES, blank=True, null=True, verbose_name=_('Activity Years'))
    played = models.PositiveBigIntegerField(blank=True, null=True, verbose_name=_('Played (Viewed)'))
    subscribers = models.PositiveBigIntegerField(blank=True, null=True, verbose_name=_('Subscribers (Followers)'))
    sponsee_experience = models.CharField(max_length=3, choices=SPONSOR_EXPERIENCE_CHOICES, blank=True, null=True,
                                          verbose_name=_('Sponsee Experience'))
    ready = models.CharField(max_length=3, choices=READY_CHOICES, blank=True, null=True, verbose_name=_('Ready to Receive Requests'))
    general_proposal = models.FileField(upload_to='CM/general_proposals/', blank=True, null=True, validators=[FileExtensionValidator(['pdf'])],
                                        verbose_name=_('General Proposal'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super(ContentMaker, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} / {self.platform} / {self.field}'

    class Meta:
        ordering = ('-datetime_created',)

    def get_absolute_url(self):
        return reverse('content_maker_detail', args=[self.slug])


class BusinessOwner(models.Model):
    # Choices
    STATUS_CHOICES = [
        ('ap', _('Approved')),
        ('rj', _('Rejected')),
        ('ip', _('In Progress')),
    ]
    FIELD_CHOICES = [
        ('app', _('Agriculture, Plants, and Pets')),
        ('abs', _('Architecture and Building Services')),
        ('cam', _('Consulting and Management')),
        ('cnp', _('Content Production')),
        ('des', _('Design')),
        ('dts', _('Digital and Technology Services')),
        ('edu', _('Education')),
        ('ens', _('Engineering Services')),
        ('fac', _('Fashion and Clothing')),
        ('caf', _('Commercial and Financial')),
        ('fic', _('Food Industry and Cooking')),
        ('haa', _('Handicrafts and Arts')),
        ('hmb', _('Health, Medicine, and Beauty')),
        ('hbb', _('Home-based Business')),
        ('iat', _('Investment and Trading')),
        ('mai', _('Manufacturing and Industrial')),
        ('maa', _('Marketing and Advertising')),
        ('npc', _('Non-Profit and Charity')),
        ('obs', _('Online Business and Store')),
        ('tai', _('Tourism and Immigration')),
    ]
    ACTIVITY_YEARS_CHOICES = [
        ('lt1', _('Less Than 1 Years')),
        ('1yrs', _('1 Year')),
        ('2yrs', _('2 Years')),
        ('3yrs', _('3 Years')),
        ('4yrs', _('4 Years')),
        ('5yrs', _('5 Years')),
        ('510', _('5 - 10 Years')),
        ('m10', _('More Than 10 Years')),
    ]
    SPONSOR_EXPERIENCE_CHOICES = [
        ('hve', _("Have")),
        ('dnt', _("Don't Have")),
    ]
    # Fields
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='business_owner')
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Title'))
    description = models.CharField(max_length=500, verbose_name=_('Description'))
    cover = models.ImageField(upload_to='BO/covers/', verbose_name=_('BO Profile Cover'))
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True, allow_unicode=True)
    datetime_created = models.DateField(auto_now_add=True, verbose_name=_('Datetime of Creation'))
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, blank=True, null=True, default='ip', verbose_name=_('BO Status'))
    field = models.CharField(max_length=3, choices=FIELD_CHOICES, blank=True, null=True, verbose_name=_('BO Field'))
    link1 = models.URLField(max_length=200, verbose_name=_('Link1'))
    link2 = models.URLField(max_length=200, blank=True, null=True, verbose_name=_('Link2'))
    email = models.CharField(max_length=300, blank=True, null=True, verbose_name=_('Email'))
    year = models.CharField(max_length=4, choices=ACTIVITY_YEARS_CHOICES, blank=True, null=True, verbose_name=_('Foundation Year'))
    sponsor_experience = models.CharField(max_length=3, choices=SPONSOR_EXPERIENCE_CHOICES, blank=True, null=True,
                                          verbose_name=_('Sponsor Experience'))
    general_proposal = models.FileField(upload_to='BO/general_proposals/', blank=True, null=True, validators=[FileExtensionValidator(['pdf'])],
                                        verbose_name=_('General Proposal'))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super(BusinessOwner, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.title} / {self.field}'

    class Meta:
        ordering = ('-datetime_created',)

    def get_absolute_url(self):
        return reverse('business_owner_detail', args=[self.slug])


# --------------------------------- Process ---------------------------------
def generate_unique_id():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))


def generate_unique_code():
    return ''.join(random.choices(string.digits + string.digits, k=8))


class Sponsorship(models.Model):
    # Choices
    STATUS_CHOICES = [
        ('wa', _('Waiting')),  # => waiting for admin to approve
        ('rj', _('Rejected')),  # => rejected by admin
        ('ip', _('Open')),  # => ready to receive requests
        ('as', _('Assigned')),  # => partner assigned and the sponsorship is in progress
        ('pa', _('Paid')),  # => closed
    ]
    CM_FIELD_CHOICES = [
        ('nom', _('No Matter')),
        ('art', _('Art')),
        ('b&s', _('Business & Startups')),
        ('c&t', _('Cinema & TV')),
        ('com', _('Comedy')),
        ('c&s', _('Culture & Social')),
        ('edu', _('Education')),
        ('e&s', _('Entertainment & Story')),
        ('hlf', _('Health, Life Style & Fashion')),
        ('his', _('History')),
        ('mus', _('Music')),
        ('pol', _('Politics')),
        ('rel', _('Religions')),
        ('sdv', _('Self Development')),
        ('spo', _('Sport')),
        ('t&s', _('Technology & Science')),
        ('trc', _('True Crime')),
    ]
    BO_FIELD_CHOICES = [
        ('nom', _('No Matter')),
        ('app', _('Agriculture, Plants, and Pets')),
        ('abs', _('Architecture and Building Services')),
        ('cam', _('Consulting and Management')),
        ('cnp', _('Content Production')),
        ('des', _('Design')),
        ('dts', _('Digital and Technology Services')),
        ('edu', _('Education')),
        ('ens', _('Engineering Services')),
        ('fac', _('Fashion and Clothing')),
        ('caf', _('Commercial and Financial')),
        ('fic', _('Food Industry and Cooking')),
        ('haa', _('Handicrafts and Arts')),
        ('hmb', _('Health, Medicine, and Beauty')),
        ('hbb', _('Home-based Business')),
        ('iat', _('Investment and Trading')),
        ('mai', _('Manufacturing and Industrial')),
        ('maa', _('Marketing and Advertising')),
        ('npc', _('Non-Profit and Charity')),
        ('obs', _('Online Business and Store')),
        ('tai', _('Tourism and Immigration')),
    ]
    TYPE_CHOICES = [
        ('nsr', _('Need Sponsor')),
        ('nse', _('Need Sponsee')),
    ]
    SIGN_CHOICES = [
        ('dne', _('Done')),
        ('ndn', _('Not Done')),
    ]
    # Generals
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    description = models.CharField(max_length=500, verbose_name=_('Description'))
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True, allow_unicode=True)
    unique_url_id = models.CharField(max_length=20, null=True, unique=True, blank=True)
    code = models.CharField(max_length=8, null=True, unique=True, blank=True)
    datetime_created = models.DateField(auto_now_add=True, verbose_name=_('Datetime of Creation'))
    deadline = models.DateField(verbose_name=_('Deadline'))
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default='wa', verbose_name=_('Sponsorship Status'))
    # Mains
    type = models.CharField(max_length=3, choices=TYPE_CHOICES, verbose_name=_('Sponsorship Type'))
    sponsor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='sponsorships_sponsor')
    sponsee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='sponsorships_sponsee')
    min_price = models.PositiveIntegerField(verbose_name=_('Min Price'))
    max_price = models.PositiveIntegerField(verbose_name=_('Max Price'))
    specialized_cm_proposal = models.FileField(upload_to='sponsorships/specialized_cm_proposals/', blank=True, null=True, verbose_name=_('Specialized CM Proposal'))
    specialized_bo_proposal = models.FileField(upload_to='sponsorships/specialized_bo_proposals/', blank=True, null=True, verbose_name=_('Specialized BO Proposal'))
    sponsor_sign = models.CharField(max_length=3, choices=SIGN_CHOICES, default='ndn', verbose_name=_('Sponsor Sign'))
    sponsee_sign = models.CharField(max_length=3, choices=SIGN_CHOICES, default='ndn', verbose_name=_('Sponsee Sign'))
    # Favorites
    favorite_cm_field1 = models.CharField(max_length=3, choices=CM_FIELD_CHOICES, default='nom', verbose_name=_('Favorite CM Field 1'))
    favorite_cm_field2 = models.CharField(max_length=3, choices=CM_FIELD_CHOICES, blank=True, null=True, verbose_name=_('Favorite CM Field 2'))
    favorite_cm_field3 = models.CharField(max_length=3, choices=CM_FIELD_CHOICES, blank=True, null=True, verbose_name=_('Favorite CM Field 3'))
    favorite_bo_field1 = models.CharField(max_length=3, choices=BO_FIELD_CHOICES, default='nom', verbose_name=_('Favorite BO Field 1'))
    favorite_bo_field2 = models.CharField(max_length=3, choices=BO_FIELD_CHOICES, blank=True, null=True, verbose_name=_('Favorite BO Field 2'))
    favorite_bo_field3 = models.CharField(max_length=3, choices=BO_FIELD_CHOICES, blank=True, null=True, verbose_name=_('Favorite BO Field 3'))
    # Invitations
    sponsor_invitation1 = models.ForeignKey(BusinessOwner, on_delete=models.CASCADE, blank=True, null=True, related_name='invited_sponsor1')
    sponsor_invitation2 = models.ForeignKey(BusinessOwner, on_delete=models.CASCADE, blank=True, null=True, related_name='invited_sponsor2')
    sponsor_invitation3 = models.ForeignKey(BusinessOwner, on_delete=models.CASCADE, blank=True, null=True, related_name='invited_sponsor3')
    sponsee_invitation1 = models.ForeignKey(ContentMaker, on_delete=models.CASCADE, blank=True, null=True, related_name='invited_sponsee1')
    sponsee_invitation2 = models.ForeignKey(ContentMaker, on_delete=models.CASCADE, blank=True, null=True, related_name='invited_sponsee2')
    sponsee_invitation3 = models.ForeignKey(ContentMaker, on_delete=models.CASCADE, blank=True, null=True, related_name='invited_sponsee3')

    def save(self, *args, **kwargs):
        # if self.pk is not None:
        #     old_status = SaleFile.objects.get(pk=self.pk).status
        #     if old_status == 'pen' and self.status == 'acc':
        #         self.datetime_expired = timezone.now() + timezone.timedelta(days=60)
        # else:
        #     if self.status == 'acc':
        #         self.datetime_expired = timezone.now() + timezone.timedelta(days=60)
        if not self.unique_url_id:
            self.unique_url_id = generate_unique_id()
        if not self.code:
            self.code = generate_unique_code()
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super(Sponsorship, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.type} / {self.title} / {self.code}'

    class Meta:
        ordering = ('-datetime_created',)

    def get_absolute_url(self):
        return reverse('sponsorship_detail', args=[self.slug, self.unique_url_id])


class Offer(models.Model):
    # Choices
    STATUS_CHOICES = [
        ('su', _('Submitted')),
        ('rj', _('Rejected')),
        ('ac', _('Accepted')),
    ]
    # Generals
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    description = models.CharField(max_length=500, verbose_name=_('Description'))
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True, allow_unicode=True)
    code = models.CharField(max_length=8, null=True, unique=True, blank=True)
    datetime_created = models.DateField(auto_now_add=True, verbose_name=_('Datetime of Creation'))
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, blank=True, null=True, default='su', verbose_name=_('Offer Status'))
    # Mains
    sponsorship = models.ForeignKey(Sponsorship, on_delete=models.CASCADE, related_name='offers', verbose_name=_('Sponsorship'))
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requesters', verbose_name=_('Requester'))
    roughly_price = models.PositiveIntegerField(verbose_name=_('Roughly Offering Price'))
    proposal = models.FileField(upload_to='offers/proposals/', blank=True, null=True, verbose_name=_('Offering Proposal'))

    def save(self, *args, **kwargs):
        # if self.pk is not None:
        #     old_status = SaleFile.objects.get(pk=self.pk).status
        #     if old_status == 'pen' and self.status == 'acc':
        #         self.datetime_expired = timezone.now() + timezone.timedelta(days=60)
        # else:
        #     if self.status == 'acc':
        #         self.datetime_expired = timezone.now() + timezone.timedelta(days=60)
        if not self.code:
            self.code = generate_unique_code()
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        super(Offer, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.code} / {self.requester} / {self.title}'

    class Meta:
        ordering = ('-datetime_created',)

    def get_absolute_url(self):
        return reverse('offer_detail', args=[self.slug, self.code])



