from django.db import models

# Create your models here.

class QUEST(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_text = models.CharField(max_length=200)

class IO(models.Model):
    question = models.ForeignKey(QUEST, to_field="question_id", on_delete=models.CASCADE) #親のオブジェクトが削除されたら同じidのオブジェクトを削除する
    io_id = models.IntegerField(default=0)
    input_text = models.CharField(max_length=200)
    output_text = models.CharField(max_length=200)