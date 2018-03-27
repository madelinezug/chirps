from django.contrib import admin

# Register your models here.
from .models import Individual
from .models import Organization
from .models import Affiliation
from .models import Announcement
from .models import Tags
from .models import AnnounceTags
from .models import SubmitAnnouncement
from .models import SubmitTag
from .models import UserSearch
from .models import TagSearch
from .models import Save


admin.site.register(Individual)
