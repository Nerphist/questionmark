from rest_framework.permissions import BasePermission


class IsTeacherPost(BasePermission):
    message = 'The user is not a teacher'

    def has_permission(self, request, view):
        return request.user.is_teacher() if request.method == 'POST' else True


class IsAssistantOrTeacherPost(BasePermission):
    message = 'Only teacher and his assistants can create'

    def has_permission(self, request, view):
        print(view.queryset)
        return (request.user.is_teacher() or request.user.is_assitant()) if request.method == 'POST' else True


class IsStudent(BasePermission):
    message = 'The user is not a student'

    def has_permission(self, request, view):
        return request.user.is_student()


def allow_test_modification(user, test):
    if (user.is_assitant() and user.assistant.teacher_id != test.creator_id) or \
            (user.is_teacher() and user.teacher.id != test.creator_id):
        return False
    return True
