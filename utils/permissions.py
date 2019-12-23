from rest_framework.permissions import BasePermission


class IsTeacherPost(BasePermission):
    message = 'The user is not a teacher'

    def has_permission(self, request, view):
        return request.user.is_teacher() if request.method in ['POST', 'PUT', 'DELETE'] else True


class IsAssistantOrTeacherPostPutDelete(BasePermission):
    message = 'Only teacher and his assistants can create'

    def has_permission(self, request, view):
        return (request.user.is_teacher() or request.user.is_assistant()) if request.method in ['POST', 'PUT',
                                                                                                'DELETE'] else True


class IsStudent(BasePermission):
    message = 'The user is not a student'

    def has_permission(self, request, view):
        return request.user.is_student()


def allow_test_modification(user, test):
    if (user.is_assistant() and user.assistant.teacher_id != test.creator_id) or \
            (user.is_teacher() and user.teacher.id != test.creator_id):
        return False
    return True
