from lms_controller import LmsController
import xdj
from django.conf import settings
@xdj.Controller(
    url="course/{0}".format(settings.COURSE_ID_PATTERN),
    template="courses_course.html"
)
class CoursesController(LmsController):
    """
    /home/hcsadmin/edx-ginkgo.2-3/apps/edx/edx-platform/openedx/features/course_experience/views/course_home.py
    """
    def on_get(self,model):
        if isinstance(model,xdj.Model):
            course = self.get_course_by_id(model.params.course_id)
            model.course=course
            model.outline = xdj.dobject(self.get_courseware_outline(model.request,model.params.course_id))
            return self.render(model)