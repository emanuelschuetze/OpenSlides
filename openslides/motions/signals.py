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
    workflow_1 = Workflow(name='DGB')
    workflow_1.save(skip_autoupdate=True)
    state_1_1 = State(name='eingereicht',
                                     workflow=workflow_1,
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     restriction=[
                                        "is_submitter",
                                        "managers_only"
                                     ],
                                     dont_set_identifier=True,
                                     merge_amendment_into_final=-1)
    state_1_1.save(skip_autoupdate=True)
    state_1_2 = State(name='geprüft',
                                     workflow=workflow_1,
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     restriction=[
                                        "is_submitter",
                                        "managers_only"
                                     ],
                                     dont_set_identifier=True,
                                     merge_amendment_into_final=-1)
    state_1_2.save(skip_autoupdate=True)
    state_1_3 = State(name='zugeordnet',
                                     workflow=workflow_1,
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     dont_set_identifier=False,
                                     merge_amendment_into_final=-1)
    state_1_3.save(skip_autoupdate=True)
    state_1_4 = State(name='Empfehlung der ABK liegt vor',
                                     workflow=workflow_1,
                                     allow_submitter_edit=False,
                                     allow_support=True,
                                     allow_create_poll=True,
                                     dont_set_identifier=False,
                                     merge_amendment_into_final=-1)
    state_1_4.save(skip_autoupdate=True)
    state_1_10 = State(name='angenommen',
                                     workflow=workflow_1,
                                     recommendation_label='Annahme',
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     css_class='green',
                                     merge_amendment_into_final=1)
    state_1_10.save(skip_autoupdate=True)
    state_1_11 = State(name='angenommen in geänderter Fassung',
                                     workflow=workflow_1,
                                     recommendation_label='Annahme in geänderter Fassung',
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     css_class='green',
                                     merge_amendment_into_final=1)
    state_1_11.save(skip_autoupdate=True)
    state_1_12 = State(name='angenommen als Material zu Antrag',
                                     workflow=workflow_1,
                                     recommendation_label='Annahme als Material zu Antrag',
                                     show_recommendation_extension_field=True,
                                     show_state_extension_field=True,
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     css_class='green',
                                     merge_amendment_into_final=1)
    state_1_12.save(skip_autoupdate=True)
    state_1_13 = State(name='angenommen als Material an',
                                     workflow=workflow_1,
                                     recommendation_label='Annahme als Material an',
                                     show_recommendation_extension_field=True,
                                     show_state_extension_field=True,
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     css_class='green',
                                     merge_amendment_into_final=1)
    state_1_13.save(skip_autoupdate=True)
    state_1_14 = State(name='angenommen in geänderter Fassung als Material',
                                     workflow=workflow_1,
                                     recommendation_label='Annahme in geänderter Fassung als Material',
                                     show_recommendation_extension_field=True,
                                     show_state_extension_field=True,
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     css_class='green',
                                     merge_amendment_into_final=1)
    state_1_14.save(skip_autoupdate=True)
    state_1_15 = State(name='erledigt bei Annahme von Antrag',
                                     workflow=workflow_1,
                                     recommendation_label='Erledigt bei Annahme von Antrag',
                                     show_recommendation_extension_field=True,
                                     show_state_extension_field=True,
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     css_class='grey',
                                     merge_amendment_into_final=-1)
    state_1_15.save(skip_autoupdate=True)
    state_1_16 = State(name='abgelehnt',
                                     workflow=workflow_1,
                                     recommendation_label='Ablehnung',
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     css_class='red',
                                     merge_amendment_into_final=-1)
    state_1_16.save(skip_autoupdate=True)
    state_1_17 = State(name='nicht befasst',
                                     workflow=workflow_1,
                                     recommendation_label='Nichtbefassung',
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     css_class='grey',
                                     merge_amendment_into_final=-1)
    state_1_17.save(skip_autoupdate=True)
    state_1_20 = State(name='zurückgezogen',
                                     workflow=workflow_1,
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     dont_set_identifier=True,
                                     css_class='grey',
                                     merge_amendment_into_final=-1)
    state_1_20.save(skip_autoupdate=True)
    state_1_21 = State(name='Sonstiges',
                                     workflow=workflow_1,
                                     recommendation_label='Sonstiges',
                                     show_recommendation_extension_field=True,
                                     show_state_extension_field=True,
                                     allow_submitter_edit=False,
                                     allow_support=False,
                                     allow_create_poll=False,
                                     css_class='grey',
                                     merge_amendment_into_final=-1)
    state_1_21.save(skip_autoupdate=True)
    state_1_1.next_states.add(state_1_2, state_1_20)
    state_1_2.next_states.add(state_1_3, state_1_20)
    state_1_3.next_states.add(state_1_4, state_1_20)
    state_1_4.next_states.add(state_1_10, state_1_11, state_1_12, state_1_13, state_1_14, state_1_15, state_1_16, state_1_17, state_1_20, state_1_21)
    workflow_1.first_state = state_1_1
    workflow_1.save(skip_autoupdate=True)


    # IG Metall workflow (ABK)
    workflow_2 = Workflow(name='IG Metall (ABK)')
    workflow_2.save(skip_autoupdate=True)
    state_2_1 = State(name='in Bearbeitung',
                        workflow=workflow_2,
                        restriction=[
                            "is_submitter",
                            "managers_only"
                        ],
                        allow_submitter_edit=True,
                        dont_set_identifier=True,
                        merge_amendment_into_final=-1)
    state_2_1.save(skip_autoupdate=True)
    state_2_2 = State(name='gestellt',
                        workflow=workflow_2,
                        restriction=[
                            "is_submitter",
                            "managers_only"
                        ],
                        dont_set_identifier=True,
                        merge_amendment_into_final=-1)
    state_2_2.save(skip_autoupdate=True)
    state_2_3 = State(name='verworfen',
                        workflow=workflow_2,
                        restriction=[
                            "is_submitter",
                            "managers_only"
                        ],
                        dont_set_identifier=True,
                        css_class='grey',
                        merge_amendment_into_final=-1)
    state_2_3.save(skip_autoupdate=True)
    state_2_4 = State(name='geprüft',
                        workflow=workflow_2,
                        restriction=[
                            "motions.can_see_internal",
                            "motions.can_manage_metadata",
                            "managers_only"
                        ],
                        dont_set_identifier=True,
                        merge_amendment_into_final=-1)
    state_2_4.save(skip_autoupdate=True)
    state_2_5 = State(name='an Federführenden zugeteilt',
                        workflow=workflow_2,
                        restriction=[
                            "motions.can_see_internal",
                            "motions.can_manage_metadata",
                            "managers_only"
                        ],
                        merge_amendment_into_final=-1)
    state_2_5.save(skip_autoupdate=True)
    state_2_6 = State(name='empfohlen durch Federführenden',
                        workflow=workflow_2,
                        restriction=[
                            "motions.can_see_internal",
                            "motions.can_manage_metadata",
                            "managers_only"
                        ],
                        merge_amendment_into_final=-1)
    state_2_6.save(skip_autoupdate=True)
    state_2_7 = State(name='beraten durch gfVm',
                        workflow=workflow_2,
                        restriction=[
                            "motions.can_see_internal",
                            "motions.can_manage_metadata",
                            "managers_only"
                        ],
                        merge_amendment_into_final=-1)
    state_2_7.save(skip_autoupdate=True)
    state_2_8 = State(name='beraten durch Vorstand',
                        workflow=workflow_2,
                        restriction=[
                            "motions.can_see_internal",
                            "motions.can_manage_metadata",
                            "managers_only"
                        ],
                        merge_amendment_into_final=-1)
    state_2_8.save(skip_autoupdate=True)
    state_2_9 = State(name='beraten durch ABK',
                        workflow=workflow_2,
                        restriction=[
                            "motions.can_see_internal",
                            "motions.can_manage_metadata",
                            "managers_only"
                        ],
                        merge_amendment_into_final=-1)
    state_2_9.save(skip_autoupdate=True)
    state_2_10 = State(name='Freigabe',
                        workflow=workflow_2,
                        allow_create_poll=True,
                        merge_amendment_into_final=-1)
    state_2_10.save(skip_autoupdate=True)
    state_2_20 = State(name='angenommen',
                        workflow=workflow_2,
                        recommendation_label='Annahme',
                        css_class='green',
                        merge_amendment_into_final=1)
    state_2_20.save(skip_autoupdate=True)
    state_2_21 = State(name='angenommen in geänderter Fassung',
                        workflow=workflow_2,
                        recommendation_label='Annahme in geänderter Fassung',
                        css_class='green',
                        merge_amendment_into_final=1)
    state_2_21.save(skip_autoupdate=True)
    state_2_22 = State(name='angenommen als Material zu',
                        workflow=workflow_2,
                        recommendation_label='Annahme als Material zu',
                        show_recommendation_extension_field=True,
                        show_state_extension_field=True,
                        css_class='green',
                        merge_amendment_into_final=1)
    state_2_22.save(skip_autoupdate=True)
    state_2_23 = State(name='angenommen als Material an Vorstand',
                        workflow=workflow_2,
                        recommendation_label='Annahme als Material an den Vorstand',
                        css_class='green',
                        merge_amendment_into_final=1)
    state_2_23.save(skip_autoupdate=True)
    state_2_24 = State(name='erledigt durch',
                        workflow=workflow_2,
                        recommendation_label='Erledigt durch',
                        show_recommendation_extension_field=True,
                        show_state_extension_field=True,
                        css_class='grey',
                        merge_amendment_into_final=-1)
    state_2_24.save(skip_autoupdate=True)
    state_2_25 = State(name='erledigt durch Praxis',
                        workflow=workflow_2,
                        recommendation_label='Erledigt durch Praxis',
                        css_class='grey',
                        merge_amendment_into_final=-1)
    state_2_25.save(skip_autoupdate=True)
    state_2_26 = State(name='abgelehnt',
                        workflow=workflow_2,
                        recommendation_label='Ablehnung',
                        css_class='red',
                        merge_amendment_into_final=-1)
    state_2_26.save(skip_autoupdate=True)
    state_2_27 = State(name='nicht befasst',
                        workflow=workflow_2,
                        recommendation_label='Nichtbefassung',
                        css_class='grey',
                        merge_amendment_into_final=-1)
    state_2_27.save(skip_autoupdate=True)
    state_2_28 = State(name='zurückgezogen',
                        workflow=workflow_2,
                        dont_set_identifier=True,
                        css_class='grey',
                        merge_amendment_into_final=-1)
    state_2_28.save(skip_autoupdate=True)
    state_2_29 = State(name='Sonstiges',
                        workflow=workflow_2,
                        recommendation_label='Sonstiges',
                        show_recommendation_extension_field=True,
                        show_state_extension_field=True,
                        css_class='grey',
                        merge_amendment_into_final=-1)
    state_2_29.save(skip_autoupdate=True)
    state_2_1.next_states.add(state_2_2, state_2_3)
    state_2_2.next_states.add(state_2_4, state_2_28)
    state_2_4.next_states.add(state_2_5, state_2_28)
    state_2_5.next_states.add(state_2_6, state_2_28)
    state_2_6.next_states.add(state_2_7, state_2_28)
    state_2_7.next_states.add(state_2_8, state_2_28)
    state_2_8.next_states.add(state_2_9, state_2_28)
    state_2_9.next_states.add(state_2_10, state_2_28)
    state_2_10.next_states.add(state_2_20, state_2_21, state_2_22, state_2_23, state_2_24, state_2_25, state_2_26,state_2_27, state_2_28, state_2_29)
    workflow_2.first_state = state_2_1
    workflow_2.save(skip_autoupdate=True)

    # IG Metall workflow (SBK)
    workflow_3 = Workflow(name='IG Metall (SBK)')
    workflow_3.save(skip_autoupdate=True)
    state_3_1 = State(name='in Bearbeitung',
                        workflow=workflow_3,
                        restriction=[
                            "is_submitter",
                            "managers_only"
                        ],
                        allow_submitter_edit=True,
                        dont_set_identifier=True,
                        merge_amendment_into_final=-1)
    state_3_1.save(skip_autoupdate=True)
    state_3_2 = State(name='gestellt',
                        workflow=workflow_3,
                        restriction=[
                            "is_submitter",
                            "managers_only"
                        ],
                        dont_set_identifier=True,
                        merge_amendment_into_final=-1)
    state_3_2.save(skip_autoupdate=True)
    state_3_3 = State(name='verworfen',
                      workflow=workflow_3,
                        restriction=[
                            "is_submitter",
                            "managers_only"
                        ],
                        dont_set_identifier=True,
                        css_class='grey',
                        merge_amendment_into_final=-1)
    state_3_3.save(skip_autoupdate=True)
    state_3_4 = State(name='geprüft',
                        workflow=workflow_3,
                        restriction=[
                            "motions.can_see_internal",
                            "motions.can_manage_metadata",
                            "managers_only"
                        ],
                        dont_set_identifier=True,
                        merge_amendment_into_final=-1)
    state_3_4.save(skip_autoupdate=True)
    state_3_5 = State(name='an Federführenden zugeteilt',
                        workflow=workflow_3,
                        restriction=[
                            "motions.can_see_internal",
                            "motions.can_manage_metadata",
                            "managers_only"
                        ],
                        merge_amendment_into_final=-1)
    state_3_5.save(skip_autoupdate=True)
    state_3_6 = State(name='empfohlen durch Federführenden',
                        workflow=workflow_3,
                        restriction=[
                            "motions.can_see_internal",
                            "motions.can_manage_metadata",
                            "managers_only"
                        ],
                        merge_amendment_into_final=-1)
    state_3_6.save(skip_autoupdate=True)
    state_3_7 = State(name='beraten durch gfVm',
                        workflow=workflow_3,
                        restriction=[
                            "motions.can_see_internal",
                            "motions.can_manage_metadata",
                            "managers_only"
                        ],
                        merge_amendment_into_final=-1)
    state_3_7.save(skip_autoupdate=True)
    state_3_8 = State(name='beraten durch Vorstand',
                        workflow=workflow_3,
                        restriction=[
                            "motions.can_see_internal",
                            "motions.can_manage_metadata",
                            "managers_only"
                        ],
                        merge_amendment_into_final=-1)
    state_3_8.save(skip_autoupdate=True)
    state_3_9 = State(name='beraten durch SBK',
                        workflow=workflow_3,
                        restriction=[
                            "motions.can_see_internal",
                            "motions.can_manage_metadata",
                            "managers_only"
                        ],
                        merge_amendment_into_final=-1)
    state_3_9.save(skip_autoupdate=True)
    state_3_10 = State(name='Freigabe',
                        workflow=workflow_3,
                        allow_create_poll=True,
                        merge_amendment_into_final=-1)
    state_3_10.save(skip_autoupdate=True)
    state_3_20 = State(name='angenommen',
                        workflow=workflow_3,
                        recommendation_label='Annahme',
                        css_class='green',
                        merge_amendment_into_final=1)
    state_3_20.save(skip_autoupdate=True)
    state_3_21 = State(name='abgelehnt',
                        workflow=workflow_3,
                        recommendation_label='Ablehnung',
                        css_class='red',
                        merge_amendment_into_final=-1)
    state_3_21.save(skip_autoupdate=True)
    state_3_22 = State(name='nicht befasst',
                        workflow=workflow_3,
                        recommendation_label='Nichtbefassung',
                        css_class='grey',
                        merge_amendment_into_final=-1)
    state_3_22.save(skip_autoupdate=True)
    state_3_23 = State(name='zurückgezogen',
                        workflow=workflow_3,
                        dont_set_identifier=True,
                        css_class='grey',
                        merge_amendment_into_final=-1)
    state_3_23.save(skip_autoupdate=True)
    state_3_1.next_states.add(state_3_2, state_3_3)
    state_3_2.next_states.add(state_3_4, state_3_23)
    state_3_4.next_states.add(state_3_5, state_3_23)
    state_3_5.next_states.add(state_3_6, state_3_23)
    state_3_6.next_states.add(state_3_7, state_3_23)
    state_3_7.next_states.add(state_3_8, state_3_23)
    state_3_8.next_states.add(state_3_9, state_3_23)
    state_3_9.next_states.add(state_3_10, state_3_23)
    state_3_10.next_states.add(state_3_20, state_3_21, state_3_22, state_3_23)
    workflow_3.first_state = state_3_1
    workflow_3.save(skip_autoupdate=True)


    # verdi workflow
    workflow_4 = Workflow(name='ver.di')
    workflow_4.save(skip_autoupdate=True)
    state_4_1 = State(name='in Bearbeitung',
                        workflow=workflow_4,
                        restriction=[
                            "is_submitter",
                            "managers_only"
                        ],
                        allow_submitter_edit=True,
                        dont_set_identifier=True,
                        merge_amendment_into_final=-1)
    state_4_1.save(skip_autoupdate=True)
    state_4_2 = State(name='gestellt',
                        workflow=workflow_4,
                        restriction=[
                            "is_submitter",
                            "managers_only"
                        ],
                        dont_set_identifier=True,
                        merge_amendment_into_final=-1)
    state_4_2.save(skip_autoupdate=True)
    state_4_3 = State(name='verworfen',
                        workflow=workflow_4,
                        restriction=[
                            "is_submitter",
                            "managers_only"
                        ],
                        dont_set_identifier=True,
                        css_class='grey',
                        merge_amendment_into_final=-1)
    state_4_3.save(skip_autoupdate=True)
    state_4_4 = State(name='geprüft',
                        workflow=workflow_4,
                        restriction=[
                            "is_submitter",
                            "managers_only"
                        ],
                        dont_set_identifier=True,
                        merge_amendment_into_final=-1)
    state_4_4.save(skip_autoupdate=True)
    state_4_5 = State(name='zugeordnet',
                        workflow=workflow_4,
                        merge_amendment_into_final=-1)
    state_4_5.save(skip_autoupdate=True)
    state_4_6 = State(name='Empfehlung der ABK liegt vor',
                        workflow=workflow_4,
                        allow_create_poll=True,
                        merge_amendment_into_final=-1)
    state_4_6.save(skip_autoupdate=True)
    state_4_10 = State(name='angenommen',
                        workflow=workflow_4,
                        recommendation_label='Annahme',
                        css_class='green',
                        merge_amendment_into_final=1)
    state_4_10.save(skip_autoupdate=True)
    state_4_11 = State(name='angenommen und weitergeleitet an',
                        workflow=workflow_4,
                        recommendation_label='Annahme und Weiterleitung an',
                        show_recommendation_extension_field=True,
                        show_state_extension_field=True,
                        css_class='green',
                        merge_amendment_into_final=1)
    state_4_11.save(skip_autoupdate=True)
    state_4_12 = State(name='angenommen in geänderter Fassung',
                        workflow=workflow_4,
                        recommendation_label='Annahme in geänderter Fassung',
                        css_class='green',
                        merge_amendment_into_final=1)
    state_4_12.save(skip_autoupdate=True)
    state_4_13 = State(name='angenommen in geänderter Fassung und weitergeleitet an',
                        workflow=workflow_4,
                        recommendation_label='Annahme in geänderter Fassung und Weiterleitung an',
                        show_recommendation_extension_field=True,
                        show_state_extension_field=True,
                        css_class='green',
                        merge_amendment_into_final=1)
    state_4_13.save(skip_autoupdate=True)
    state_4_14 = State(name='angenommen als Arbeitsmaterial zu Antrag',
                        workflow=workflow_4,
                        recommendation_label='Annahme als Arbeitsmaterial zu Antrag',
                        show_recommendation_extension_field=True,
                        show_state_extension_field=True,
                        css_class='green',
                        merge_amendment_into_final=1)
    state_4_14.save(skip_autoupdate=True)
    state_4_15 = State(name='angenommen als Arbeitsmaterial zur Weiterleitung an',
                        workflow=workflow_4,
                        recommendation_label='Annahme als Arbeitsmaterial zur Weiterleitung an',
                        show_recommendation_extension_field=True,
                        show_state_extension_field=True,
                        css_class='green',
                        merge_amendment_into_final=1)
    state_4_15.save(skip_autoupdate=True)
    state_4_16 = State(name='angenommen in geänderter Fassung durch Änderungsantrag',
                        workflow=workflow_4,
                        recommendation_label='Annahme in geänderter Fassung durch Änderungsantrag',
                        show_recommendation_extension_field=True,
                        show_state_extension_field=True,
                        css_class='green',
                        merge_amendment_into_final=1)
    state_4_16.save(skip_autoupdate=True)
    state_4_17 = State(name='angenommen in geänderter Fassung als Material',
                        workflow=workflow_4,
                        recommendation_label='Annahme in geänderter Fassung als Material',
                        show_recommendation_extension_field=True,
                        show_state_extension_field=True,
                        css_class='green',
                        merge_amendment_into_final=1)
    state_4_17.save(skip_autoupdate=True)
    state_4_18 = State(name='erledigt durch',
                        workflow=workflow_4,
                        recommendation_label='Erledigt durch',
                        show_recommendation_extension_field=True,
                        show_state_extension_field=True,
                        css_class='grey',
                        merge_amendment_into_final=-1)
    state_4_18.save(skip_autoupdate=True)
    state_4_19 = State(name='abgelehnt',
                        workflow=workflow_4,
                        recommendation_label='Ablehnung',
                        css_class='red',
                        merge_amendment_into_final=-1)
    state_4_19.save(skip_autoupdate=True)
    state_4_20 = State(name='nicht befasst',
                        workflow=workflow_4,
                        recommendation_label='Nichtbefassung',
                        css_class='grey',
                        merge_amendment_into_final=-1)
    state_4_20.save(skip_autoupdate=True)
    state_4_21 = State(name='zurückgezogen',
                        workflow=workflow_4,
                        dont_set_identifier=True,
                        css_class='grey',
                        merge_amendment_into_final=-1)
    state_4_21.save(skip_autoupdate=True)
    state_4_22 = State(name='Sonstiges',
                        workflow=workflow_4,
                        recommendation_label='Sonstiges',
                        show_recommendation_extension_field=True,
                        show_state_extension_field=True,
                        css_class='grey',
                        merge_amendment_into_final=-1)
    state_4_22.save(skip_autoupdate=True)
    state_4_1.next_states.add(state_4_2, state_4_3)
    state_4_2.next_states.add(state_4_4, state_4_21)
    state_4_4.next_states.add(state_4_5, state_4_21)
    state_4_5.next_states.add(state_4_6, state_4_21)
    state_4_6.next_states.add(state_4_10, state_4_11, state_4_12, state_4_13, state_4_14, state_4_15, state_4_16, state_4_17, state_4_18, state_4_19, state_4_20, state_4_21, state_4_22)
    workflow_4.first_state = state_4_1
    workflow_4.save(skip_autoupdate=True)


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
