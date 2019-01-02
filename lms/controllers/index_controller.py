import xdj
from lms_controller import LmsController
@xdj.Controller(
    url="",
    template="index.html"
)
class IndexController(LmsController):
    def __init__(self):
        super(type(self),self).__init__()
    def on_get(self,model):
        if isinstance(model,xdj.Model):
            model.courses= self.get_list_of_coursewares(model.user)

            return self.render(model)