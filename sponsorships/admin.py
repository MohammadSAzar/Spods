from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from . import models
from .forms import AdminPanelUserChangeForm, AdminPanelUserCreateForm

# ---------------------------------------- CM & BO ----------------------------------------
@admin.register(models.ContentMaker)
class ContentMakerAdmin(admin.ModelAdmin):
    model = models.ContentMaker
    list_display = ('title', 'creator', 'platform', 'ready', 'min_price', 'max_price', 'played', 'subscribers', 'status',
                    'datetime_created',)


class ContentMakerInline(admin.StackedInline):
    model = models.ContentMaker
    can_delete = False
    verbose_name_plural = 'CM'
    fields = ('title', 'creator', 'platform', 'ready', 'min_price', 'max_price', 'played', 'subscribers', 'status',
              'datetime_created',)


@admin.register(models.BusinessOwner)
class BusinessOwnerAdmin(admin.ModelAdmin):
    model = models.BusinessOwner
    list_display = ('title', 'field', 'status', 'datetime_created',)


class BusinessOwnerInline(admin.StackedInline):
    model = models.BusinessOwner
    can_delete = False
    verbose_name_plural = 'BO'
    fields = ('title', 'field', 'status', 'datetime_created',)


# ---------------------------------------- CUM ----------------------------------------
class CustomUserAdmin(BaseUserAdmin):
    form = AdminPanelUserChangeForm
    add_form = AdminPanelUserCreateForm
    inlines = (BusinessOwnerInline, BusinessOwnerInline)

    list_display = ('phone_number', 'info_status', 'type', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('phone_number', 'password', 'info_status', 'type')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'password1', 'password2'),
        }),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    filter_horizontal = ()


admin.site.register(models.CustomUserModel, CustomUserAdmin)


# ---------------------------------------- Process ----------------------------------------
@admin.register(models.Sponsorship)
class SponsorshipAdmin(admin.ModelAdmin):
    model = models.Sponsorship
    list_display = ('title', 'code', 'type', 'sponsor', 'sponsee', 'sponsor_sign', 'sponsee_sign', 'status',
                    'min_price', 'max_price', 'datetime_created', 'deadline',)


@admin.register(models.Offer)
class OfferAdmin(admin.ModelAdmin):
    model = models.Offer
    list_display = ('title', 'code', 'sponsorship', 'requester', 'status', 'roughly_price', 'proposal', 'datetime_created',)

