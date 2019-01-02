#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Controller này dùng để biên tập một khóa học
"""
import xdj
@xdj.Controller(
    url="couserware/courses/editor",
    template="couserware/courses_editor.html"
)
class couserware_couser_controller(xdj.BaseController):
    def on_get(self,model):
        return self.render(model)
    def doLoadItem(self,model):
        if isinstance(model,xdj.Model):
            if model.post_data.course_id == "*":
                return {}
            else:
                import branding
                from opaque_keys import edx
                course_id = edx.locator.CourseLocator.from_string(model.post_data.course_id)
                ret = branding.CourseOverview.objects.get(id=course_id)
                import cms.djangoapps.contentstore.views.course as C
                from opaque_keys.edx.keys import CourseKey
                course_key = CourseKey.from_string(model.post_data.course_id)
                model.request._body = ""
                from openedx.core.djangoapps.models.course_details import CourseDetails
                details = CourseDetails.fetch(course_key)
                """
                details.pre_requisite_courses
                details.entrance_exam_enabled: Khi option này mà bật lên thì phần đề cương khóa học sẽ tự thêm một bài test
                details.entrance_exam_id
                details.entrance_exam_minimum_score_pct
                """
                model.request.method = "GET"
                ret_settings= C.settings_handler(model.request, course_key_string = model.post_data.course_id)
                return ret
    def doLoadSettings(self,model):
        """
        Lấy thông tin setting của khóa học
        :param model:
        :return:
        """
        """
        '/home/hcsadmin/edx-ginkgo.2-3/apps/edx/edx-platform/cms/djangoapps/contentstore/views/course.py'
        view_function.func_code.co_name
        'settings_handler'
        import cms.djangoapps.contentstore.views.course
        import cms.djangoapps.contentstore.views.course as C
        C.settings_handler
        request._body=""
        """
        import cms.djangoapps.contentstore.views.course as C
        model.request._body=""
        ret = C.settings_handler(model.request,{'course_key_string': u'course-v1:LV+001+001'})
        return ret
    def doLoadGrading(self,model):
        """

        :param model:
        :return:
        """
        """
        '/home/hcsadmin/edx-ginkgo.2-3/apps/edx/edx-platform/cms/djangoapps/contentstore/views/course.py'
        import cms.djangoapps.contentstore,views.course as C
        C.grading_handler(request,{'grader_index': None, 'course_key_string': u'course-v1:LV+001+001'})
        
        from models.settings.course_grading import CourseGradingModel
        CourseGradingModel.fetch(course_key)
        course_key = CourseKey.from_string(course_key_string)
        course_details = CourseGradingModel.fetch(course_key)
        
        """

        pass
    def doGetTeam(self,model):
        """
        Hàm này lấy danh sách các thành viên trong khóa học bao gồm instructors và staff

        :param model:
        :return:
        """
        """
        /home/hcsadmin/edx-ginkgo.2-3/apps/edx/edx-platform/cms/djangoapps/contentstore/views/user.py
        _manage_users(request, course_key)
        
        course_module = modulestore().get_course(course_key)
        instructors = set(CourseInstructorRole(course_key).users_with_role())
        # the page only lists staff and assumes they're a superset of instructors. Do a union to ensure.
        staff = set(CourseStaffRole(course_key).users_with_role()).union(instructors)
        formatted_users = []
        for user in instructors:
            formatted_users.append(user_with_role(user, 'instructor'))
        for user in staff - instructors:
            formatted_users.append(user_with_role(user, 'staff'))
        
        """
        pass
    def doEnroll(self,model):
        """
        Hàm này dùng để enroll user, ngay cả khi
        :param model:
        :return:
        """

        """
        '/home/hcsadmin/edx-ginkgo.2-3/apps/edx/edx-platform/common/djangoapps/student/models.py'
        from student.models import CourseEnrollment
        from opaque_keys import edx
        course_id = edx.locator.CourseLocator.from_string(model.post_data.course_id)
        CourseEnrollment.enroll(user, course_key)
        """
        pass
    def doAddUserToRoleInCourse(self,sender):
        """
        Hàm này dùng để add user vào role mà role này liên kết đến khóa học

        :param sender:
        :return:
        """
        """
        '/home/hcsadmin/edx-ginkgo.2-3/apps/edx/edx-platform/common/djangoapps/student/auth.py'
        import student.auth as auth
        import student.roles
        course_id = edx.locator.CourseLocator.from_string(model.post_data.course_id)
        role=student.roles.CourseInstructorRole(course_id)

        """
    def checkUserAndCourse(self,model):
        """
        Hàm này dùng để kiểm tra quyền của user trong khóa học
        :param sender:
        :return:
        """
        course_key = edx.locator.CourseLocator.from_string(model.post_data.course_id)
        from django.contrib.auth import get_user_model
        import cms.djangoapps.contentstore.views.course as C
        u = get_user_model().objects.get(username="user00300")
        ret = C.get_course_and_check_access(course_key, u)
        return ret
    def doGetListOfGroupStudentInCourseWare(self,model):
        course_id = edx.locator.CourseLocator.from_string(model.post_data.course_id)
        course = self.checkUserAndCourse(model)
        from xmodule.modulestore.django import modulestore
        import cms.djangoapps.contentstore.course_group_config as GCF
        GCF.GroupConfiguration
        GCF.GroupConfiguration.get_all_user_partition_details
        x = modulestore()
        lst = GCF.GroupConfiguration.get_all_user_partition_details(x, course)
        ret = [x for x in lst if x["schema"]!="enrollment_track"]
        return ret
    def doLoadAdvanceSettings(self,model):
        """
        Hàm này dùng để lấy mục advance settings của khóa học
        '/home/hcsadmin/edx-ginkgo.2-3/apps/edx/edx-platform/cms/djangoapps/contentstore/views/course.py'
        :param model:
        :return:
        """
        """
        cms/djangoapps/contentstore/views/course
        advanced_settings_handler
        from opaque_keys.edx.keys import CourseKey as CK
        course_key = CK.from_string(course_key_string)
        from cms.djangoapps.contentstore.views.course import get_course_and_check_access
        course_module = get_course_and_check_access(course_key, request.user)
        from models.settings.course_metadata import CourseMetadata
        CourseMetadata.fetch(course_module)
        """
        pass
    def doSaveAdvanceSettings(self,model):
        """
        Hàm này dùng để lưu phần cấu hình nân cao cho khóa học
        :param model:
        :return:
        """
        data = {
                'course_survey_name':
                    {
                        'deprecated': True,
                        'display_name': 'Pre-Course Survey Name',
                        'help': u'Name of SurveyForm to display as a pre-course survey to the user.',
                        'value': None
                     },
                'discussion_link':
                    {
                        'deprecated': True,
                        'display_name': u'Discussion Forum External Link',
                        'help': u'Allows specification of an external link to replace discussion forums.',
                        'value': None
                    },
                'course_survey_required':
                    {
                        'deprecated': True,
                        'display_name': u'Pre-Course Survey Required',
                        'help': u'Specify whether students must complete a survey before they can view your course content. '
                                u'If you set this value to true, you must add a name for the survey to the Course Survey Name setting above.',
                        'value': False
                    },
                'annotation_token_secret':
                    {
                        'deprecated': False,
                        'display_name': u'Secret Token String for Annotation',
                        'help': u'Enter the secret string for annotation storage. The textannotation, '
                                u'videoannotation, and imageannotation advanced modules require this string.',
                        'value': u'xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
                    },
                'remote_gradebook':
                    {
                        'deprecated': False,
                        'display_name': u'Remote Gradebook',
                        'help': u'Enter the remote gradebook mapping. '
                                u'Only use this setting when REMOTE_GRADEBOOK_URL has been specified.',
                        'value': {}
                    },
                'discussion_sort_alpha':
                    {
                        'deprecated': False,
                        'display_name': u'Discussion Sorting Alphabetical',
                        'help': u'Enter true or false. If true, discussion categories and subcategories are sorted alphabetically. '
                                u'If false, they are sorted chronologically by creation date and time.',
                        'value': False
                    },
                'is_new':
                    {
                        'deprecated': False,
                        'display_name': u'Course Is New',
                        'help': u'Enter true or false. If true, the course appears in the list of new courses on edx.org, '
                                u'and a New! badge temporarily appears next to the course image.',
                        'value': None
                    },
                'discussion_topics':
                    {
                        'deprecated': False,
                        'display_name': u'Discussion Topic Mapping',
                        'help': u'Enter discussion categories in the following format: '
                                u'"CategoryName": {"id": "i4x-InstitutionName-CourseNumber-course-CourseRun"}. '
                                u'For example, one discussion category may be "Lydian Mode": {'
                                u'"id": "i4x-UniversityX-MUS101-course-2015_T1"}. '
                                u'The "id" value for each category must be unique. '
                                u'In "id" values, the only special characters that are supported are underscore, '
                                u'hyphen, and period.',
                        'value':
                            {
                                'General':
                                    {
                                        'id': u'course'
                                    }
                            }
                    },
                'edxnotes':
                    {
                        'deprecated': False,
                        'display_name': u'Enable Student Notes',
                        'help': u'Enter true or false. If true, students can use the Student Notes feature.',
                        'value': False
                    },
                'issue_badges':
                    {
                        'deprecated': False,
                        'display_name': u'Issue Open Badges',
                        'help': u'Issue Open Badges badges for this course. '
                                u'Badges are generated when certificates are created.',
                        'value': True
                    },
                'enrollment_domain':
                    {
                        'deprecated': False,
                        'display_name': u'External Login Domain',
                        'help': u'Enter the external login method students can use for the course.',
                        'value': None
                    },
                'source_file':
                    {
                        'deprecated': True,
                        'display_name': u'LaTeX Source File Name',
                        'help': u'Enter the source file name for LaTeX.',
                        'value': None
                    },
                'course_edit_method':
                    {
                        'deprecated': True,
                        'display_name': u'Course Editor',
                        'help': u'Enter the method by which this course is edited ("XML" or "Studio").',
                        'value': u'Studio'
                    },
                'certificates_show_before_end':
                    {
                        'deprecated': True,
                        'display_name': u'Certificates Downloadable Before End',
                        'help': u"Enter true or false. If true, students can download certificates before the course ends, "
                                u"if they've met certificate requirements.",
                        'value': False
                    },
                'max_student_enrollments_allowed':
                    {
                        'deprecated': False,
                        'display_name': u'Course Maximum Student Enrollment',
                        'help': u'Enter the maximum number of students that can enroll in the course. '
                                u'To allow an unlimited number of students, enter null.',
                        'value': None
                    },
                'teams_configuration':
                    {
                        'deprecated': False,
                        'display_name': u'Teams Configuration',
                        'help': u'Specify the maximum team size and topics for teams inside the provided set of curly braces. '
                                u'Make sure that you enclose all of the sets of topic values within a set of square brackets,'
                                u'with a comma after the closing curly brace for each topic, '
                                u'and another comma after the closing square brackets. '
                                u'For example, to specify that teams should have a maximum of 5 participants '
                                u'and provide a list of 2 topics, enter the configuration in this format: '
                                u'{"topics": [{"name": "Topic1Name", "description": "Topic1Description", "id": "Topic1ID"}, '
                                u'{"name": "Topic2Name", "description": "Topic2Description", "id": "Topic2ID"}], "max_team_size": 5}. '
                                u'In "id" values, the only supported special characters are underscore, hyphen, and period.',
                        'value': {}
                    },
                'announcement':
                    {
                        'deprecated': False,
                        'display_name': 'Course Announcement Date',
                        'help': u'Enter the date to announce your course.',
                        'value': None
                    },
                'showanswer':
                    {
                        'deprecated': False,
                        'display_name': u'Show Answer',
                        'help': u'Specify when the Show Answer button appears for each problem. '
                                u'Valid values are "always", "answered", "attempted", "closed", "finished", "past_due", '
                                u'"correct_or_past_due", and "never".', u'value': u'finished'
                    },
                'display_name':
                    {
                        'deprecated': False,
                        'display_name': u'Course Display Name',
                        'help': u'Enter the name of the course as it should appear in the edX.org course list.',
                        'value': u'Django Web Framework'
                    },
                'video_speed_optimizations':
                    {
                        'deprecated': False,
                        'display_name': u'Enable video caching system',
                        'help': u'Enter true or false. If true, video caching will be used for HTML5 videos.',
                        'value': True
                    },
                'certificates_display_behavior':
                    {
                        'deprecated': False,
                        'display_name': u'Certificates Display Behavior',
                        'help': u'Enter end, early_with_info, or early_no_info. After certificate generation, '
                                u'students who passed see a link to their certificates on the dashboard and '
                                u'students who did not pass see information about the grading configuration. '
                                u'The default is end, which displays this certificate information to all students '
                                u'after the course end date. To display this certificate information to all '
                                u'students as soon as certificates are generated, enter early_with_info. '
                                u'To display only the links to passing students as soon as certificates are generated, '
                                u'enter early_no_info.',
                        'value': u'end'
                    },
                'enable_timed_exams':
                    {
                        'deprecated': False,
                        'display_name': u'Enable Timed Exams',
                        'help': u'Enter true or false. If this value is true, '
                                u'timed exams are enabled in your course. '
                                u'Regardless of this setting, timed exams are enabled if Enable Proctored Exams is set to true.',
                        'value': True
                    },
                'discussion_blackouts':
                    {
                        'deprecated': False,
                        'display_name': u'Discussion Blackout Dates',
                        'help': u'Enter pairs of dates between which students cannot post to discussion forums. '
                                u'Inside the provided brackets, enter an additional set of square brackets '
                                u'surrounding each pair of dates you add. Format each pair of dates as ["YYYY-MM-DD", "YYYY-MM-DD"]. '
                                u'To specify times as well as dates, format each pair as ["YYYY-MM-DDTHH:MM", "YYYY-MM-DDTHH:MM"]. '
                                u'Be sure to include the "T" between the date and time. '
                                u'For example, an entry defining two blackout periods looks like this, '
                                u'including the outer pair of square brackets: [["2015-09-15", "2015-09-21"], ["2015-10-01", "2015-10-08"]] ',
                        'value': []
                    },
                'due':
                    {
                        'deprecated': False,
                        'display_name': u'Due Date',
                        'help': u'Enter the date by which problems are due.',
                        'value': None
                    },
                'html_textbooks':
                    {
                        'deprecated': False,
                        'display_name': u'HTML Textbooks',
                        'help': u'For HTML textbooks that appear as separate tabs in the course, '
                                u'enter the name of the tab (usually the title of the book) as well as the URLs '
                                u'and titles of each chapter in the book.',
                        'value': []
                    },
                'invitation_only':
                    {
                        'deprecated': False,
                        'display_name': u'Invitation Only',
                        'help': u'Whether to restrict enrollment to invitation by the course staff.',
                        'value': False
                    },
                'no_grade':
                    {
                        'deprecated': False,
                        'display_name': u'Course Not Graded',
                        'help': u'Enter true or false. If true, the course will not be graded.',
                        'value': False
                    },
                'catalog_visibility':
                    {
                        'deprecated': False,
                        'display_name': u'Course Visibility In Catalog',
                        'help': u"Defines the access permissions for showing the course in the course catalog. "
                                u"This can be set to one of three values: 'both' (show in catalog and allow access to about page), "
                                u"'about' (only allow access to about page), "
                                u"'none' (do not show in catalog and do not allow access to an about page).",
                        'value': u'both'
                    },
                'instructor_info':
                    {
                        'deprecated': False,
                        'display_name': u'Course Instructor',
                        'help': u'Enter the details for Course Instructor',
                        'value':
                            {
                                'instructors': [u'user014@test.com.vn']
                            }
                    },
                'display_organization': {
                    'deprecated': False,
                    'display_name': u'Course Organization Display String',
                    'help': u'Enter the course organization that you want to appear in the course. '
                            u'This setting overrides the organization that you entered when you created the course. '
                            u'To use the organization that you entered when you created the course, enter null.',
                    'value': None
                },
                'days_early_for_beta':
                    {
                        'deprecated': False,
                        'display_name': u'Days Early for Beta Users',
                        'help': u'Enter the number of days before the start date that beta users can access the course.',
                        'value': None
                    },
                'mobile_available':
                    {
                        'deprecated': False,
                        'display_name': u'Mobile Course Available',
                        'help': u'Enter true or false. If true, the course will be available to mobile devices.',
                        'value': False
                    },
                'enable_ccx':
                    {
                        'deprecated': False,
                        'display_name': u'Enable CCX',
                        'help': u'Allow course instructors to assign CCX Coach roles, and allow coaches to manage Custom Courses on edX. '
                                u'When false, Custom Courses cannot be created, but existing Custom Courses will be preserved.',
                        'value': False
                    },
                'max_attempts':
                    {
                        'deprecated': False,
                        'display_name': u'Maximum Attempts',
                        'help': u'Enter the maximum number of times a student can try to answer problems. '
                                u'By default, Maximum Attempts is set to null, '
                                u'meaning that students have an unlimited number of attempts for problems. '
                                u'You can override this course-wide setting for individual problems. '
                                u'However, if the course-wide setting is a specific number, '
                                u'you cannot set the Maximum Attempts for individual problems to unlimited.',
                        'value': None
                    },
                'advanced_modules':
                    {
                        'deprecated': False,
                        'display_name': u'Advanced Module List',
                        'help': u'Enter the names of the advanced modules to use in your course.',
                        'value': [
                            u'officemix',
                            u'google-calender',
                            u'poll',
                            u'xb_scorm',
                            u'videojs',
                            u'edx_sga',
                            u'paellavideo',
                            u'scormxblock',
                            u'vimeo',
                            u'mt3d',
                            u'acid',
                            u'carousel',
                            u'flash',
                            u'forum_leaderboard',
                            u'adventure',
                            u'activetable',
                            u'animation',
                            u'voicerecognizer',
                            u'flow-control',
                            u'pdf',
                            u'piechart',
                            u'protoru',
                            u'pumukit',
                            u'qualtricssurvey',
                            u'schoolyourself',
                            u'uniplay',
                            u'vectordraw',
                            u'zoomcloudrecording',
                            u'azure_media_services',
                            u'flash'
                        ]
                    },
                'disable_progress_graph':
                    {
                        'deprecated': False,
                        'display_name': u'Disable Progress Graph',
                        'help': u'Enter true or false. If true, students cannot view the progress graph.',
                        'value': False
                    },
                'end_of_course_survey_url':
                    {
                        'deprecated': True,
                        'display_name': u'Course Survey URL',
                        'help': u'Enter the URL for the end-of-course survey. If your course does not have a survey, enter null.',
                        'value': None
                    },
                'cert_html_view_overrides':
                    {
                        'deprecated': False,
                        'display_name': u'Certificate Web/HTML View Overrides',
                        'help': u'Enter course-specific overrides for the Web/HTML template parameters here (JSON format)',
                        'value': {}
                    },
                'due_date_display_format':
                    {
                        'deprecated': False,
                        'display_name': u'Due Date Display Format',
                        'help': u'Enter the format for due dates. The default is Mon DD, YYYY. Enter "%m-%d-%Y" for MM-DD-YYYY, '
                                u'"%d-%m-%Y" for DD-MM-YYYY, "%Y-%m-%d" for YYYY-MM-DD, or "%Y-%d-%m" for YYYY-DD-MM.',
                        'value': None
                    },
                'matlab_api_key':
                    {
                        'deprecated': False,
                        'display_name': 'Matlab API key',
                        'help': u'Enter the API key provided by MathWorks for accessing the MATLAB Hosted Service. '
                                u'This key is granted for exclusive use in this course for the specified duration. '
                                u'Do not share the API key with other courses. '
                                u'Notify MathWorks immediately if you believe the key is exposed or compromised. '
                                u'To obtain a key for your course, or to report an issue, please contact moocsupport@mathworks.com',
                        'value': None
                    },
                'bypass_home':
                    {
                        'deprecated': True,
                        'display_name': u'Bypass Course Home',
                        'help': u'Bypass the course home tab when students arrive from the dashboard, '
                                u'sending them directly to course content.',
                        'value': False
                    },
                'cert_name_long':
                    {
                        'deprecated': False,
                        'display_name': u'Certificate Name (Long)',
                        'help': u'Use this setting only when generating PDF certificates. Between quotation marks, '
                                u'enter the long name of the type of certificate that students receive when they complete the course. '
                                u'For instance, "Certificate of Achievement".',
                        'value': u''
                    },
                'cert_name_short':
                    {
                        'deprecated': False,
                        'display_name': u'Certificate Name (Short)',
                        'help': u'Use this setting only when generating PDF certificates. '
                                u'Between quotation marks, enter the short name of the type of certificate that students '
                                u'receive when they complete the course. For instance, "Certificate".',
                        'value': u''
                    },
                'enable_proctored_exams':
                    {
                        'deprecated': False,
                        'display_name': u'Enable Proctored Exams',
                        'help': u'Enter true or false. If this value is true, '
                                u'proctored exams are enabled in your course. '
                                u'Note that enabling proctored exams will also enable timed exams.',
                        'value': False
                    },
                'annotation_storage_url':
                    {
                        'deprecated': False,
                        'display_name': u'URL for Annotation Storage',
                        'help': u'Enter the location of the annotation storage server. '
                                u'The textannotation, videoannotation, and imageannotation advanced modules require this setting.',
                        'value': u'http://your_annotation_storage.com'
                    },
                'xqa_key':
                    {
                        'deprecated': True,
                        'display_name': u'XQA Key',
                        'help': u'This setting is not currently supported.',
                        'value': None
                    },
                'info_sidebar_name':
                    {
                        'deprecated': False,
                        'display_name': u'Course Home Sidebar Name',
                        'help': u'Enter the heading that you want students to see above your course handouts on the Course Home page. '
                                u'Your course handouts appear in the right panel of the page.',
                        'value': u'Course Handouts'
                    },
                'display_coursenumber':
                    {
                        'deprecated': False,
                        'display_name': u'Course Number Display String',
                        'help': u'Enter the course number that you want to appear in the course. '
                                u'This setting overrides the course number that you entered when you created the course. '
                                u'To use the course number that you entered when you created the course, enter null.',
                        'value': u''
                    },
                'use_latex_compiler':
                    {
                        'deprecated': False,
                        'display_name': u'Enable LaTeX Compiler',
                        'help': u'Enter true or false. If true, you can use the LaTeX templates for HTML components and advanced Problem components.',
                        'value': False
                    },
                'allow_anonymous_to_peers':
                    {
                        'deprecated': False,
                        'display_name': u'Allow Anonymous Discussion Posts to Peers',
                        'help': u'Enter true or false. If true, students can create discussion posts that are anonymous to other students. '
                                u'This setting does not make posts anonymous to course staff.',
                        'value': True
                    },
                'create_zendesk_tickets':
                    {
                        'deprecated': False,
                        'display_name': u'Create Zendesk Tickets For Suspicious Proctored Exam Attempts',
                        'help': u'Enter true or false. If this value is true, a Zendesk ticket will be created for suspicious attempts.',
                        'value': True
                    },
                'static_asset_path':
                    {
                        'deprecated': False,
                        'display_name': u'Static Asset Path',
                        'help': u'Enter the path to use for files on the Files & Uploads page. '
                                u'This value overrides the Studio default, c4x://.',
                        'value': u''
                    },
                'hide_progress_tab':
                    {
                        'deprecated': True,
                        'display_name': u'Hide Progress Tab', u'help': u'Allows hiding of the progress tab.',
                        'value': None
                    },
                'show_calculator':
                    {
                        'deprecated': False,
                        'display_name': u'Show Calculator',
                        'help': u'Enter true or false. When true, students can see the calculator in the course.',
                        'value': False
                    },
                'cosmetic_display_price':
                    {
                        'deprecated': False,
                        'display_name': u'Cosmetic Course Display Price',
                        'help': u'The cost displayed to students for enrolling in the course. '
                                u'If a paid course registration price is set by an administrator in the database, '
                                u'that price will be displayed instead of this one.',
                        'value': 0
                    },
                'ccx_connector':
                    {
                        'deprecated': False,
                        'display_name': u'CCX Connector URL',
                        'help': u"URL for CCX Connector application for managing creation of CCXs. (optional). "
                                u"Ignored unless 'Enable CCX' is set to 'true'.",
                        'value': u''
                    },
                'advertised_start':
                    {
                        'deprecated': False,
                        'display_name': u'Course Advertised Start',
                        'help': u'Enter the text that you want to use as the advertised starting time frame for the course, '
                                u'such as "Winter 2018". If you enter null for this value, '
                                u'the start date that you have set for this course is used.',
                        'value': None
                    },
                'cert_html_view_enabled':
                    {
                        'deprecated': False,
                        'display_name': u'Certificate Web/HTML View Enabled',
                        'help': u'If true, certificate Web/HTML views are enabled for the course.',
                        'value': False
                    },
                'rerandomize':
                    {
                        'deprecated': False,
                        'display_name': u'Randomization',
                        'help': u'Specify the default for how often variable values in a problem are randomized. '
                                u'This setting should be set to "never" unless you plan to provide a Python script to identify '
                                u'and randomize values in most of the problems in your course. '
                                u'Valid values are "always", "onreset", "never", and "per_student".',
                        'value': u'never'
                    },
                'video_upload_pipeline':
                    {
                        'deprecated': False,
                        'display_name': u'Video Upload Credentials',
                        'help': u"Enter the unique identifier for your course's video files provided by edX.",
                        'value': {}
                    },
                'course_image':
                    {
                        'deprecated': False,
                        'display_name': u'Course About Page Image',
                        'help': u'Edit the name of the course image file. You must upload this file on the Files & Uploads page. '
                                u'You can also set the course image on the Settings & Details page.',
                        'value': u'images (1).jpeg'
                    },
                'video_thumbnail_image':
                    {
                        'deprecated': False,
                        'display_name': u'Course Video Thumbnail Image',
                        'help': u'Edit the name of the video thumbnail image file. '
                                u'You can set the video thumbnail image on the Settings & Details page.',
                        'value': u'images_course_image.jpg'
                    },
                'learning_info':
                    {
                        'deprecated': False,
                        'display_name': u'Course Learning Information',
                        'help': u'Specify what student can learn from the course.',
                        'value': []
                    },
                'allow_public_wiki_access':
                    {
                        'deprecated': False,
                        'display_name': u'Allow Public Wiki Access',
                        'help': u"Enter true or false. If true, edX users can view the course wiki even if they're not enrolled in the course.",
                        'value': False
                    },
                'enable_subsection_gating':
                    {
                        'deprecated': False,
                        'display_name': u'Enable Subsection Prerequisites',
                        'help': u'Enter true or false. If this value is true, you can hide a subsection until learners earn '
                                u'a minimum score in another, prerequisite subsection.',
                        'value': False
                    },
                'css_class':
                    {
                        'deprecated': True,
                        'display_name': u'CSS Class for Course Reruns',
                        'help': u'Allows courses to share the same css class across runs even if they have different numbers.',
                        'value': u''
                    },
                'lti_passports':
                    {
                        'deprecated': False,
                        'display_name': u'LTI Passports',
                        'help': u'Enter the passports for course LTI tools in the following format: "id:client_key:client_secret".',
                        'value': []
                    },
                'banner_image':
                    {
                        'deprecated': False,
                        'display_name': u'Course Banner Image',
                        'help': u'Edit the name of the banner image file. You can set the banner image on the Settings & Details page.',
                        'value': u'images_course_image.jpg'
                    },
                'show_reset_button':
                    {
                        'deprecated': False,
                        'display_name': u'Show Reset Button for Problems',
                        'help': u"Enter true or false. If true, problems in the course default to always displaying a 'Reset' button. "
                                u"You can override this in each problem's settings. "
                                u"All existing problems are affected when this course-wide setting is changed.",
                        'value': False
                    },
                'allow_proctoring_opt_out':
                    {
                        'deprecated': False,
                        'display_name': u'Allow Opting Out of Proctored Exams',
                        'help': u'Enter true or false. If this value is true, '
                                u'learners can choose to take proctored exams without proctoring. '
                                u'If this value is false, all learners must take the exam with proctoring. '
                                u'This setting only applies if proctored exams are enabled for the course.',
                        'value': True
                    },
                'allow_anonymous':
                    {
                        'deprecated': False,
                        'display_name': u'Allow Anonymous Discussion Posts',
                        'help': u'Enter true or false. If true, students can create discussion posts that are anonymous to all users.',
                        'value':True
                    }
        }
        from models.settings.course_metadata import CourseMetadata

        is_valid, errors, updated_data = CourseMetadata.validate_and_update_from_json(
            course_module,
            request.json,
            user=request.user,
        )

        from cms.djangoapps.contentstore.views.course import advanced_settings_handler

        advanced_settings_handler(request, course_key_string='course-v1:LV+LV-DEV-PY-DJANGO+LV-DEV-PY-DJANGO')


