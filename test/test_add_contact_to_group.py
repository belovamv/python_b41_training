from model.contact import Contact
from model.group import Group
import random


def test_add_contact_to_group(app, db):
    contacts_without_group = app.orm.get_contacts_without_group()
    if len(contacts_without_group) == 0:
        app.contact.create(Contact(firstname="new_contact_without_group"))
        contacts_without_group = app.orm.get_contacts_without_group()
    if len(db.get_group_list()) == 0:
        app.group.create(Group(name="group_preconditions"))
        app.contact.go_to_home_page()

    all_groups = db.get_group_list()
    contact = random.choice(contacts_without_group)
    group = random.choice(all_groups)

    app.contact.add_contact_to_group(contact.id, group.id)
    app.contact.go_to_home_page()
    app.contact.select_group_in_filter(group.id)
    all_contacts_in_group = app.contact.find_elements_in_list()
    assert sorted(all_contacts_in_group, key=Contact.id_or_max) == sorted(app.orm.get_contacts_in_group(group), key=Contact.id_or_max)
