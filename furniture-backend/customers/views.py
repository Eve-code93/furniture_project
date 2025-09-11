from rest_framework import generics, permissions
from .models import Customer
from .serializers import CustomerSerializer

# Only used if you want admins to list all customers
class CustomerListView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAdminUser]


# Customer can view or edit their own profile
class CustomerProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Get or create customer profile for logged-in user
        customer, _ = Customer.objects.get_or_create(user=self.request.user)
        return customer
