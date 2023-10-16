from django.urls import path
from django.contrib import admin
from .views import register,signin,logout,user_log,studentDataView,home,studentSection,profile,company_del,notadmin,coordinatorSection,showDriveList,applied,updateprofile,appliedListForStudent,appliedStudentList,selectcompanyname,displayCompList,CompList,elligibleStudents,mail_shortlistStudents,graph,trainingView,trainingPieChart


urlpatterns = [
    path('',home),
    path('signup', register),
    path('signin',signin),
    path('logout',logout),
    path('user',user_log),
    path('studentDataForm',studentDataView),
    path('studentSection',studentSection),
    path('profile',profile),
    path('comp',company_del),
    path('notadmin',notadmin),
    path('coordinatorSection',coordinatorSection),
    path('drivelist',showDriveList),
    path("applied/<int:id>",applied),
    path("updateprofile",updateprofile),
    path("drivelistforStudent",appliedListForStudent),
    path("coordinatorAppliedStudentsList",appliedStudentList),
    path('selectcomp',selectcompanyname),
    path('displayComp/<int:id>',displayCompList),
    path('list',CompList),
    path('elligible/<int:id>',elligibleStudents),
    path('sendMail/<int:id>/<int:comp_id>',mail_shortlistStudents),
    path("statistic",graph),
    path("training",trainingView),
    path('trainingStatistic',trainingPieChart)

]