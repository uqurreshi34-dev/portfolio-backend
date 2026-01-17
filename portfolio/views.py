from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from .models import Project, Skill, Contact
from .serializers import ProjectSerializer, SkillSerializer, ContactSerializer

# Create your views here.
# Class based views


class ProjectListView(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetailView(RetrieveAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class SkillListView(ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer


class ContactCreateView(CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
