import time


from transformers import pipeline 
t0 = time.time()
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
t1 = time.time()
total1 = t1 - t0
print(total1)
sequence_to_classify = "How can I improve my critical thinking skills?"
candidate_labels = ["Housing & accomodation support",
                     "Fees, funding & money advice", 
                     "Appeals, Complaints & Misconduct",  
                     "Administration" , 
                     "Academic Digital Employability Skills", 
                     "Dignity & Inclusion"]
classifier(sequence_to_classify, candidate_labels, multi_label = True)
t2 = time.time()
print(classifier(sequence_to_classify, candidate_labels))
total2 = t2 - t1
print(total2)