from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from users.models import CustomUser

# @admin.register(CustomUser)
# class CustomUserAdmin(BaseAdmin):
#     pass

# # ユーザーのパスワードが平文で保存されないようにするためのフォーム
# class CustomUserChangeForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = '__all__'  # すべてのフィールドを表示

#     def clean_password(self):
#         # 既存のパスワードフィールドをハッシュ化して保存しない
#         return self.initial["password"]

@admin.register(CustomUser)
class CustomUserAdmin(DefaultUserAdmin):
    """
    (管理画面設定) ユーザー
    """

    # カスタムユーザーモデルに合わせて list_display を設定
    list_display = ('email', 'account_status', 'company', 'is_staff', 'is_superuser', 'created_at')
    list_filter = ('account_status', 'company', 'is_staff', 'is_superuser')
    search_fields = ('email',)
    ordering = ('email',)

    # フィールドセットをカスタマイズ（管理画面のフィールド表示を変更）
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('company',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'groups')}),
        ('Account Status', {'fields': ('account_status',)}),
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),
    )

    # 管理画面でユーザーを作成する際のフィールド
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'company',
                'is_staff',
                'is_superuser',
                'groups'
            ),
        }),
    )

    readonly_fields = ('created_at', 'updated_at')
