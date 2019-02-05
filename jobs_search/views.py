from django.views import generic
from django.views.generic.edit import CreateView
from .models import Annonce
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Profile
from .forms import ProfileForm
from .forms import UserLoginForm
from django.contrib.auth.models import User

class AnnoncesListView(generic.ListView):

    template_name = "jobs_search/index.html"
    context_object_name = "all_annonces"
    paginate_by = 6

    def get_queryset(self):
        return Annonce.objects.order_by('-date')


class AnnonceDetailView (generic.DetailView):

    model = Annonce
    context_object_name = 'annonce'
    template_name = 'jobs_search/detail.html'


# @method_decorator(login_required, name='dispatch')
class CreateAnnonce(CreateView):

    template_name = "jobs_search/annonce_form.html"
    model = Annonce
    fields = ['title', 'domaine', 'region', 'description', 'image', 'phone']

    def form_valid(self, form):
        form.instance.owner = Profile.objects.get(user=self.request.user)
        return super(CreateAnnonce, self).form_valid(form)

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(CreateAnnonce, self).dispatch(*args, **kwargs)


class ProfileFormView(View):

    # user registration view

    form_class = ProfileForm
    template_name = 'jobs_search/register.html'

    def get(self, request):

        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):

        form = self.form_class(request.POST)

        if form.is_valid():
            # profile = form.save(commit=False)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            status = form.cleaned_data['status']

            u_s_r = User.objects.create(email=email, username=username)
            u_s_r.set_password(password)
            u_s_r.save()
            profile = Profile.objects.create(user=u_s_r, status=status)
            profile.save()

            # return user object if credentials are correct

            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('jobs_search:index')

        return render(request, self.template_name, {'form': form})


class UserLoginFormView(View):

    # user login view

    form_class = UserLoginForm
    template_name = 'jobs_search/login.html'

    def get(self, request):

        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):

        form = self.form_class(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:

            login(request, user)
            return redirect('jobs_search:index')

        else:

            return render(request, self.template_name, {'form': form})


def user_logout(request):

    logout(request)
    return redirect('jobs_search:index')


def user_annonces_list(request):

    user = request.user
    profile = Profile.objects.get(user=user)
    list_annonces = profile.annonce_set.all()
    context = {
        'list_annonces': list_annonces
    }
    return render(request, 'jobs_search/annonces_list.html', context)


def search(request):

    region = request.POST.get('region')
    domaine = request.POST.get('domaine')

    # annonces_region = Annonce.objects.filter(region__contains=region)
    # annonces_domaine = Annonce.objects.filter(domaine__contains=domaine)
    # annonces = annonces_region | annonces_domaine

    annonces = Annonce.objects.filter(region=region, domaine=domaine)

    return render(request, 'jobs_search/search_results.html', {'annonces': annonces})
