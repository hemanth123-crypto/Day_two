from services.customer_services import CustomerService
from services.membership_services import MembershipService
from services.account_services import AccountService


class StoreSystem:

    def register_customer(self):
        CustomerService.add_customer()

    def view_customers(self):
        CustomerService.view_customers()

    def update_customer(self):
        CustomerService.update_customer()

    def delete_customer(self):
        CustomerService.delete_customer()

    def add_membership(self):
        MembershipService.add_membership()

    def view_memberships(self):
        MembershipService.view_memberships()

    def update_membership(self):
        MembershipService.update_membership()

    def delete_membership(self):
        MembershipService.delete_membership()

    def apply_discount(self):
        MembershipService.apply_discount()

    def create_membership_account(self):
        AccountService.create_membership()

    def renew_membership(self):
        AccountService.renew_membership()

    def expire_membership(self):
        AccountService.expire_membership()

    def delete_membership_account(self):
        AccountService.delete_membership()

    def view_accounts(self):
        AccountService.view_accounts()