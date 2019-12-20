from rest_framework.permissions import BasePermission


class IsTeacher(BasePermission):
    message = 'The user is not a teacher'

    def has_permission(self, request, view):
        return request.user.is_teacher()


class IsAssistantOrTeacher(BasePermission):
    message = 'Student can\'t access this view'

    def has_permission(self, request, view):
        return request.user.is_teacher() or request.user.is_assitant()


class IsStudent(BasePermission):
    message = 'The user is not a student'

    def has_permission(self, request, view):
        return request.user.is_student()
