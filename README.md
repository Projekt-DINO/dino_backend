# DINO Backend

Django-Backend für das Dino-Projekt



 **Globals**

Um die AWS Daten, welche in der [IAM Konsole](https://console.aws.amazon.com/iam/home?region=eu-west-1#/home) am Nutzer hängen, zu speichern, muss eine Datei namens `globals.py` erstellt werden. Diese liegt im Pfad: `api/database/dynamodb/globals/globals.py` und mittels `import globals` importiert. 

Die Datei sieht folgendermaßen aus: 

```
USER_NAME = "infowiss"
AWS_ACCESS_KEY = "..."
AWS_SECRET_ACCESS_KEY = "..."
AWS_REGION = "eu-west-1"
```

Die beiden Keys wurden von `Alexander Teusz` an alle Teilnehmer der Coding Gruppe gesendet. 