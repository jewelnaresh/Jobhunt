from django.db import models
from django.shortcuts import reverse

# class JobData(models.Model):
#     company_name = models.CharField(max_length=32)
#     job_title = models.CharField(max_length=32)
#     link = models.CharField(max_length=64)

#     def __str__(self):
#         return f'{self.company_name} - {self.job_title}'
# 

class Jobseeker(models.Model):
    name = models.CharField(max_length=128)
    job_title = models.CharField(max_length=128)
    location = models.CharField(max_length=128)
    description = models.TextField(null=True)

    def __str__(self):
        return f'{self.name} - {self.job_title}'



# class Company(models.Model):
#     name = models.CharField(max_length=128)
#     def __str__(self):
#         return f'{self.name}'


class JobData(models.Model):
    company_name = models.CharField(max_length=128)
    job_title = models.CharField(max_length=128)
    link = models.CharField(max_length=64)
    slug = models.SlugField(default="test-job")

    def __str__(self):
        return f'{self.company_name} - {self.job_title}'


    def get_absolute_url(self):
        return reverse('product', kwargs={
            'slug': self.slug
        })
