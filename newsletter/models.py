from django.db import models


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    user_type = models.CharField(max_length=20, blank=True,
                                 choices=[('salaried', 'Salaried'),
                                          ('freelancer', 'Freelancer'),
                                          ('business', 'Business'),
                                          ('investor', 'Investor')])
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email


class CALead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15)
    city = models.CharField(max_length=100, blank=True)
    query_type = models.CharField(max_length=50,
                                  choices=[('itr', 'ITR Filing'),
                                           ('gst', 'GST Help'),
                                           ('planning', 'Tax Planning'),
                                           ('business', 'Business Tax'),
                                           ('other', 'Other')])
    message = models.TextField(blank=True)
    source_tool = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, default='new',
                              choices=[('new', 'New'),
                                       ('contacted', 'Contacted'),
                                       ('converted', 'Converted')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.query_type} ({self.created_at.date()})"
