from django import forms

class RoutineForm(forms.Form):
    name = forms.CharField(max_length=100)

class ScheduleForm(forms.Form):
    start_time = forms.TimeField()
    end_time = forms.TimeField()
    subject = forms.CharField(max_length=30)
    teacher_short_name = forms.CharField(max_length=30)

    def clean(self):
        cleaned_data = super().clean()

        if self.errors:
            return cleaned_data

        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time >= end_time:
            self.add_error("start_time", "Start time must be before end time")

        return cleaned_data