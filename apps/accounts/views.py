from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from core.permissions import IsOwnerOrIsAdmin
from rest_framework.generics import ListAPIView,DestroyAPIView,RetrieveUpdateAPIView
from .serializers import ListUserSerializer,RegisterUserSerializer,AdminUsersSerializer,UpdateUserSerializer,ChangePasswordUserSerializer
from .models import User

__all__ = [
    'UserListApiView',
    'UserDetailAPiView',
    'UserCreateView',
    'FullUserListApiView',
    'DeleteUserApiView',
    'UserApiView',
    'ChangePasswordApiView'
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
    
class DeleteUserApiView(DestroyAPIView):
    """
    Delete User

    Access => Admin Or HerSelf
    """
    permission_classes = [IsOwnerOrIsAdmin]

    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()

class ChangePasswordApiView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordUserSerializer

    def post(self,request):
        user = request.user
        srz = self.serializer_class(data=request.data)
        if srz.is_valid():
            srz.change_password(validated_data=srz.validated_data,user=user)
            return Response({'msg':'Password Changed'},status=status.HTTP_200_OK)
        return Response(srz.errors,status=status.HTTP_400_BAD_REQUEST)



