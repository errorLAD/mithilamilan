from django import forms
from .models import Area, Landmark, FoodPlace, Market, Event, LandmarkReview, FoodPlaceReview, MarketReview, EventReview

INPUT_CLASSES = 'w-full bg-slate-50 border border-slate-200 focus:border-[#E85D2A] focus:bg-white rounded-xl px-4 py-2.5 text-xs sm:text-sm font-medium transition-all outline-none shadow-2xs'
FILE_CLASSES = 'w-full text-xs text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-extrabold file:bg-amber-50 file:text-[#E85D2A] hover:file:bg-amber-100 cursor-pointer bg-slate-50 border border-slate-200 rounded-xl p-2'

class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['name', 'description', 'location', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': INPUT_CLASSES, 'placeholder': 'स्थान या क्षेत्र के बारे में विस्तृत जानकारी दर्ज करें...'}),
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'क्षेत्र का नाम (e.g. Madhubani, Darbhanga, Laxmi Nagar)'}),
            'location': forms.TextInput(attrs={'class': INPUT_CLASSES, 'placeholder': 'स्थान या शहर (e.g. Bihar / Delhi NCR)'}),
            'image': forms.FileInput(attrs={'class': FILE_CLASSES}),
        }

class LandmarkForm(forms.ModelForm):
    class Meta:
        model = Landmark
        fields = ['name', 'description', 'category', 'area', 'image', 'address', 'timings', 'entry_fee', 'rating']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': INPUT_CLASSES}),
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': INPUT_CLASSES}),
            'timings': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'entry_fee': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'image': forms.FileInput(attrs={'class': FILE_CLASSES}),
            'category': forms.Select(attrs={'class': INPUT_CLASSES}),
            'area': forms.Select(attrs={'class': INPUT_CLASSES}),
            'rating': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'min': '0', 'max': '5', 'step': '0.1'}),
        }

class FoodPlaceForm(forms.ModelForm):
    class Meta:
        model = FoodPlace
        fields = ['name', 'description', 'cuisine', 'area', 'image', 'address', 'timings', 'price_range', 'rating']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': INPUT_CLASSES}),
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': INPUT_CLASSES}),
            'timings': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'price_range': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'image': forms.FileInput(attrs={'class': FILE_CLASSES}),
            'cuisine': forms.Select(attrs={'class': INPUT_CLASSES}),
            'area': forms.Select(attrs={'class': INPUT_CLASSES}),
            'rating': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'min': '0', 'max': '5', 'step': '0.1'}),
        }

class MarketForm(forms.ModelForm):
    class Meta:
        model = Market
        fields = ['name', 'description', 'area', 'image', 'address', 'timings', 'specialties']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': INPUT_CLASSES}),
            'name': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'address': forms.Textarea(attrs={'rows': 2, 'class': INPUT_CLASSES}),
            'timings': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'specialties': forms.Textarea(attrs={'rows': 2, 'class': INPUT_CLASSES}),
            'image': forms.FileInput(attrs={'class': FILE_CLASSES}),
            'area': forms.Select(attrs={'class': INPUT_CLASSES}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'venue', 'area', 'image', 'start_date', 'end_date', 'ticket_price', 'ticket_link']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': INPUT_CLASSES}),
            'title': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'venue': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'ticket_price': forms.TextInput(attrs={'class': INPUT_CLASSES}),
            'ticket_link': forms.URLInput(attrs={'class': INPUT_CLASSES}),
            'image': forms.FileInput(attrs={'class': FILE_CLASSES}),
            'category': forms.Select(attrs={'class': INPUT_CLASSES}),
            'area': forms.Select(attrs={'class': INPUT_CLASSES}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': INPUT_CLASSES}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': INPUT_CLASSES}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        fields = ['content', 'rating']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'class': INPUT_CLASSES}),
            'rating': forms.Select(attrs={'class': INPUT_CLASSES}),
        }

class LandmarkReviewForm(ReviewForm):
    class Meta(ReviewForm.Meta):
        model = LandmarkReview

class FoodPlaceReviewForm(ReviewForm):
    class Meta(ReviewForm.Meta):
        model = FoodPlaceReview

class MarketReviewForm(ReviewForm):
    class Meta(ReviewForm.Meta):
        model = MarketReview

class EventReviewForm(forms.ModelForm):
    class Meta:
        model = EventReview
        fields = ['rating', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'class': INPUT_CLASSES}),
            'rating': forms.NumberInput(attrs={'class': INPUT_CLASSES, 'min': '0', 'max': '5', 'step': '0.1'}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASSES,
            'placeholder': 'Search areas, landmarks, food places...'
        })
    )