from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import DonationPlace
from django.contrib import messages
from .forms import DonationPlaceForm
from django_countries.fields import Country
from django.http import HttpResponse


@staff_member_required
def review_place(request, id=None):
    if id is None:
        submissions = DonationPlace.objects.filter(published=False)
        return render(request, 'admin/review_place_index.html', {'submissions': submissions})
    else:
        place = get_object_or_404(DonationPlace, pk=id)
        if request.method == 'POST':
            if request.POST['approve'] == 'true':
                place.published = True
                place.save()
                # redirect to donation place page
                redirect('/admin')
        else:
            num_contributions = DonationPlace.objects.filter(contributor=place.contributor).count()
            return render(request, 'admin/review_place.html', {'place': place, 'num_contributions': num_contributions})


@staff_member_required
def import_donation_places(request):
    if request.method == 'POST':
        try:
            csv_file = request.FILES["csv_file"]
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File is not CSV type')
                return redirect('/admin/import_donation_places')

            # if file is too large, return
            if csv_file.multiple_chunks():
                messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
                return redirect('/admin/import_donation_places')

            file_data = csv_file.read().decode("utf-8")
            count = 0
            lines = file_data.split("\n")
            del lines[-1]
            for line in lines:
                fields = line.split(",")
                p = DonationPlace.objects.create(name=fields[0], street=fields[1], house=int(fields[2]), address_supplement=fields[3], postal_code=int(fields[4]), city=fields[5], country=Country.country_from_ioc(ioc_code=fields[6]), published=True)
                p.save()
        except Exception as e:
            messages.error(request, "Unable to upload file. " + repr(e))
            return redirect('/admin/import_donation_places')

        messages.success(request, str(count) + " place(s) added")
        return redirect('/admin')

    else:
        return render(request, 'admin/upload_donations_places.html')
