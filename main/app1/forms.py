from django import forms
from .models import CommonModel, UserModel

class PythonCodeFormField(forms.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = PythonCodeWidget
        super().__init__(*args, **kwargs)

class PythonCodeWidget(forms.Textarea):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('attrs', {}).update({
            'class': 'python-code-widget',
            'rows': 20,
            'cols': 80,
        })
        super().__init__(*args, **kwargs)

class StrategyForm(forms.ModelForm):
    ticker = forms.CharField()
    start_date = forms.DateField()
    end_date = forms.DateField()
    normal_stop_loss = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    normal_take_profit = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    trailing_stop_loss = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    dynamic_exit_condition = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    atr_stop_loss = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    atr_take_profit = forms.DecimalField(max_digits=10, decimal_places=2, required=False)

    strategy = forms.ChoiceField(choices=[])

    class Meta:
        model = CommonModel
        fields = ['ticker', 'start_date', 'end_date', 'normal_stop_loss', 'normal_take_profit', 'trailing_stop_loss', 'dynamic_exit_condition', 'atr_stop_loss', 'atr_take_profit', 'strategy']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get the user from kwargs
        super(StrategyForm, self).__init__(*args, **kwargs)

        # Get common model choices
        common_choices = [(f"{obj.name}", f"{obj.name}") for obj in CommonModel.objects.all()]
        
        # Get user choices based on the owner
        user_choices = [(f"{obj.name}", f"{obj.name}") for obj in UserModel.objects.filter(owner=user)]
        print(common_choices)
        print("Hello")
        print(user_choices)
        # Combine both lists
        combined_choices = common_choices + user_choices
        print(combined_choices)
        # Set the combined choices in the strategy field
        self.fields['strategy'].choices = combined_choices

class csvForm(forms.ModelForm):
    csv_file = forms.FileField()
    normal_stop_loss = forms.DecimalField(max_digits=10, decimal_places=2,required=False)
    normal_take_profit = forms.DecimalField(max_digits=10, decimal_places=2,required=False)
    trailing_stop_loss = forms.DecimalField(max_digits=10, decimal_places=2,required=False)
    dynamic_exit_condition = forms.DecimalField(max_digits=10, decimal_places=2,required=False)
    atr_stop_loss = forms.DecimalField(max_digits=10, decimal_places=2,required=False)
    atr_take_profit = forms.DecimalField(max_digits=10, decimal_places=2,required=False)
    strategy = forms.ModelChoiceField(queryset=CommonModel.objects.all())
    class Meta:
        model = CommonModel
        fields = ['csv_file', 'normal_stop_loss','normal_take_profit','trailing_stop_loss','dynamic_exit_condition','atr_stop_loss','atr_take_profit','strategy']

class userstrategy(forms.ModelForm):
    strategy = forms.CharField()
    source = PythonCodeFormField(required=False)

    class Meta:
        model = UserModel
        fields = ['strategy', 'source']


