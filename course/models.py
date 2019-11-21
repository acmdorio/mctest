'''
=====================================================================
Copyright (C) 2019 Francisco de Assis Zampirolli
from Federal University of ABC and individual contributors.
All rights reserved.

This file is part of webMCTest 1.1 (or MCTest 5.1).

Languages: Python 3.7, Django 2.2.4 and many libraries described at
github.com/fzampirolli/mctest

You should cite some references included in vision.ufabc.edu.br:8000
in any publication about it.

webMCTest is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License
(gnu.org/licenses/agpl-3.0.txt) as published by the Free Software
Foundation, either version 3 of the License, or (at your option) 
any later version.

webMCTest is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

=====================================================================
'''
from django.db import models
# from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from account.models import User
from student.models import Student


# Create your models here.
class Institute(models.Model):
    institute_name = models.CharField(max_length=50,
                                      # help_text = _("Institute name"),
                                      verbose_name=_("Institute name"),
                                      )
    institute_code = models.CharField(max_length=20,
                                      # help_text = _("Institute code"),
                                      verbose_name=_("Institute code"),
                                      )
    institute_logo = models.CharField(max_length=20,
                                      # help_text = _("Institute logo"),
                                      verbose_name=_("Institute logo"),
                                      )
    institute_url = models.CharField(max_length=20,
                                     help_text=_("All teachers must register institutional email"),
                                     verbose_name=_("Institute url"),
                                     )
    institute_exams_generated = models.IntegerField(default=0,
                                                    help_text=_(
                                                        "Total of exams generated per student. Remember, when "
                                                        "creating an exam, it can be applied across multiple "
                                                        "classrooms and to multiple students."),
                                                    verbose_name=_("Exams generated by the Institute"),
                                                    )
    institute_exams_corrected = models.IntegerField(default=0,
                                                    help_text=_(
                                                        "Total of corrected exams. Remember, some students may be "
                                                        "absent."),
                                                    verbose_name=_("Exams corrected by the Institute"),
                                                    )
    institute_questions_corrected = models.IntegerField(default=0,
                                                        help_text=_("Total of corrected question."),
                                                        verbose_name=_("Questions corrected by the Institute"),
                                                        )
    # institute_date = models.DateTimeField(#null=True, blank=True,
    #    help_text = _("Date of last update, format: DD/MM/YYYY"),
    #    verbose_name=_("Date last update"),
    # )
    institute_profs = models.ManyToManyField(User, blank=True,
                                             verbose_name=_("Institute professors"),
                                             )
    institute_coords = models.ManyToManyField(User, blank=True,
                                              related_name='institute2',  # relacionamento reverso
                                              verbose_name=_("Institute coordinators"),
                                              )

    class Meta:
        ordering = ["institute_code", "institute_name"]

    def __str__(self):
        return self.institute_name


class Course(models.Model):
    institutes = models.ManyToManyField(Institute,
                                        related_name='courses2',  # relacionamento reverso
                                        blank=True)
    course_name = models.CharField(max_length=100,
                                   help_text=_("Course name - does not include the institute code"),
                                   verbose_name=_("Course name"),
                                   )
    course_code = models.CharField(max_length=20,
                                   # help_text = _("Course code"),
                                   verbose_name=_("Course code"),
                                   )

    course_profs = models.ManyToManyField(User, blank=True,
                                          verbose_name=_("Course professors"),
                                          )
    course_coords = models.ManyToManyField(User, blank=True,
                                           related_name='course2',  # relacionamento reverso
                                           verbose_name=_("Course coordinators"),
                                           )

    class Meta:
        ordering = ["institutes__institute_code", "course_name"]

    def __str__(self):
        # return self.course_name
        return ' - '.join([', '.join([i.institute_code for i in self.institutes.all()]), self.course_name])


class Discipline(models.Model):
    courses = models.ManyToManyField(Course,
                                     related_name='disciples2',  # relacionamento reverso
                                     blank=True,
                                     verbose_name=_("Discipline course"),
                                     )
    discipline_name = models.CharField(max_length=100,
                                       verbose_name=_("Discipline name"),
                                       )
    discipline_code = models.CharField(max_length=20,
                                       verbose_name=_("Discipline code"),
                                       )
    discipline_objective = models.TextField(default='', blank=True,
                                            verbose_name=_("Discipline objective"),
                                            )

    discipline_profs = models.ManyToManyField(User, blank=True,
                                              # related_name='disciples2', #relacionamento reverso
                                              verbose_name=_("Discipline professors"),
                                              )
    discipline_coords = models.ManyToManyField(User, blank=True,
                                               related_name='disciples2',  # relacionamento reverso
                                               verbose_name=_("Discipline coordinators"),
                                               )

    class Meta:
        ordering = ["courses__institutes__institute_code", "courses__course_code", "discipline_name"]

    def __str__(self):
        str = []
        for c in self.courses.all():
            for i in c.institutes.all():
                str.append(i.institute_code)
        return ' - '.join([
            ', '.join(str),
            ', '.join([c.course_code for c in self.courses.all()]),
            self.discipline_name,
            # Discipline.objects.filter(discipline_profs=self.user),
        ])
        # return '[{0}]  {1}'.format(self.courses.course_name, self.discipline_name)
        # return Classroom.objects.filter(discipline__discipline_profs=self.request.user)


class Classroom(models.Model):
    students = models.ManyToManyField(Student,
                                      related_name='classrooms2',  # relacionamento reverso
                                      blank=True,
                                      verbose_name=_("Classroom students"),
                                      )
    discipline = models.ForeignKey(Discipline,
                                   related_name='classrooms2',  # relacionamento reverso
                                   on_delete=models.CASCADE,
                                   verbose_name=_("Classroom discipline"),
                                   )
    # discipline_profs = models.ManyToManyField(User)
    # classroom_who_created = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    classroom_profs = models.ManyToManyField(User, blank=True,
                                             verbose_name=_("Classroom professors"),
                                             )
    classroom_code = models.CharField(max_length=20,
                                      verbose_name=_("Classroom code"),
                                      )
    classroom_room = models.CharField(max_length=20,
                                      verbose_name=_("Classroom room"),
                                      )
    classroom_days = models.CharField(max_length=20, blank=True,

                                      verbose_name=_("Classroom days"),
                                      )
    classroom_type_choice = (
        ('PClass', 'Practical Class'),
        ('TClass', 'Theoretical Class'),
    )
    classroom_type = models.CharField(default='', max_length=6,
                                      choices=classroom_type_choice,
                                      verbose_name=_("Classroom type"),
                                      )

    class Meta:
        ordering = ["discipline__courses__institutes__institute_code", "discipline__discipline_code", "classroom_code"]

    def __str__(self):
        return ' - '.join([', '.join([d.discipline_code for d in Discipline.objects.all() if (d == self.discipline)]),
                           self.classroom_code])
        # return ' - '.join([', '.join([self.discipline.classrooms.all()]), self.classroom_code])
        # return self.classroom_code
        # return '[{0}]  {1}'.format(self.discipline.discipline_code, self.classroom_code)