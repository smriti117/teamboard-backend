from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Count, Q

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .models import Company, KBEntry, QueryLog
from .permissions import IsAdminUser
from .serializers import KBEntrySerializer


class RegisterView(APIView):
    """
    Method : POST
    Endpoint : /api/auth/register/
    Public
    Creates a User -> signal auto-creates Company + api_key ->
    view updates company_name -> returns a JWT + the api_key.
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        company_name = request.data.get('company_name')
        email = request.data.get('email', '')

        if not username or not password or not company_name:
            return Response(
                {"error": "username, password, and company_name are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "A user with that username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create_user(
            username=username, password=password, email=email
        )

        company = user.company
        company.company_name = company_name
        company.save(update_fields=['company_name'])

        access = str(AccessToken.for_user(user))

        return Response(
            {
                "username": user.username,
                "company_name": company.company_name,
                "api_key": company.api_key,
                "access": access,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """
    Method : POST
    Endpoint :  /api/auth/login/
    Public. 
    Validates credentials and returns a fresh JWT + credentials.
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is None:
            return Response(
                {"error": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        access = str(AccessToken.for_user(user))
        company = user.company

        return Response(
            {
                "access": access,
                "company_name": company.company_name,
                "api_key": company.api_key,
            },
            status=status.HTTP_200_OK,
        )


class KBQueryView(APIView):
    """
    Method : POST
    Endpoint :  /api/kb/query/
    Protected (JWT required)
    Searches KBEntry and logs the query atomically.
    """

    def post(self, request):
        search_term = request.data.get('search', '')
        if not isinstance(search_term, str) or not search_term.strip():
            return Response(
                {"error": "The 'search' field is required and cannot be blank."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        search_term = search_term.strip()

        company = request.user.company

        with transaction.atomic():
            matches = KBEntry.objects.filter(
                Q(question__icontains=search_term) | Q(answer__icontains=search_term)
            )
            results = list(matches)
            count = len(results)

            QueryLog.objects.create(
                company=company,
                search_term=search_term,
                results_count=count,
            )

        serialized = KBEntrySerializer(results, many=True).data

        return Response(
            {
                "search": search_term,
                "count": count,
                "results": serialized,
            },
            status=status.HTTP_200_OK,
        )


class UsageSummaryView(APIView):
    """
    Method : GET
    Endpoint:  /api/admin/usage-summary/
    Admin-only. Platform-wide usage stats.
    """
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_queries = QueryLog.objects.aggregate(total=Count('id'))['total'] or 0

        active_companies = QueryLog.objects.values('company').distinct().count()

        top_terms_qs = (
            QueryLog.objects
            .values('search_term')
            .annotate(count=Count('id'))
            .order_by('-count')[:5]
        )
        top_search_terms = [
            {"search_term": row['search_term'], "count": row['count']}
            for row in top_terms_qs
        ]

        return Response(
            {
                "total_queries": total_queries,
                "active_companies": active_companies,
                "top_search_terms": top_search_terms,
            },
            status=status.HTTP_200_OK,
        )
