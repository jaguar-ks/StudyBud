from django.db import models
from django.contrib.auth.models import User

# The Topic model
class Topic(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

# The Room model
class Room(models.Model):
    
    members = models.ManyToManyField(User, related_name='members', blank=True)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    # This atribute represent the room's name
    name = models.CharField(max_length=200)
    # This attribute represent the room's discreption
    description = models.TextField(null=True, blank=True)
    # This attribute will change automaticlly every time the room got updated
    updated = models.DateTimeField(auto_now=True)
    # This attribute will take it's value up on the creation
    created = models.DateTimeField(auto_now_add=True)
    
    # Room string rpresentation
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-updated', '-created']

# The Message model
class Message(models.Model):
    # this attribute represent the user who is sending the message
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    # this attribute represent a room
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    # This attribute represent the message text that wil be sent
    body = models.TextField()
    # This attribute will change automaticlly every time the message got updated
    updated = models.DateTimeField(auto_now=True)
    # This attribute will take it's value up on the creation
    created = models.DateTimeField(auto_now_add=True)
    
    # Message string represantation
    def __str__(self):
        r = self.body[0:40]
        if len(self.body) > 40:r+='...'
        return r
    
    class Meta:
        ordering = ['-updated', '-created']


