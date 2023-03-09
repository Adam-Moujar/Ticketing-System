from ticketing.apps import TicketingConfig

sequence_to_classify = 'How can I improve my critical thinking skills?'
candidate_labels = [
    'Housing & accomodation support',
    'Fees, funding & money advice',
    'Appeals, Complaints & Misconduct',
    'Administration',
    'Academic Digital Employability Skills',
    'Dignity & Inclusion',
]
print(
    TicketingConfig.CLASSIFIER(
        sequence_to_classify, candidate_labels, multi_label=True
    )
)
