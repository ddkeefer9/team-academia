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
    """
    Notes on the usage of this table:
        The assessment table contains high level information of a given assessment.
        title (CharField): A title given to the assessment.
        domainexamination (BooleanField): A boolean for if assessment is an examination.
        domainproduct (BooleanField): A boolean for if the assessment is a product.
        domainperformance (BooleanField): A boolean for if the assessment is a performance.
        directmeasure (BooleanField): A boolean for if the assessment is a direct measure. (*)
        numberofuses (IntegerField): A count for the number of times 
    """
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
    """
    Notes on the usage of this table:
        This table contains information on the collected data from a given version of an assesment.
        numberstudents (IntegerField): The count of students include in this assessment version.
        overallproficient (IntegerField): The count of students with a proficient assessment.
        assessmentversion (ForeignKey): A foreign key to the assessment version table.
        datarange (CharField): A data range for the collection period of this assessment version.
    Additional Remarks:
        datarange is not standard across programs/departments. 
    """
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
    """
    Notes on the usage of this table:
        The assessmentversion table provides high level information about a given version of an assessment.
        date (DateField): Date of the assessment version record.
        description (CharField): A description of the assessment.
        finalterm (BooleanField): Boolean of whether the assessment was done in the last term before graduation.
        where (CharField): A description of how the assessment is to be conducted (hence where).
        allstudents (BooleanField): Required for all students or not.
        sampledescription (CharField): Additional description of the assessment. Only available if all students were not assessed.
        Describes how the assessment was sampled.
        frequency (CharField): The sampling frequency in years for this assessment.
        threshold (CharField): The threshold for the measurement of this assessment (percentage, pass/fail, etc.).
        target (IntegerField): A target percentage of proficiency for the assessment.
        changedfromprior (BooleanField): Was the assessment changed since last sample/assessment version?
        slo (ForeignKey): A foreign key to MakereportsSloinreport which contains the SLO as it is in the particular report.
        number (IntegerField): The SLO number associated with the prior foreign key.
        frequencychoice (CharField): Letter for the rate of the assessment (Y for yearly, S for semester, O for other)
    """
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
    """
    Notes on the usage of this table:
        This table contains information relating to the college.
        name (CharField): The name of the college.
        active (BooleanField): College active or not.
    """
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
        name (CharField): The name of the degree program.
        level (CharField): The level of the degree program (UG for undergraduate for example)
        cycle (IntegerField): Their reporting cycle.
        department (ForeignKey): The department that coordinates this degree program
        startingyear (IntegerField): The starting year of their current reporting cycle.
        active (BooleanField): A boolean of whether the program is active or inactive
        accredited (BooleanField): A boolean of whether this program is accredited or not.
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
    
    def __str__(self):
        return self.name


class MakereportsDepartment(models.Model):
    """
    Notes on the usage of this table:
        The department table contains high-level information relating to the department.
        name (CharField): The department name.
        college (ForeignKey): A foreign key to the MakereportsCollege table.
        active (BooleanField): Boolean for if department active or not.
    """
    name = models.CharField(max_length=100)
    college = models.ForeignKey(MakereportsCollege, models.DO_NOTHING)
    active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'makeReports_department'

    def __str__(self):
        return self.name


class MakereportsGradedrubric(models.Model):
    """
    Notes on the usage of this table:
        This table contains the feedback on the graded rubric.
        rubricversion (ForeignKey): A foreign key to the MakereportsRubric table
        section1comment (CharField): Comment section for the "Student Learning Outcomes (SLOs)"
        section2comment (CharField): Comment section for the "Assessment Methods"
        section3comment (CharField): Comment section for the "Data Collection and Analysis"
        section4comment (CharField): Comment section for the "Decisions and Actions"
        complete (BooleanField): BooleanField describing whether the graded rubric is completed.
    """
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
        author (CharField): This is the author of the report
        section1comment (CharField): Comment section for the "Student Learning Outcomes (SLOs)"
        section2comment (CharField): Comment section for the "Assessment Methods"
        section3comment (CharField): Comment section for the "Data Collection and Analysis"
        section4comment (CharField): Comment section for the "Decisions and Actions"
        submitted (BooleanField): Boolean of whether the report has been submitted for review or not.
        degreeprogram (ForeignKey): The degree program this report is for.
        rubric (OneToOneField): A one-to-one foreign key to the rubric this report is utilizing.
        year (IntegerField): The year this report was submitted.
        returned (BooleanField): Whether the report has been returned from review.
        date_range_of_reported_data (CharField): A CharField formatting the range of years this report covers.
        numberofslos (IntegerField): The number of SLOs this report contains
        accreditorestslos (BooleanField): SLOs established by accrediting body. This means the set of SLOs were not
        developed internally but come from a standard external source.
        accreditorrevslos (BooleanField): SLOs reviewed by accrediting body. This is a bit stricter than the prior.
        It means that the SLOs are actually reviewed and enforced by the accrediting body.
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
    """
    Notes on the usage of this table:
        This table contains high level information on the rubric in the makereports process.
        date (DateField): Creation date for this report rubric.
        fullfile (CharField): An absolute path to the .pdf describing the rubric.
        name (CharField): The name of the rubric.
    Additional Comments:
        Only two rubrics, an Accredited Assessment Rubric, and an Non-accredited Assessment Rubric.
        respective pk for each is 5 & 4.
    """
    date = models.DateField()
    fullfile = models.CharField(db_column='fullFile', max_length=100, blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'makeReports_rubric'


class MakereportsRubricitem(models.Model):
    """
    Notes on the usage of this table:
        This table contains a description of a particular rubric item.
        text (CharField): A text description of the rubric item.
        section (IntegerField): The section number this rubric is assigned to.
        rubricversion (ForeignKey): A foreign key to the MakereportsRubric table, see its docstring for additional information.
        order (IntegerField): Ordering sequence for the rubric item. Lower numbers are displayed first.
        dmetext (CharField): DME - did not meet expectations. This is the text in the rubric that goes into the DME column.
        eetext (CharField): EE - exceeds expectations. This is the text in the rubric that goes into the EE column.
        metext (CharField): ME - meets expectations with concerns. This is the text in the rubric that goes into the ME column.
        abbreviation (CharField): A code for the rubric item, e.g., one could shortcut the rubric "SLOs consists of a single construct" as "SCON".
    """
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
        blooms (CharField): The blooms taxonomy that the SLO is assessing
        numberofuses (IntegerField): The number of times the SLO has been used (*)
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
    """
    Notes on the Usage of this table:
        Contains foreign keys relating to goals for graduation.
        slo (ForeignKey): A foreign key to the SLO used for the grad goal.
        gradgoal (ForeignKey): A foreign key to a table containing the raw HTML describing the grad goal.
    """
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
        report (ForeignKey): A foreign key that creates a relation to the MakereportReport that this SLO is being used within.
        slo (ForeignKey): A foreign key that denotes the MakereportsSlo, which itself contains additional information about the SLO (More info is in "MakerportsSlo" docstring)
        date (DateField): A date, that I am assuming relates to when this SLO was added to a report. (*)
        goaltext (CharField): The goal of the SLO.
        number (IntegerField): The position (or number) that the SLO belongs to in the report. (1 for 1st, 2 for 2nd, etc.)
        numberofassess (integerField): The number of times this SLO has been used for an assessment.
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
        status (CharField): The status of the SLO, this can be Met, Partially Met, Not Met, or Unknown.
        sloir (OneToOneField): This is a one-to-one foreign key to the SLO in report that this status is referring to.
        override (BooleanField): This is a mechanism to allow the overriding of the Slostatus if needed.
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
