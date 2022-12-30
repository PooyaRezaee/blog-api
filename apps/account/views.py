from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from core.permissions import IsOwnerOrIsAdmin
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveUpdateAPIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from .serializers import ListUserSerializer,RegisterUserSerializer,AdminUsersSerializer,UpdateUserSerializer
from .models import User

__all__ = [
    'UserListApiView',
    'UserDetailAPiView',
    'UserCreateView',
    'FullUserListApiView',
    'ChangeToken',
    'DeleteUserApiView',
    'UserApiView'
]

class UserListApiView(ListAPIView):
    """
    Show Summery Users
    
    Access => Any
    """
    permission_classes = [AllowAny]
    serializer_class = ListUserSerializer
    queryset = User.objects.all()

class UserApiView(APIView):
    """
    Show Detail UserSelf

    Access => Authenticated
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()

    def get(self, request):
        user = self.queryset.get(pk=request.user.id)
        srz_data = self.serializer_class(instance=user).data
        return Response(srz_data,status=status.HTTP_200_OK)

class FullUserListApiView(ListAPIView):
    """
    Show Full Information Users
    
    Access => Admin
    """
    permission_classes = [IsAdminUser]
    serializer_class = AdminUsersSerializer
    queryset = User.objects.all()

class UserDetailAPiView(RetrieveUpdateAPIView):
    """
    Show Detail,Update & Delelte User
    
    Access => Admin : Full; User : name,email,phone_number;
    """
    permission_classes = [IsOwnerOrIsAdmin]
    queryset = User.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.request.user.is_admin:
            serializer_class = AdminUsersSerializer
        else:
            serializer_class = UpdateUserSerializer
            
        kwargs.setdefault('context', self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class UserCreateView(APIView):
    """
    Create New User
    
    Access => Any
    - have throttle
    """

    permission_classes = [AllowAny]
    throttle_scope = 'register'
    serializer_class = RegisterUserSerializer

    def post(self,request):
        srz = self.serializer_class(data=request.data)
        if srz.is_valid():
            srz.create_user(srz.validated_data)
            return Response(srz.data,status=status.HTTP_201_CREATED)
        return Response(srz.errors,status=status.HTTP_400_BAD_REQUEST)


class ChangeToken(ListAPIView):
    """
    Refresh Token If Exists

    Access => Any
    - have throttle
    """
    
    permission_classes = [AllowAny]
    throttle_scope = 'ref_token'

    def post(self,request):
        user = request.user
        data = request.data
        username = request.data.get('username')
        password = request.data.get('password')
        
        response_error = {}
        error = False

        if username is None:
            response_error['username'] = ['This Field Required']
            error = True

        if password is None:
            response_error['password'] = ['This Field Required']
            error = True

        if error:
            return Response(response_error)
        
        srz = AuthTokenSerializer(data=request.data)
        srz.is_valid(raise_exception=True)
        user = User.objects.get(email=username)
        token = Token.objects.filter(user=user)
        if token.exists():
            token.first().delete()
            new_token = Token.objects.create(user=user)
            return Response({'token':new_token.key})  
        
        return Response({'msg':'token not created'})
    
class DeleteUserApiView(DestroyAPIView):
    """
    Delete User

    Access => Admin Or HerSelf
    """
    permission_classes = [IsOwnerOrIsAdmin]

    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()