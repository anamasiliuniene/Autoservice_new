from .models import OrderReview
from django.contrib.auth.models import User
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms.models import inlineformset_factory
from .models import Order, OrderLine


class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = OrderReview
        fields = ['content']


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'photo']


class CustomUserCreateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class InstanceCreateUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['car', 'manager', 'status', 'due_back']
        widgets = {
            'due_back': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'}
            )
        }

    # optional: parse datetime-local correctly
    due_back = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        input_formats=['%Y-%m-%dT%H:%M']
    )


class OrderLineForm(forms.ModelForm):
    class Meta:
        model = OrderLine
        fields = ['service', 'quantity']


OrderLineFormSet = inlineformset_factory(
    Order,
    OrderLine,
    form=OrderLineForm,
    extra=0,
    can_delete=True
)