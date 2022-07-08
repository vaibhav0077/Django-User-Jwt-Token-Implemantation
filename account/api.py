from rest_framework import generics, permissions, mixins
from rest_framework.generics import UpdateAPIView
from rest_framework import status
from rest_framework.response import Response
from .serializer import RegisterSerializer, UserSerializer, ChangePasswordSerializer, UpdateUserSerializer
from django.contrib.auth.models import User


# Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        print("Serializer registered: ", serializer)
        serializer.is_valid(raise_exception=True)
        # print(serializer.errors)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })


class UpdateProfileView(generics.UpdateAPIView):

    queryset = User.objects.all()
    # permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer


class ChangePasswordView(UpdateAPIView):

    serializer_class = ChangePasswordSerializer
    model = User
    # permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            if serializer.data.get("new_password") != serializer.data.get("confirm_password"):
                return Response({"msg": "old password not equal to confirm password."}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': ['NOthing To Show']
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ForgetPasswordAPi(generics.GenericAPIView):
