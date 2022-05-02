from main.models import MakereportsAssessmentdata, MakereportsAssessmentversion, MakereportsCollege, MakereportsDegreeprogram, MakereportsDepartment, MakereportsReport, MakereportsSlo, MakereportsSloinreport

class CollegeQueries:
    def getCollegeQSFromID(college_id):
        """
        Gets the college query set to be sent into the pdf generation plotting methods

        Returns:
            - collegeQS: QuerySet containing one college name
        """
        collegeQS = MakereportsCollege.objects.filter(pk=college_id)
        return collegeQS

    def getDegreesFromCollegeQS(collegeQS):
        """
        Gets the degree query set that includes every degree program listed under the college name

        Returns:
            - degreeProgramQS: A query set of degree programs
        """
        departmentQS = MakereportsDepartment.objects.filter(college__in=collegeQS)
        degreeProgramQS = MakereportsDegreeprogram.objects.filter(department__in=departmentQS)
        return degreeProgramQS

class DegreeQueries:
    def pdfDegreeAssessmentQuery(degree_id):
        """
        Queries to help with College Comparison Assessment Proficiency

        Queries from the MakereportsReport table -> MakereportsAssessmentversion table -> MakereportsAssessmentdata table.

        Returns:
            assessmentDataQS - The assessment data for the given degree_id
        """

        makeReportQS = MakereportsReport.objects.filter(degreeprogram=degree_id)
        if len(makeReportQS) < 1:  # Degree program does not have a report associated with it.
            return None
        
        reportsAssessmentVersionQS = MakereportsAssessmentversion.objects.filter(report__in=makeReportQS)
        
        assessmentDataQS = MakereportsAssessmentdata.objects.filter(assessmentversion__in=reportsAssessmentVersionQS)
        return assessmentDataQS
        
    def pdfDegreeReportQuery(degree_id):
        """
        Queries to help with College Number of SLOs Comparison

        Queries from the MakereportsReport table.

        Returns:
            numOfSLOsDataQS - The number of SLOs for the given degree_id
        """
        makeReportQS = MakereportsReport.objects.filter(degreeprogram=degree_id)
        return makeReportQS
    
    def pdfDegreeBloomQuery(degree_id):
        """
        Queries to help with College Comparison for Bloom Taxonomies

        Queries from the MakereportsReport table -> MakereportsSloinreport table -> MakereportsSlo table.

        Returns:
            sloBloomQS - The bloom taxonomies used for each SLO for the given degree_id
        """

        makeReportQS = MakereportsReport.objects.filter(degreeprogram=degree_id)
        if len(makeReportQS) < 1:  # Degree program does not have a report associated with it.
            return None
        
        sloInReportQS = MakereportsSloinreport.objects.filter(report__in=makeReportQS)
        
        sloBloomQS = MakereportsSlo.objects.filter(makereportssloinreport__in = sloInReportQS)
        return sloBloomQS