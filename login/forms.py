from django import forms
import pytz
from .models import Time_zone, Meeting, Members

class UserRegistrationForm(forms.Form):
	username = forms.CharField(
			required = True,
			label = 'Username',
			max_length = 32
		)
	email = forms.CharField(
			required = True,
			label = 'Email',
			max_length = 32,
		)
	password = forms.CharField(
			required = True,
			label = 'Password',
			max_length = 32,
			widget = forms.PasswordInput()
		)

class TimezoneForm(forms.ModelForm):
	tz = pytz.all_timezones
	# timezone = forms.ModelChoiceField(queryset=tz)
	# timezone = forms.CharField(max_length=128, help_text="Please enter the category name.")
	# timezone = forms.ChoiceField(choices=tz, required=True)

	class Meta:
		model = Time_zone
		fields = ('timezone',) 

class MeetingForm(forms.ModelForm):
	st_date = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], help_text="%Y-%m-%d %H:%M:%S")
	end_date = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M:%S'], help_text="%Y-%m-%d %H:%M:%S")
	class Meta:
		model = Meeting
		fields = ('title', 'st_date', 'end_date',)
		# widgets = {'username': forms.HiddenInput()}

class MembersForm(forms.ModelForm):

	YESNO_CHOICES = ((0, 'No'), (1, 'Yes'), (2, 'May Be'))
	# status = forms.TypedChoiceField(choices=YESNO_CHOICES, widget=forms.RadioSelect, coerce=int)
	# email = forms.CharField(max_length=128)
	# hash_meet = forms.CharField()

	class Meta:
		model = Members
		fields = ('email', 'timezone')
		widgets = {'hash_meet': forms.HiddenInput(),
					'status': forms.HiddenInput()}
