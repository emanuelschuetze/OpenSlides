from django.apps import apps

from .models import State, Workflow


def create_builtin_workflows(sender, **kwargs):
    """
    Receiver function to create a simple and a complex workflow. It is
    connected to the signal django.db.models.signals.post_migrate during
    app loading.
    """
    if Workflow.objects.exists():
        # If there is at least one workflow, then do nothing.
        return

    # DGB workflow
    workflow_1 = Workflow.objects.create(name='DGB')
    state_1_1 = State.objects.create(name='eingereicht',
                                     workflow=workflow_1,
                                     allow_submitter_edit=True,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     required_permission_to_see='motions.can_manage',
                                     dont_set_identifier=True)
    state_1_2 = State.objects.create(name='geprüft',
                                     workflow=workflow_1,
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     required_permission_to_see='motions.can_manage',
                                     dont_set_identifier=True)
    state_1_3 = State.objects.create(name='zugeordnet',
                                     workflow=workflow_1,
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     dont_set_identifier=False)
    state_1_4 = State.objects.create(name='Empfehlung der ABK liegt vor',
                                     workflow=workflow_1,
                                     allow_submitter_edit=False,
                                     allow_support=True,
                                     allow_create_poll=True,
                                     dont_set_identifier=False)
    state_1_10 = State.objects.create(name='angenommen',
                                     workflow=workflow_1,
                                     recommendation_label='Annahme',
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     css_class='success',
                                     merge_amendment_into_final=1)
    state_1_11 = State.objects.create(name='angenommen in geänderter Fassung',
                                     workflow=workflow_1,
                                     recommendation_label='Annahme in geänderter Fassung',
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     css_class='success',
                                     merge_amendment_into_final=1)
    state_1_12 = State.objects.create(name='angenommen als Material zu Antrag',
                                     workflow=workflow_1,
                                     recommendation_label='Annahme als Material zu Antrag',
                                     show_recommendation_extension_field=True,
                                     show_state_extension_field=True,
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     css_class='success',
                                     merge_amendment_into_final=1)
    state_1_13 = State.objects.create(name='angenommen als Material an',
                                     workflow=workflow_1,
                                     recommendation_label='Annahme als Material an',
                                     show_recommendation_extension_field=True,
                                     show_state_extension_field=True,
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     css_class='success',
                                     merge_amendment_into_final=1)
    state_1_14 = State.objects.create(name='angenommen in geänderter Fassung als Material',
                                     workflow=workflow_1,
                                     recommendation_label='Annahme in geänderter Fassung als Material',
                                     show_recommendation_extension_field=True,
                                     show_state_extension_field=True,
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     css_class='success',
                                     merge_amendment_into_final=1)
    state_1_15 = State.objects.create(name='erledigt bei Annahme von Antrag',
                                     workflow=workflow_1,
                                     recommendation_label='Erledigt bei Annahme von Antrag',
                                     show_recommendation_extension_field=True,
                                     show_state_extension_field=True,
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     css_class='default')
    state_1_16 = State.objects.create(name='abgelehnt',
                                     workflow=workflow_1,
                                     recommendation_label='Ablehnung',
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     css_class='danger')
    state_1_17 = State.objects.create(name='nicht befasst',
                                     workflow=workflow_1,
                                     recommendation_label='Nichtbefassung',
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     css_class='default')
    state_1_20 = State.objects.create(name='zurückgezogen',
                                     workflow=workflow_1,
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     dont_set_identifier=True,
                                     css_class='default')
    state_1_21 = State.objects.create(name='Sonstiges',
                                     workflow=workflow_1,
                                     recommendation_label='Sonstiges',
                                     show_recommendation_extension_field=True,
                                     show_state_extension_field=True,
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     css_class='default')
    state_1_1.next_states.add(state_1_2, state_1_20)
    state_1_2.next_states.add(state_1_3, state_1_20)
    state_1_3.next_states.add(state_1_4, state_1_20)
    state_1_4.next_states.add(state_1_10, state_1_11, state_1_12, state_1_13, state_1_14, state_1_15, state_1_16, state_1_17, state_1_20, state_1_21)
    workflow_1.first_state = state_1_1
    workflow_1.save(skip_autoupdate=True)


    # IG Metall workflow (ABK)
    workflow_2 = Workflow.objects.create(name='IG Metall')
    state_2_1 = State.objects.create(name='in Bearbeitung',
                                     workflow=workflow_2,
                                     allow_submitter_edit=True,
                                     required_permission_to_see='motions.can_manage',
                                     dont_set_identifier=True)
    state_2_2 = State.objects.create(name='gestellt',
                                     workflow=workflow_2,
                                     required_permission_to_see='motions.can_manage',
                                     dont_set_identifier=True)
    state_2_3 = State.objects.create(name='geprüft',
                                     workflow=workflow_2,
                                     required_permission_to_see='motions.can_manage',
                                     dont_set_identifier=True)
    state_2_4 = State.objects.create(name='Fachbereich zugeteilt',
                                     workflow=workflow_2,
                                     required_permission_to_see='motions.can_manage')
    state_2_5 = State.objects.create(name='empfohlen durch Fachabteilung',
                                     workflow=workflow_2,
                                     required_permission_to_see='motions.can_manage')
    state_2_6 = State.objects.create(name='beraten durch gfVM',
                                     workflow=workflow_2,
                                     required_permission_to_see='motions.can_manage')
    state_2_7 = State.objects.create(name='beraten durch Vorstand',
                                     workflow=workflow_2,
                                     required_permission_to_see='motions.can_manage')
    state_2_8 = State.objects.create(name='beraten durch ABK',
                                     workflow=workflow_2,
                                     required_permission_to_see='motions.can_manage')
    state_2_9 = State.objects.create(name='initiale Freigabe',
                                     workflow=workflow_2,
                                     allow_create_poll=True)
    state_2_10 = State.objects.create(name='in Bearbeitung auf GT',
                                     workflow=workflow_2)
    state_2_11 = State.objects.create(name='erneute Freigabe',
                                     workflow=workflow_2,
                                     allow_create_poll=True)
    state_2_20 = State.objects.create(name='angenommen',
                                     workflow=workflow_2,
                                     recommendation_label='Annahme',
                                     css_class='success',
                                     merge_amendment_into_final=1)
    state_2_21 = State.objects.create(name='angenommen in geänderter Fassung',
                                     workflow=workflow_2,
                                     recommendation_label='Annahme in geänderter Fassung',
                                     css_class='success',
                                     merge_amendment_into_final=1)
    # TODO: merge_amend_into_final=True?
    state_2_22 = State.objects.create(name='angenommen als Material zu Antrag',
                                     workflow=workflow_2,
                                     recommendation_label='Annahme als Material zu Antrag',
                                     show_recommendation_extension_field=True,
                                     show_state_extension_field=True,
                                     css_class='success',
                                     merge_amendment_into_final=1)
    # TODO: merge_amend_into_final=True?
    state_2_23 = State.objects.create(name='angenommen als Material an',
                                     workflow=workflow_2,
                                     recommendation_label='Annahme als Material an',
                                     show_recommendation_extension_field=True,
                                     show_state_extension_field=True,
                                     css_class='success',
                                     merge_amendment_into_final=1)
    # TODO: merge_amend_into_final=True?
    state_2_24 = State.objects.create(name='angenommen in geänderter Fassung als Material',
                                     workflow=workflow_2,
                                     recommendation_label='Annahme in geänderter Fassung als Material',
                                     show_recommendation_extension_field=True,
                                     show_state_extension_field=True,
                                     css_class='success',
                                     merge_amendment_into_final=1)
    state_2_25 = State.objects.create(name='erledigt bei Annahme von Antrag',
                                     workflow=workflow_2,
                                     recommendation_label='Erledigt bei Annahme von Antrag',
                                     show_recommendation_extension_field=True,
                                     show_state_extension_field=True,
                                     css_class='default')
    state_2_26 = State.objects.create(name='abgelehnt',
                                     workflow=workflow_2,
                                     recommendation_label='Ablehnung',
                                     css_class='danger')
    state_2_27 = State.objects.create(name='nicht befasst',
                                     workflow=workflow_2,
                                     recommendation_label='Nichtbefassung',
                                     css_class='default')
    state_2_28 = State.objects.create(name='zurückgezogen',
                                     workflow=workflow_2,
                                     dont_set_identifier=True,
                                     css_class='default')
    state_2_29 = State.objects.create(name='Sonstiges',
                                     workflow=workflow_2,
                                     recommendation_label='Sonstiges',
                                     show_recommendation_extension_field=True,
                                     show_state_extension_field=True,
                                     css_class='default')
    state_2_1.next_states.add(state_2_2)
    state_2_2.next_states.add(state_2_3, state_2_28)
    state_2_3.next_states.add(state_2_4, state_2_28)
    state_2_4.next_states.add(state_2_5, state_2_28)
    state_2_5.next_states.add(state_2_6, state_2_28)
    state_2_6.next_states.add(state_2_7, state_2_28)
    state_2_7.next_states.add(state_2_8, state_2_28)
    state_2_8.next_states.add(state_2_9, state_2_28)
    state_2_9.next_states.add(state_2_10, state_2_20, state_2_21, state_2_22, state_2_23, state_2_24, state_2_25, state_2_26,state_2_27, state_2_28, state_2_29)
    state_2_10.next_states.add(state_2_11, state_2_28)
    state_2_11.next_states.add(state_2_10, state_2_20, state_2_21, state_2_22, state_2_23, state_2_24, state_2_25, state_2_26,state_2_27, state_2_28, state_2_29)
    workflow_2.first_state = state_2_1
    workflow_2.save(skip_autoupdate=True)


def get_permission_change_data(sender, permissions, **kwargs):
    """
    Yields all necessary collections if 'motions.can_see' permission changes.
    """
    motions_app = apps.get_app_config(app_label="motions")
    for permission in permissions:
        # There could be only one 'motions.can_see' and then we want to return data.
        if (
            permission.content_type.app_label == motions_app.label
            and permission.codename == "can_see"
        ):
            yield from motions_app.get_startup_elements()
