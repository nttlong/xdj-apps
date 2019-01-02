#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Controller này dùng để xem danh sách khóa học
"""
import xdj
@xdj.Controller(
    url="couserware/courses",
    template="couserware/courses.html"
)
class couserware_couser_controller(xdj.BaseController):
    def on_get(self,sender):
        return self.render(sender)
    def doLoadItems(self,sender):
        """
        https://programtalk.com/python-examples-amp/student.models.anonymous_id_for_user/
        :param sender:
        :return:
        """
        from sysadmin import entities

        import branding
        import courseware
        from sysadmin.entities import courseware as cw
        from xdj import pymqr
        from xdj import medxdb
        from django.contrib.auth.models import User
        import sysadmin
        import datetime
        from django.db.models import Q

        # courseware.models.StudentModule.objects.all()[0].student.last_name
        ret = branding.get_visible_courses()
        qr = pymqr.query(medxdb.db(), cw.modulestore_active_versions)
        for item in ret:
            # course = courseware.models.StudentModule.objects.get(course_id=item.id)
            x = qr.new().match(pymqr.funcs.expr((pymqr.docs.org == item.id.org) & (pymqr.docs.run == item.id.run) & (
                        pymqr.docs.course == item.id.course))).object
            fx=sysadmin.models.course_authors.course_authors()
            item.course_id=item.id.__str__()
            if not x.is_empty():
                authors= User.objects.filter(id=x.edited_by)
                if authors.__len__()>0:
                    sql_items=sysadmin.models.course_authors.course_authors._meta.model.objects.filter(Q(user_id=x.edited_by)&
                                                                                                      Q(course_id=item.id.__str__())).count()
                    item.author=xdj.dobject(username=authors[0].username)
                    if sql_items==0:
                        fx.user_id = x.edited_by
                        fx.course_id = item.id.__str__()
                        fx.created_on = datetime.datetime.now()
                        fx.save()
            item.totalActiveStudent=courseware.models.StudentModule.objects.filter(course_id=item.id).filter(module_type="course").count()
            """Tính số học viên đang tương tác với khóa học"""

        return ret
    def doDeleteItem(self,sender):
        from opaque_keys import edx
        course_id = edx.locator.CourseLocator.from_string(sender.post_data.course_id)
        import openedx.core.djangoapps.models as md
        modulestorr = md.course_details.modulestore()
        modulestorr.delete_course(course_id,sender.user.id)
        """Xóa khóa học, người xóa là user đang đăng nhập"""
        return {}
    @xdj.Page(
        url="course",
        template="couserware/course.html"
    )
    class course(object):
        def doLoadItem(self,sender):
            # x = branding.modulestore()._modulestore.create_course(org="X",
            """

            :param sender:
            :return:
            """
            """
            import cms.djangoapps.contentstore.views.course as C
            fields={'start': datetime.datetime(2030, 1, 1, 0, 0, tzinfo=<UTC>), 'cert_html_view_enabled': True, 'display_name': u'Kh\xf3a h\u1ecdc test 002', 'language': 'en', 'wiki_slug': u'LV.A001.B001'}
            store='split'
            C.create_new_course_in_store(store, user, org, number, run, fields)
            C._create_new_course(request, org, number, run, fields)
            C._create_or_rerun_course(request)
            request.json={u'org': u'LV', u'run': u'B001', u'display_name': u'Kh\xf3a h\u1ecdc test 002', u'number': u'A001'}
            /home/hcsadmin/edx-ginkgo.2-3/apps/edx/edx-platform/common/djangoapps/util/json_request.py
            import cms.djangoapps.contentstore.views.course as V
            V.course_handler(request)
            """
            #sender.request._body='{"org":"001","number":"001","display_name":"long-test","run":"001"}'
            from django.conf import settings
            if not hasattr(settings,"ADVANCED_PROBLEM_TYPES"):
                setattr(settings,"ADVANCED_PROBLEM_TYPES",[
                    dict(
                        boilerplate_name = None,
                        component="openassessment"
                    ),
                    dict(
                        boilerplate_name=None,
                        component="drag-and-drop-v2"
                    )
                ])
                """
                settings.ADVANCED_PROBLEM_TYPES
                    [{'boilerplate_name': None, 'component': 'openassessment'}, {'boilerplate_name': None, 'component': 'drag-and-drop-v2'}]
                """
            sender.request._body='{"org":"001","number":"001","display_name":"long-test","run":"001"}'
            # if sender.post_data.course_id=="*":
            #     import openedx.core.djangoapps.models as md
            #     modulestor = md.course_details.modulestore()
            #     modulestor.create_course(org="LV",course="Khóa học test",run=1,user_id=3)
            #     """org, course, run, user_id"""
            return {}
        def doCreateItem(self,sender):
            from django.conf import settings
            if not hasattr(settings, "ADVANCED_PROBLEM_TYPES"):
                """
                Kiểm tra cấu hình
                """
                setattr(settings, "ADVANCED_PROBLEM_TYPES", [
                    dict(
                        boilerplate_name=None,
                        component="openassessment"
                    ),
                    dict(
                        boilerplate_name=None,
                        component="drag-and-drop-v2"
                    )
                ])
            import json
            sender.request._body = json.dumps(sender.post_data.__dict__)
            # if sender.request._body.has_key("org") and \
            #         sender.request._body.has_key("number") and \
            #         sender.request._body.has_key("display_name") and \
            #         sender.request._body.has_key("run"):
            import cms.djangoapps.contentstore.views.course as V
            ret = V.course_handler(sender.request)
            return ret
            # else:
            #     return dict(
            #         error="Miss data"
            #     )
        def doNewSection(self,sender):
            """
            request._body='{"parent_locator":"block-v1:LV+001+001+type@course+block@course","category":"chapter","display_name":"Section"}'
            import cms.djangoapps.contentstore.views.item as V
            V.xblock_handler(sender.request)

            :param sender:
            :return:
            """
            pass




