#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xdj
from opaque_keys.edx.keys import CourseKey, UsageKey
from xmodule.modulestore.django import modulestore
from xmodule.course_module import CourseDescriptor
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from xmodule.error_module import ErrorDescriptor
from xmodule.x_module import XModule
from xblock.core import XBlock
from django.contrib.auth.models import AnonymousUser
"""
/home/hcsadmin/edx-ginkgo.2-3/apps/edx/edx-platform/lms/djangoapps/courseware/access.py
def has_access(user, action, obj, course_key=None):
"""
def get_course_with_access(user, action, course_key, depth=0, check_if_enrolled=False):
    """
    Given a course_key, look up the corresponding course descriptor,
    check that the user has the access to perform the specified action
    on the course, and return the descriptor.

    Raises a 404 if the course_key is invalid, or the user doesn't have access.

    depth: The number of levels of children for the modulestore to cache. None means infinite depth

    check_if_enrolled: If true, additionally verifies that the user is either enrolled in the course
      or has staff access.
    """
    course = get_course_by_id(course_key, depth)
    check_course_access(course, user, action, check_if_enrolled)
    return course
def has_access(user, action, obj, course_key=None):
    """
    Check whether a user has the access to do action on obj.  Handles any magic
    switching based on various settings.

    Things this module understands:
    - start dates for modules
    - visible_to_staff_only for modules
    - DISABLE_START_DATES
    - different access for instructor, staff, course staff, and students.
    - mobile_available flag for course modules

    user: a Django user object. May be anonymous. If none is passed,
                    anonymous is assumed

    obj: The object to check access for.  A module, descriptor, location, or
                    certain special strings (e.g. 'global')

    action: A string specifying the action that the client is trying to perform.

    actions depend on the obj type, but include e.g. 'enroll' for courses.  See the
    type-specific functions below for the known actions for that type.

    course_key: A course_key specifying which course run this access is for.
        Required when accessing anything other than a CourseDescriptor, 'global',
        or a location with category 'course'

    Returns an AccessResponse object.  It is up to the caller to actually
    deny access in a way that makes sense in context.
    """
    # Just in case user is passed in as None, make them anonymous
    if not user:
        user = AnonymousUser()

    # Preview mode is only accessible by staff.
    if in_preview_mode() and course_key:
        if not has_staff_access_to_preview_mode(user, course_key):
            return ACCESS_DENIED

    # delegate the work to type-specific functions.
    # (start with more specific types, then get more general)
    if isinstance(obj, CourseDescriptor):
        return _has_access_course(user, action, obj)

    if isinstance(obj, CourseOverview):
        return _has_access_course(user, action, obj)

    if isinstance(obj, ErrorDescriptor):
        return _has_access_error_desc(user, action, obj, course_key)

    if isinstance(obj, XModule):
        return _has_access_xmodule(user, action, obj, course_key)

    # NOTE: any descriptor access checkers need to go above this
    if isinstance(obj, XBlock):
        return _has_access_descriptor(user, action, obj, course_key)

    if isinstance(obj, CourseKey):
        return _has_access_course_key(user, action, obj)

    if isinstance(obj, UsageKey):
        return _has_access_location(user, action, obj, course_key)

    if isinstance(obj, basestring):
        return _has_access_string(user, action, obj)

    # Passing an unknown object here is a coding error, so rather than
    # returning a default, complain.
    raise TypeError("Unknown object type in has_access(): '{0}'"
                    .format(type(obj)))

from lms.djangoapps.courseware import courses

"""get course of user"""
from courseware import access_utils

class LmsController(xdj.BaseController):
    def __init__(self):
        pass
    def get_course_key(self,id):
        if type(id) in [str, unicode]:
            return CourseKey.from_string(id)
        else:
            raise Exception("'id' must be str or unicode")
    def get_course_by_id(self,id):
        if type(id) in [str,unicode]:
            return courses.get_course(self.get_course_key(id))
        else:
            raise Exception("'id' must be str or unicode")

    def get_list_of_coursewares(self,user,org=None,*args,**kwargs):
        """
        Lấy danh sách các khóa học của học viên có các trường hợp sau:
        1- user nặc danh: tức chưa đăng nhập thì sẽ hiển thị danh sách các khóa học không invatation only
        2- user đã xác định: thì hiển thị danh sách các khóa học của user

        :param org:
        :param args:
        :param kwargs:
        :return:
        """
        # courses.get_courses(user,org,filter)
        # courses.get_courses(user,"lv",{"display_name__icontains":u'Kh\xf3a h\u1ecdc'})
        import branding
        # lst =branding.get_visible_courses()
        lst = courses.get_courses(user)
        ret =[]
        for item in lst:
            item.course_id=item.id.html_id()
            ret.append(item)
        return ret
    def is_course_open_for_learner(self,user,course):
        """
        Hàm này kiểm tra xem khóa học đã sẵn sàng cho user chưa
        :param user:
        :param course:
        :return:
        """
        return access_utils.is_course_open_for_learner(user,course)
