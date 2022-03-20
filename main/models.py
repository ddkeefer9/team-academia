# coding=utf8
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DjangoSummernoteAttachment(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    file = models.CharField(max_length=100)
    uploaded = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_summernote_attachment'


class MakereportsAnnouncement(models.Model):
    text = models.CharField(max_length=2000)
    expiration = models.DateField()
    creation = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'makeReports_announcement'


class MakereportsAssessment(models.Model):
    title = models.CharField(max_length=300)
    domainexamination = models.BooleanField(db_column='domainExamination')  # Field name made lowercase.
    domainproduct = models.BooleanField(db_column='domainProduct')  # Field name made lowercase.
    domainperformance = models.BooleanField(db_column='domainPerformance')  # Field name made lowercase.
    directmeasure = models.BooleanField(db_column='directMeasure')  # Field name made lowercase.
    numberofuses = models.IntegerField(db_column='numberOfUses')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'makeReports_assessment'


class MakereportsAssessmentaggregate(models.Model):
    aggregate_proficiency = models.IntegerField()
    met = models.BooleanField()
    assessmentversion = models.OneToOneField('MakereportsAssessmentversion', models.DO_NOTHING, db_column='assessmentVersion_id')  # Field name made lowercase.
    override = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'makeReports_assessmentaggregate'


class MakereportsAssessmentdata(models.Model):
    numberstudents = models.IntegerField(db_column='numberStudents')  # Field name made lowercase.
    overallproficient = models.IntegerField(db_column='overallProficient')  # Field name made lowercase.
    assessmentversion = models.ForeignKey('MakereportsAssessmentversion', models.DO_NOTHING, db_column='assessmentVersion_id')  # Field name made lowercase.
    datarange = models.CharField(db_column='dataRange', max_length=500)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'makeReports_assessmentdata'


class MakereportsAssessmentsupplement(models.Model):
    supplement = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'makeReports_assessmentsupplement'


class MakereportsAssessmentversion(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=1000)
    finalterm = models.BooleanField(db_column='finalTerm')  # Field name made lowercase.
    where = models.CharField(max_length=500)
    allstudents = models.BooleanField(db_column='allStudents')  # Field name made lowercase.
    sampledescription = models.CharField(db_column='sampleDescription', max_length=500, blank=True, null=True)  # Field name made lowercase.
    frequency = models.CharField(max_length=500)
    threshold = models.CharField(max_length=500)
    target = models.IntegerField()
    assessment = models.ForeignKey(MakereportsAssessment, models.DO_NOTHING)
    report = models.ForeignKey('MakereportsReport', models.DO_NOTHING)
    changedfromprior = models.BooleanField(db_column='changedFromPrior')  # Field name made lowercase.
    slo = models.ForeignKey('MakereportsSloinreport', models.DO_NOTHING)
    number = models.IntegerField()
    frequencychoice = models.CharField(db_column='frequencyChoice', max_length=100)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'makeReports_assessmentversion'


class MakereportsAssessmentversionSupplements(models.Model):
    assessmentversion = models.ForeignKey(MakereportsAssessmentversion, models.DO_NOTHING)
    assessmentsupplement = models.ForeignKey(MakereportsAssessmentsupplement, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'makeReports_assessmentversion_supplements'
        unique_together = (('assessmentversion', 'assessmentsupplement'),)


class MakereportsCollege(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'makeReports_college'
    
    def __str__(self):
        return self.name


class MakereportsDataadditionalinformation(models.Model):
    comment = models.CharField(max_length=3000)
    report = models.ForeignKey('MakereportsReport', models.DO_NOTHING)
    supplement = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'makeReports_dataadditionalinformation'


class MakereportsDecisionsactions(models.Model):
    text = models.CharField(max_length=3000)
    sloir = models.OneToOneField('MakereportsSloinreport', models.DO_NOTHING, db_column='sloIR_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'makeReports_decisionsactions'


class MakereportsDegreeprogram(models.Model):
    """
    Notes on the usage of this table:
        The degreeprogram table contains information regarding a degree program at UNO.
        name: The name of the degree program.
        level: The level of the degree program (UG for undergraduate for example)
        cycle: Their reporting cycle.
        department: The department that coordinates this degree program
        startingyear: The starting year of their current reporting cycle.
        active: A boolean of whether the program is active or inactive
        accredited: A boolean of whether this program is accredited or not.
    """
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=75)
    cycle = models.IntegerField(blank=True, null=True)
    department = models.ForeignKey('MakereportsDepartment', models.DO_NOTHING)
    startingyear = models.IntegerField(db_column='startingYear', blank=True, null=True)  # Field name made lowercase.
    active = models.BooleanField()
    accredited = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'makeReports_degreeprogram'
    
    # def __str__(self):
    #     return self.name


class MakereportsDepartment(models.Model):
    name = models.CharField(max_length=100)
    college = models.ForeignKey(MakereportsCollege, models.DO_NOTHING)
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'makeReports_department'

    def __str__(self):
        return self.name


class MakereportsGradedrubric(models.Model):
    rubricversion = models.ForeignKey('MakereportsRubric', models.DO_NOTHING, db_column='rubricVersion_id')  # Field name made lowercase.
    generalcomment = models.CharField(db_column='generalComment', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    section1comment = models.CharField(db_column='section1Comment', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    section2comment = models.CharField(db_column='section2Comment', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    section3comment = models.CharField(db_column='section3Comment', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    section4comment = models.CharField(db_column='section4Comment', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    complete = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'makeReports_gradedrubric'


class MakereportsGradedrubricitem(models.Model):
    grade = models.CharField(max_length=300)
    item = models.ForeignKey('MakereportsRubricitem', models.DO_NOTHING)
    rubric = models.ForeignKey(MakereportsGradedrubric, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'makeReports_gradedrubricitem'


class MakereportsGradgoal(models.Model):
    text = models.CharField(max_length=600)
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'makeReports_gradgoal'


class MakereportsGraph(models.Model):
    datetime = models.DateTimeField(db_column='dateTime')  # Field name made lowercase.
    graph = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'makeReports_graph'


class MakereportsProfile(models.Model):
    aac = models.BooleanField(blank=True, null=True)
    department = models.ForeignKey(MakereportsDepartment, models.DO_NOTHING, blank=True, null=True)
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'makeReports_profile'


class MakereportsReport(models.Model):
    """
    Notes on the usage of this table:
        The reports table contains high-level information regarding a report generated for a degree program.
        author: This is the author of the report
        section1comment:
        section2comment:
        section3comment:
        section4comment:
        submitted: Boolean of whether the report has been submitted for review or not.
        degreeprogram: The degree program this report is for.
        rubric: A foreign key to the rubric this report is utilizing.
        year: The year this report was submitted.
        returned: Whether the report has been returned from review.
        date_range_of_reported_data: A CharField formatting the range of years this report covers.
        numberofslos: The number of SLOs this report contains
        accreditorestslos: I have no clue. (*)
        accreditorrevslos: I have no clue. (*)
    Future Work:
        Variables denoted with (*) need to be inquired about to the sponsor.
    """
    author = models.CharField(max_length=100)
    section1comment = models.CharField(db_column='section1Comment', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    section2comment = models.CharField(db_column='section2Comment', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    section3comment = models.CharField(db_column='section3Comment', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    section4comment = models.CharField(db_column='section4Comment', max_length=2000, blank=True, null=True)  # Field name made lowercase.
    submitted = models.BooleanField()
    degreeprogram = models.ForeignKey(MakereportsDegreeprogram, models.DO_NOTHING, db_column='degreeProgram_id')  # Field name made lowercase.
    rubric = models.OneToOneField(MakereportsGradedrubric, models.DO_NOTHING, blank=True, null=True)
    year = models.IntegerField()
    returned = models.BooleanField()
    date_range_of_reported_data = models.CharField(max_length=500, blank=True, null=True)
    numberofslos = models.IntegerField(db_column='numberOfSLOs')  # Field name made lowercase.
    accredited = models.BooleanField()
    accreditorestslos = models.BooleanField(db_column='accreditorEstSLOs')  # Field name made lowercase.
    accreditorrevslos = models.BooleanField(db_column='accreditorRevSLOs')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'makeReports_report'

    def __str__(self):
        return f"{self.author}-{self.degreeprogram}-{self.year}"


class MakereportsReportsupplement(models.Model):
    supplement = models.CharField(max_length=100)
    report = models.ForeignKey(MakereportsReport, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'makeReports_reportsupplement'


class MakereportsRequiredfieldsetting(models.Model):
    name = models.CharField(max_length=200)
    required = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'makeReports_requiredfieldsetting'


class MakereportsResultcommunicate(models.Model):
    text = models.CharField(max_length=3000)
    report = models.ForeignKey(MakereportsReport, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'makeReports_resultcommunicate'


class MakereportsRubric(models.Model):
    date = models.DateField()
    fullfile = models.CharField(db_column='fullFile', max_length=100, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'makeReports_rubric'


class MakereportsRubricitem(models.Model):
    text = models.CharField(max_length=1000)
    section = models.IntegerField()
    rubricversion = models.ForeignKey(MakereportsRubric, models.DO_NOTHING, db_column='rubricVersion_id')  # Field name made lowercase.
    order = models.IntegerField(blank=True, null=True)
    dmetext = models.CharField(db_column='DMEtext', max_length=1000)  # Field name made lowercase.
    eetext = models.CharField(db_column='EEtext', max_length=1000)  # Field name made lowercase.
    metext = models.CharField(db_column='MEtext', max_length=1000)  # Field name made lowercase.
    abbreviation = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'makeReports_rubricitem'


class MakereportsSlo(models.Model):
    """
    Notes on the Usage of this table:
        MakereportsSlo contains additional information on the SLO itself.
        Blooms: The blooms taxonomy that the SLO is assessing
        Numberofuses: The number of times the SLO has been used (*)
    Definition for Blooms Abbreviations
        EV: Evaluation
        SN: Synthesis
        AN: Analysis
        AP: Application
        CO: Comprehension
        KN: Knowledge
    Future Work:
        Number of uses is ambiguous as we already have info with the SLOinreport regarding the number of assesses.
        Not sure exactly what "uses" means.
    """
    blooms = models.CharField(max_length=50)
    numberofuses = models.IntegerField(db_column='numberOfUses')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'makeReports_slo'


class MakereportsSloGradgoals(models.Model):
    slo = models.ForeignKey(MakereportsSlo, models.DO_NOTHING)
    gradgoal = models.ForeignKey(MakereportsGradgoal, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'makeReports_slo_gradGoals'
        unique_together = (('slo', 'gradgoal'),)


class MakereportsSloinreport(models.Model):
    """
    Notes on the Usage of this table:
        Sloinreport contains information regarding the used SLO in a report.
        report: A foreign key that creates a relation to the MakereportReport that this SLO is being used within.
        slo: A foreign key that denotes the MakereportsSlo, which itself contains additional information about the SLO (More info is in "MakerportsSlo" docstring)
        date: A date, that I am assuming relates to when this SLO was added to a report. (*)
        goaltext: The goal of the SLO.
        number: A number that has no meaning, it might relate to the range of years this SLO is applied to (2 for 2 years, 3 for 3 years, etc.) (*)
        numberofassess: The number of times this SLO has been used for an assessment, this is also a guess (*)
    Future Work:
        Variables marked with (*) could be inquired about to our sponsor.
    """
    report = models.ForeignKey(MakereportsReport, models.DO_NOTHING)
    slo = models.ForeignKey(MakereportsSlo, models.DO_NOTHING)
    changedfromprior = models.BooleanField(db_column='changedFromPrior')  # Field name made lowercase.
    date = models.DateField()
    goaltext = models.CharField(db_column='goalText', max_length=1000)  # Field name made lowercase.
    number = models.IntegerField()
    numberofassess = models.IntegerField(db_column='numberOfAssess')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'makeReports_sloinreport'

    def __str__(self):
        return f"{self.date}-{self.goaltext[0:20]}"


class MakereportsSlostatus(models.Model):
    """
    Notes on the Usage of this table:
        Slostatus contains information regarding if the SLO is not met, also contains a foreign key to the Sloinreport.
        status: The status of the SLO, this can be Met, Partially Met, Not Met, or Unknown.
        sloir: This is a foreign key to the SLO in report that this status is referring to.
        override: This is a mechanism to allow the overriding of the Slostatus if needed.
    """
    status = models.CharField(max_length=50)
    sloir = models.OneToOneField(MakereportsSloinreport, models.DO_NOTHING, db_column='sloIR_id')  # Field name made lowercase.
    override = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'makeReports_slostatus'


class MakereportsSlostostakeholder(models.Model):
    text = models.CharField(max_length=2000)
    report = models.ForeignKey(MakereportsReport, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'makeReports_slostostakeholder'
