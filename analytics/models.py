from django.db.models import UniqueConstraint, Q

from api_tests.models import Test, Question, Answer
from users.models import Student
from utils.models import AbstractCreateUpdateModel
from django.db import models


class SolvedTest(AbstractCreateUpdateModel):
    class Meta(AbstractCreateUpdateModel.Meta):
        db_table = 'solved_tests'
        constraints = [
            UniqueConstraint(fields=['test', 'student'], condition=Q(is_checked=False), name='only_one_test')]

    test = models.ForeignKey(Test, null=False, on_delete=models.CASCADE, db_index=True, related_name='solutions')
    student = models.ForeignKey(Student, null=True, on_delete=models.SET_DEFAULT,
                                default=Student.get_anonymous_student, db_index=True,
                                related_name='solved_tests')
    mark = models.IntegerField(default=0)
    is_checked = models.BooleanField(default=False)

    def set_mark(self):
        self.mark = int(100 * (len(list(filter(lambda x: x.correct, self.solved_questions.all()))) / len(
            self.test.questions.all())))
        self.save()

    def check_test(self):
        self.is_checked = True
        for question in self.solved_questions.all():
            question.set_correct()
        self.set_mark()


class SolvedQuestion(AbstractCreateUpdateModel):
    class Meta(AbstractCreateUpdateModel.Meta):
        db_table = 'solved_questions'
        unique_together = [['question', 'solved_test']]

    solved_test = models.ForeignKey(SolvedTest, null=False, on_delete=models.CASCADE, related_name='solved_questions')
    question = models.ForeignKey(Question, null=False, on_delete=models.CASCADE, related_name='solutions')
    correct = models.BooleanField(default=False)

    def set_correct(self):
        self.correct = list(map(lambda x: x.answer, self.solved_answers.all())) == list(
            filter(lambda x: x.is_right, self.question.answers.all()))
        self.save()


class SolvedAnswer(AbstractCreateUpdateModel):
    class Meta(AbstractCreateUpdateModel.Meta):
        db_table = 'solved_answers'
        unique_together = [['solved_question', 'answer']]

    solved_question = models.ForeignKey(SolvedQuestion, null=False, on_delete=models.CASCADE,
                                        related_name='solved_answers')
    answer = models.ForeignKey(Answer, null=False, on_delete=models.CASCADE, related_name='solutions')

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     saved = super().save(force_insert, force_update, using, update_fields)
    #     self.solved_question.set_correct()
    #     self.solved_question.solved_test.set_mark()
    #     return saved
    #
    # def delete(self, using=None, keep_parents=False):
    #     question = self.solved_question
    #     test = self.solved_question.solved_test
    #     deleted = super().delete(using, keep_parents)
    #     question.set_correct()
    #     test.set_mark()
    #     return deleted
