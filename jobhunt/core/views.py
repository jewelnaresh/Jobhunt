from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import authenticate, login, logout

from .models import JobData
from .scraper import Data, Website, Crawler


def postjob(request):
    return render(request, 'core/postjob.html')

class JobListView(ListView):
    model = JobData
    paginate_by = 20
    template_name = 'core/index.html'


def scraper_view(request):
    return render(request, 'core/scraper.html')


def scraper(request):
    crawler = Crawler()

    siteData = [
        ['Xpress', 'https://xpress.jobs/jobs', 'h3.job_listing-title', 'div.job_listing-company a strong',
            'a.job_listing-clickbox[href*="/View/"]', '(/View/).*', 'a.next', 'https://xpress.jobs/Jobs/Sector/it'],
        ['Topjobs', 'http://topjobs.lk/', 'td h2 a', 'td h1', 'td h2 a',
            '(employer).*(.jsp)', 'no-value-available', 'http://topjobs.lk/applicant/vacancybyfunctionalarea.jsp?FA=SDQ&jst=OPEN']
    ]

    sites = []
    for row in siteData:
        sites.append(Website(row[0], row[1], row[2],
                             row[3], row[4], row[5], row[6], row[7]))

    info = []
    for site in sites:
        info = crawler.find(site)
        for data in info:
            qs = JobData.objects.filter(
                company_name=data.company, job_title=data.job, link=data.jobUrl)
            print(qs)
            if qs:
                continue
            JobData.objects.create(
                company_name=data.company, job_title=data.job, link=data.jobUrl)

    context = {
        'info': info
    }

    return render(request, "core/done.html", context)


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        passwordconfirm = request.POST['passwordconfirm']

        try:
            user = User.objects.get(username=username)
            return render(request, 'core/register', {'error': 'User already exsists'})
        except User.DoesNotExist:
            if password != passwordconfirm:
                return render(request, 'core/register', {'error': 'Passwords do not match'})
            user = User.objects.create_user(
                username=username, email=email, password=password)
            auth.login(request, user)
            return redirect('index')
    else:
        return render(request, 'core/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            return render(request, "core/login.html", {"message": "Invalid credentials."})
    else:
        return render(request, 'core/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')
