from django import forms

from .models import Course, Feedback, CourseMaterial

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('title', 'description',)

    ## Course title validation
    def clean_title(self):
        title = self.cleaned_data['title']

        if len(title.strip()) < 3:
            raise forms.ValidationError("Course's title must be at least 3 characters long.")

        return title

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('rating', 'comment',)

        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),

            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write your feedback...'}),
        }

    def clean_rating(self):
        rating = self.cleaned_data['rating']

        if rating < 1 or rating > 5:
            raise forms.ValidationError('Rating must be between 1 and 5.')

        return rating

class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ('title', 'file',)

    def clean_title(self):
        title = self.cleaned_data['title']

        if len(title.strip()) < 2:
            raise forms.ValidationError('The material title must be at least 2 characters long.')

        return title

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']

        allowed_exts = [
            '.pdf',
            '.png',
            '.jpg',
            '.jpeg',
            '.gif',
            '.doc',
            '.docx',
            '.ppt',
            '.pptx',
            '.xls',
            '.xlsx',
            '.txt',
        ]

        file_name = uploaded_file.name.lower()

        if not any(
            file_name.endswith(ext)
            for ext in allowed_exts
        ):
            raise forms.ValidationError('The file type is not allowed.')

        return uploaded_file