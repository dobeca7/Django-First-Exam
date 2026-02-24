from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from academies.forms import AcademyDeleteForm, AcademyForm
from academies.models import Academy


class AcademyCreateView(SuccessMessageMixin, CreateView):
    model = Academy
    form_class = AcademyForm
    template_name = "academies/academy-form.html"
    success_message = "Academy created successfully."

    def get_success_url(self):
        return reverse("academy-detail-slug", kwargs={"slug": self.object.slug})


class AcademyEditView(UpdateView):
    model = Academy
    form_class = AcademyForm
    template_name = "academies/academy-form.html"

    def get_success_url(self):
        return reverse("academy-detail-slug", kwargs={"slug": self.object.slug})

class AcademyListView(ListView):
    model = Academy
    queryset = Academy.objects.order_by("name")
    template_name = "academies/academy-list.html"
    context_object_name = "academies"
    paginate_by = 7

class AcademyDetailView(DetailView):
    model = Academy
    template_name = "academies/academy-detail.html"
    context_object_name = "academy"

    def get_object(self, queryset=None):
        slug = self.kwargs.get("slug")
        if slug:
            return get_object_or_404(Academy, slug=slug)
        return super().get_object(queryset=queryset)


class AcademyDeleteView(DeleteView):
    model = Academy
    template_name = "academies/academy-confirm-delete.html"
    success_url = reverse_lazy("academy-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AcademyDeleteForm(instance=self.object)
        return context
