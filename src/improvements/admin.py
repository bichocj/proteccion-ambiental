from django.contrib import admin

from improvements.models import Agreement, AgreementDetail, MettingAppliedTo, Metting

admin.site.register(Agreement)
admin.site.register(AgreementDetail)
admin.site.register(MettingAppliedTo)
admin.site.register(Metting)
