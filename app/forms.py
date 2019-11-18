from .models import *
from django import forms


class PartnerForm(forms.ModelForm):

    class Meta:
        model = Partner
        fields = [
            'name',
            'identification_type',
            'data',
            'balance',
            'contractor'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'identification_type': forms.Select(attrs={'class': 'form-control'}),
            'data': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
            'contractor': forms.Select(attrs={'class': 'form-control'})
        }


class ContractorForm(forms.ModelForm):

    class Meta:
        model = Contractor
        fields = [
            'name',
            'UNP',
            'address',
            'balance',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'UNP': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = [
            'station_id',
            'owner',
            'info',
            'course'
        ]
        widgets = {
            'station_id': forms.NumberInput(attrs={'class': 'form-control'}),
            'owner': forms.TextInput(attrs={'class': 'form-control'}),
            'info': forms.Textarea(attrs={'class': 'form-control'}),
            'course': forms.NumberInput(attrs={'class': 'form-control'})

        }


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = [
            'name',
            'data',
            'partner'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'data': forms.TextInput(attrs={'class': 'form-control'}),
            'partner': forms.Select(attrs={'class': 'form-control'})
        }


class PartnerCoinForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = [
            'balance'
        ]
        widgets = {
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class StartWashingForm(forms.Form):
    station = forms.ModelChoiceField(
        label="Станция", queryset=Station.objects.all(), empty_label=None)
    post = forms.ModelChoiceField(label="Пост", queryset=Post.objects.all())
    partner = forms.ModelChoiceField(
        label="Клиент", queryset=Partner.objects.all(), required=False)
    card = forms.ModelChoiceField(
        label="Карта", queryset=Card.objects.all(), required=False)
    payment = forms.DecimalField(label="Сумма")

    station.widget.attrs.update({'class': 'form-control'})
    post.widget.attrs.update({'class': 'form-control'})
    payment.widget.attrs.update({'class': 'form-control'})
    card.widget.attrs.update({'class': 'form-control'})
    partner.widget.attrs.update({'class': 'form-control'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['post'].queryset = Post.objects.none()
        # self.fields['card'].queryset = Card.objects.none()


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'contractor',
            'amount',
            'annotation'
        ]
        widgets = {
            'contractor': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'annotation': forms.Textarea(attrs={'class': 'form-control'})
        }


# class TestMessageForm(forms.Form):
#     data = forms.CharField(max_length=100)
