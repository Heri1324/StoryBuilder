from student2_servicii import Student2Services

svc = Student2Services(language="ro-RO")

text = svc.listen_sentence()
print("STT:", text)

query = svc.make_query(text)
print("Query imagini:", query)

svc.speak(text)
