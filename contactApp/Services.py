from typing import Optional

from django.contrib.auth.models import User

from .exception import UserExistException, InvalidLoginDetails, AppLockedException
from .models import Profile, Contacts
import re


def validate_email(email):
    user_emails = User.objects.all()
    for user in user_emails:
        if user.email == email:
            return True
    return False


def validate_add_contact_name(name, user):
    list_of_contacts = Contacts.objects.all()
    for contact in list_of_contacts:
        if contact.name == name and contact.user_id == user:
            return True
    return False


# def validate_password(password):
#     if re.match(password)


def register_user(user, address, phone_number):
    user = Profile(user=user, address=address, phone_number=phone_number)
    user.save()
    return user.pk


def login_user(email, password):
    if not validate_email(email):
        raise InvalidLoginDetails()
    user: Profile = Profile.objects.get(email=email)
    if user.password != password:
        raise InvalidLoginDetails()
    user.is_enable = True
    user.save()


def add_contact(email, name, phone_number, address, contact_email):
    user = User.objects.get(email=email)
    contacts = find_all_contact(email)
    for user_contact in contacts:
        if user_contact.name == name:
            UserExistException("name already exist")
    addcontact = Contacts(name=name, phone_number=phone_number, address=address, email=contact_email, user_id=user)
    addcontact.save()


def find_all_contact(email):
    user_contacts = []
    if not validate_email(email):
        raise UserExistException()
    user = User.objects.get(email=email)
    all_contacts = Contacts.objects.all()
    for contacts in all_contacts:
        if contacts.user_id.pk == user.pk:
            user_contacts.append(contacts)
    return user_contacts


def find_a_contacts(email, name):
    list_of_contacts = find_all_contact(email)
    for contacts in list_of_contacts:
        if contacts.name == name:
            return contacts
    return f"contact doesn't exist"


def delete_a_contact(email, name):
    contacts = find_a_contacts(email, name)
    contacts.delete()


def delete_all_contacts(email):
    list_of_all_contact = find_all_contact(email)
    for contacts in list_of_all_contact:
        contacts.delete()


def edit_contacts(user_email, name, new_name: Optional[str] = None, phone_number: Optional[str] = None,
                  address: Optional[str] = None, email: Optional[str] = None):
    contact = find_a_contacts(user_email, name)
    if new_name is not None:
        contact.name = new_name
        contact.save()
    if phone_number is not None:
        contact.phone_number = phone_number
        contact.save()
    if address is not None:
        contact.address = address
        contact.save()
    if email is not None:
        contact.email = email
        contact.save()


def block_contact(email, name):
    contact = find_a_contacts(email, name)
    contact.is_blocked = True
    contact.save()


def unblock_contact(email, name):
    contact = find_a_contacts(email, name)
    contact.is_blocked = False
    contact.save()
